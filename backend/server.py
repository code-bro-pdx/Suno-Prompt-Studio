"""Suno AI Song Prompt Generator backend.

Routes (all under /api):
  GET  /                         health
  GET  /knowledge                taxonomies + scale presets + banned words for UI
  POST /generate                 AI Mode: concept -> full prompt JSON (+validation, auto-repair x1)
  POST /assemble                 Form Mode: structured form -> full prompt JSON
  POST /fill-form                Hybrid helper: concept -> structured form payload
  POST /validate                 Stand-alone validation of an existing payload
  POST /library                  Save a prompt set to MongoDB
  GET  /library                  List saved prompt sets (newest first)
  GET  /library/{id}             Read one saved set
  DELETE /library/{id}           Delete a saved set
"""
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# Local imports
from llm_service import (  # noqa: E402
    fill_form_from_concept,
    generate_from_form,
    generate_prompt,
    repair_prompt,
)
from jobs import JobQueue  # noqa: E402
from suno_knowledge import (  # noqa: E402
    COMMON_SUBGENRES,
    ESPECIALLY_HARD_BANNED,
    FULL_BANNED_WORDS,
    INSTRUMENT_MODEL_EXAMPLES,
    ITALIAN_TEMPOS,
    MIX_TYPES,
    MOTHER_GENRES,
    PLAY_METHODS,
    RHYME_SCHEME_OPTIONS,
    SCALE_PRESETS,
    SECTION_DEFAULTS,
    SECTION_META_TAGS,
    SYLLABLE_RANGES,
    TRANSITION_TAGS,
    VOCAL_RANGES,
    VOCAL_TEXTURES,
)
from validators import validate_output  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("suno-api")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

app = FastAPI(title="Suno Song Prompt Generator API")
api = APIRouter(prefix="/api")
jobs = JobQueue(db)


# ---------- Schemas ----------

class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    concept: str = Field(..., min_length=4)
    auto_repair: bool = True


class AssembleRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    form: Dict[str, Any]
    auto_repair: bool = True


class FillFormRequest(BaseModel):
    concept: str = Field(..., min_length=4)


class ValidateRequest(BaseModel):
    payload: Dict[str, Any]


class LibraryItemCreate(BaseModel):
    title: Optional[str] = None
    concept: Optional[str] = None
    mode: str = Field("ai", description="ai | form | hybrid")
    payload: Dict[str, Any]
    validation: Optional[Dict[str, Any]] = None


class LibraryItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    concept: Optional[str] = None
    mode: str = "ai"
    payload: Dict[str, Any]
    validation: Optional[Dict[str, Any]] = None
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ---------- Helpers ----------

async def _generate_with_repair(concept: str, auto_repair: bool) -> Dict[str, Any]:
    """Call LLM, validate, repair once if errors exist."""
    data = await generate_prompt(concept)
    report = validate_output(data)
    repairs = 0
    if auto_repair and report["errors"]:
        try:
            data = await repair_prompt(
                concept,
                data,
                [e["message"] for e in report["errors"]],
            )
            report = validate_output(data)
            repairs = 1
        except Exception as e:
            logger.warning("repair failed: %s", e)
    return {"payload": data, "validation": report, "repairs": repairs}


async def _assemble_with_repair(form: Dict[str, Any], auto_repair: bool) -> Dict[str, Any]:
    data = await generate_from_form(form)
    report = validate_output(data)
    repairs = 0
    if auto_repair and report["errors"]:
        try:
            data = await repair_prompt(
                f"Structured form: {form}",
                data,
                [e["message"] for e in report["errors"]],
            )
            report = validate_output(data)
            repairs = 1
        except Exception as e:
            logger.warning("assemble repair failed: %s", e)
    return {"payload": data, "validation": report, "repairs": repairs}


# Job workers wrap the above for use with JobQueue.

async def _generate_worker(req: Dict[str, Any]) -> Dict[str, Any]:
    return await _generate_with_repair(req["concept"], req.get("auto_repair", True))


async def _assemble_worker(req: Dict[str, Any]) -> Dict[str, Any]:
    return await _assemble_with_repair(req["form"], req.get("auto_repair", True))


# ---------- Routes ----------

@api.get("/")
async def root():
    return {"message": "Suno Song Prompt Generator API", "status": "ok"}


@api.get("/knowledge")
async def knowledge():
    """Return taxonomies / catalogues used by the form UI."""
    return {
        "mother_genres": MOTHER_GENRES,
        "common_subgenres": COMMON_SUBGENRES,
        "italian_tempos": ITALIAN_TEMPOS,
        "vocal_ranges": VOCAL_RANGES,
        "vocal_textures": VOCAL_TEXTURES,
        "mix_types": MIX_TYPES,
        "scale_presets": SCALE_PRESETS,
        "section_meta_tags": SECTION_META_TAGS,
        "transition_tags": TRANSITION_TAGS,
        "section_defaults": SECTION_DEFAULTS,
        "syllable_ranges": SYLLABLE_RANGES,
        "rhyme_schemes": RHYME_SCHEME_OPTIONS,
        "instrument_models": INSTRUMENT_MODEL_EXAMPLES,
        "play_methods": PLAY_METHODS,
        "banned_words": sorted(set(FULL_BANNED_WORDS)),
        "especially_hard_banned": ESPECIALLY_HARD_BANNED,
    }


@api.post("/generate")
async def post_generate(req: GenerateRequest):
    """Async: enqueue and return job_id immediately. Poll /api/jobs/{id}."""
    job_id = await jobs.enqueue("generate", {
        "concept": req.concept,
        "auto_repair": req.auto_repair,
    })
    jobs.schedule(job_id, _generate_worker)
    return {"job_id": job_id, "status": "queued"}


@api.post("/generate/sync")
async def post_generate_sync(req: GenerateRequest):
    """Synchronous variant for tests / short-prompt fallback."""
    try:
        return await _generate_with_repair(req.concept, req.auto_repair)
    except Exception as e:
        logger.exception("generate failed")
        raise HTTPException(status_code=500, detail=str(e))


@api.post("/assemble")
async def post_assemble(req: AssembleRequest):
    """Async: enqueue and return job_id immediately. Poll /api/jobs/{id}."""
    job_id = await jobs.enqueue("assemble", {
        "form": req.form,
        "auto_repair": req.auto_repair,
    })
    jobs.schedule(job_id, _assemble_worker)
    return {"job_id": job_id, "status": "queued"}


@api.post("/assemble/sync")
async def post_assemble_sync(req: AssembleRequest):
    try:
        return await _assemble_with_repair(req.form, req.auto_repair)
    except Exception as e:
        logger.exception("assemble failed")
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/jobs/{job_id}")
async def get_job(job_id: str):
    doc = await jobs.get(job_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    return doc


@api.post("/fill-form")
async def post_fill_form(req: FillFormRequest):
    try:
        form = await fill_form_from_concept(req.concept)
        return {"form": form}
    except Exception as e:
        logger.exception("fill-form failed")
        raise HTTPException(status_code=500, detail=str(e))


@api.post("/validate")
async def post_validate(req: ValidateRequest):
    return validate_output(req.payload)


# ---------- Library CRUD ----------

@api.post("/library", response_model=LibraryItem)
async def create_library_item(item: LibraryItemCreate):
    payload = item.payload or {}
    title = (item.title or payload.get("title") or "Untitled Generation").strip()
    doc = LibraryItem(
        title=title,
        concept=item.concept,
        mode=item.mode,
        payload=payload,
        validation=item.validation,
    )
    await db.library.insert_one(doc.model_dump())
    return doc


@api.get("/library", response_model=List[LibraryItem])
async def list_library():
    cursor = db.library.find({}, {"_id": 0}).sort("created_at", -1).limit(200)
    items: List[LibraryItem] = []
    async for d in cursor:
        items.append(LibraryItem(**d))
    return items


@api.get("/library/{item_id}", response_model=LibraryItem)
async def get_library_item(item_id: str):
    doc = await db.library.find_one({"id": item_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return LibraryItem(**doc)


@api.delete("/library/{item_id}")
async def delete_library_item(item_id: str):
    result = await db.library.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": True, "id": item_id}


# ---------- App wiring ----------

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
