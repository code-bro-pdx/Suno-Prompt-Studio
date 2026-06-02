"""Wrapper around emergentintegrations LlmChat for Suno prompt generation."""
import json
import os
import re
import uuid
from typing import Any, Dict, Optional

from emergentintegrations.llm.chat import LlmChat, UserMessage

from suno_knowledge import build_system_prompt

MODEL_NAME = "claude-sonnet-4-5-20250929"
PROVIDER = "anthropic"
MAX_TOKENS = 12000


def _extract_json(text: str) -> Dict[str, Any]:
    """Robust JSON extractor: strips code fences and finds the first { ... }."""
    if not text:
        raise ValueError("empty response")
    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*\})\s*```", text)
    if fenced:
        return json.loads(fenced.group(1))
    # Greedy match outer braces
    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1 or last <= first:
        raise ValueError("no JSON object found")
    return json.loads(text[first:last + 1])


def _new_chat(session_id: Optional[str] = None) -> LlmChat:
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        raise RuntimeError("EMERGENT_LLM_KEY is not configured.")
    sid = session_id or f"suno-{uuid.uuid4().hex[:12]}"
    return (
        LlmChat(
            api_key=api_key,
            session_id=sid,
            system_message=build_system_prompt(),
        )
        .with_model(PROVIDER, MODEL_NAME)
        .with_params(max_tokens=MAX_TOKENS)
    )


async def generate_prompt(user_concept: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """AI Mode: free-form concept → full Suno prompt JSON."""
    chat = _new_chat(session_id)
    response = await chat.send_message(UserMessage(text=user_concept))
    return _extract_json(response)


async def repair_prompt(
    prior_concept: str,
    prior_response_json: Dict[str, Any],
    error_messages: list[str],
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Ask the model to fix specific validation errors and return revised JSON."""
    chat = _new_chat(session_id)
    feedback = (
        "You produced this JSON for the concept below, but it failed these hard "
        "validations. Fix ALL violations and return ONE corrected JSON object with the "
        "SAME schema, no markdown fences, no prose.\n\n"
        f"USER CONCEPT:\n{prior_concept}\n\n"
        f"PRIOR JSON (truncated if long):\n{json.dumps(prior_response_json)[:9000]}\n\n"
        "HARD VIOLATIONS TO FIX:\n- " + "\n- ".join(error_messages) + "\n\n"
        "Reminders: banned words apply to LYRICS only. Style Prompt ≤ 1000 chars. "
        "sections[].bars must sum to structure_rhyme_map.total_bars. Practical target < 4:00."
    )
    response = await chat.send_message(UserMessage(text=feedback))
    return _extract_json(response)


async def fill_form_from_concept(user_concept: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """Hybrid helper: take natural-language concept and return a structured form payload."""
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        raise RuntimeError("EMERGENT_LLM_KEY is not configured.")
    sid = session_id or f"suno-form-{uuid.uuid4().hex[:12]}"
    system_msg = (
        "You convert a natural-language song concept into a structured form payload "
        "for a Suno prompt generator. Return ONE JSON object only (no fences). Schema:\n"
        "{\n"
        '  "title": string,\n'
        '  "era": string (e.g., "2010s"),\n'
        '  "bpm": integer 40-200,\n'
        '  "italian_tempo": string (e.g., "Allegro"),\n'
        '  "time_signature": string,\n'
        '  "mother_genre": string,\n'
        '  "subgenres": [ {"name": string, "weight_percent": integer} ],\n'
        '  "mood": string,\n'
        '  "instruments": [ {"type": string, "model": string, "play_method": string} ],\n'
        '  "vocal_gender": "Male" | "Female" | "Non-binary",\n'
        '  "vocal_range": string (e.g., "Female Mezzo-Soprano A3-A5"),\n'
        '  "vocal_textures": [string],\n'
        '  "mix": "Raw" | "Wet" | "Dry" | "Parallel",\n'
        '  "section_order": [string],\n'
        '  "exclude_eras": [string],\n'
        '  "exclude_genres": [string],\n'
        '  "lyrical_world": string\n'
        "}\n"
        "Use the Suno guide's preferred vocabulary (Italian tempos, technical vocal ranges, instrument models)."
    )
    chat = (
        LlmChat(api_key=api_key, session_id=sid, system_message=system_msg)
        .with_model(PROVIDER, MODEL_NAME)
        .with_params(max_tokens=2500)
    )
    response = await chat.send_message(UserMessage(text=user_concept))
    return _extract_json(response)


async def generate_from_form(form: Dict[str, Any], session_id: Optional[str] = None) -> Dict[str, Any]:
    """Form Mode: structured payload → full Suno prompt JSON (LLM-assembled)."""
    concept = (
        "Build a Suno prompt using these structured choices. Honor every field; "
        "if any field conflicts with the rules, prefer the rule and note it in workflow_advice.\n\n"
        f"FORM PAYLOAD:\n{json.dumps(form, indent=2)}"
    )
    return await generate_prompt(concept, session_id)
