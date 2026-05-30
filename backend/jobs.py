"""Async job queue backed by MongoDB.

Jobs are documents in db.jobs with shape:
{
  id, kind ('generate' | 'assemble'),
  status ('queued' | 'running' | 'done' | 'error'),
  request (dict),
  result (dict | None),
  error (str | None),
  created_at, updated_at
}
"""
import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict

logger = logging.getLogger("suno-jobs")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobQueue:
    def __init__(self, db):
        self.db = db
        self.collection = db.jobs

    async def enqueue(self, kind: str, request: Dict[str, Any]) -> str:
        job_id = str(uuid.uuid4())
        await self.collection.insert_one({
            "id": job_id,
            "kind": kind,
            "status": "queued",
            "request": request,
            "result": None,
            "error": None,
            "created_at": _now(),
            "updated_at": _now(),
        })
        return job_id

    async def update(self, job_id: str, patch: Dict[str, Any]) -> None:
        patch["updated_at"] = _now()
        await self.collection.update_one({"id": job_id}, {"$set": patch})

    async def get(self, job_id: str) -> Dict[str, Any] | None:
        return await self.collection.find_one({"id": job_id}, {"_id": 0})

    async def run(
        self,
        job_id: str,
        worker: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
    ) -> None:
        """Run a worker against the job's request; update status to running/done/error."""
        await self.update(job_id, {"status": "running"})
        try:
            doc = await self.get(job_id)
            if not doc:
                return
            result = await worker(doc["request"])
            await self.update(job_id, {"status": "done", "result": result})
        except Exception as e:
            logger.exception("job %s failed", job_id)
            await self.update(job_id, {"status": "error", "error": str(e)})

    def schedule(
        self,
        job_id: str,
        worker: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
    ) -> None:
        """Fire-and-forget background task."""
        asyncio.create_task(self.run(job_id, worker))
