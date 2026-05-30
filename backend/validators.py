"""Validation helpers for Suno prompt outputs.
Light, dependency-free heuristics that match the rules from Prompt 05
and the MasterofSFL guide.
"""
import re
from typing import Any, Dict, List

from suno_knowledge import ESPECIALLY_HARD_BANNED, FULL_BANNED_WORDS

MAX_STYLE_PROMPT_CHARS = 1000
MAX_DURATION_SEC = 4 * 60  # under 4:00 hard cap


def check_banned_words(text: str) -> List[str]:
    """Return a sorted unique list of banned words present in text.
    Single tokens use word-boundary matching; multi-word phrases
    use substring matching.
    """
    if not text:
        return []
    text_lower = text.lower()
    hits: List[str] = []
    for word in set(FULL_BANNED_WORDS):
        w = word.lower()
        if " " in w or "-" in w:
            if w in text_lower:
                hits.append(word)
        else:
            if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", text_lower):
                hits.append(word)
    return sorted(set(hits))


def _parse_practical_target(s: str) -> Dict[str, int] | None:
    if not s:
        return None
    m = re.search(r"(\d+):(\d{2})\s*[-–]\s*(\d+):(\d{2})", s)
    if not m:
        m2 = re.search(r"(\d+):(\d{2})", s)
        if m2:
            return {
                "low": int(m2.group(1)) * 60 + int(m2.group(2)),
                "high": int(m2.group(1)) * 60 + int(m2.group(2)),
            }
        return None
    return {
        "low": int(m.group(1)) * 60 + int(m.group(2)),
        "high": int(m.group(3)) * 60 + int(m.group(4)),
    }


def compute_strict_duration(total_bars: int, bpm: int) -> str:
    if not total_bars or not bpm:
        return "0:00"
    sec = int(round(total_bars * (60.0 / bpm) * 4))
    return f"{sec // 60}:{sec % 60:02d}"


def validate_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a structured report: {errors:[], warnings:[], info:{}}"""
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    info: Dict[str, Any] = {}

    # ----- style_prompt length -----
    sp = data.get("style_prompt", "") or ""
    sp_len = len(sp)
    info["style_prompt_char_count"] = sp_len
    if sp_len == 0:
        errors.append({"code": "empty_style_prompt", "message": "Style Prompt is empty."})
    elif sp_len > MAX_STYLE_PROMPT_CHARS:
        errors.append({
            "code": "style_prompt_too_long",
            "message": f"Style Prompt is {sp_len} chars; max is {MAX_STYLE_PROMPT_CHARS}.",
            "meta": {"length": sp_len, "max": MAX_STYLE_PROMPT_CHARS},
        })
    elif sp_len > 950:
        warnings.append({
            "code": "style_prompt_near_limit",
            "message": f"Style Prompt at {sp_len}/{MAX_STYLE_PROMPT_CHARS} chars — trim for safety.",
        })

    # ----- banned words in LYRICS only (per Prompt 05) -----
    lyrics = data.get("lyrics", "") or ""
    ly_bans = check_banned_words(lyrics)
    info["banned_words_in_lyrics"] = ly_bans
    allowed = data.get("validation_self_check", {}).get("banned_words_used") or []
    allowed_lower = {str(w).lower().strip(".,;:") for w in allowed}
    unauthorized = [w for w in ly_bans if w.lower() not in allowed_lower]
    if unauthorized:
        errors.append({
            "code": "banned_words_in_lyrics",
            "message": f"Banned word(s) in lyrics: {', '.join(unauthorized)}.",
            "meta": {"words": unauthorized},
        })
    hard_hits = [w for w in ly_bans if w.lower() in ESPECIALLY_HARD_BANNED]
    if hard_hits:
        errors.append({
            "code": "hard_banned_in_lyrics",
            "message": f"Zero-tolerance word(s) in lyrics: {', '.join(hard_hits)}.",
            "meta": {"words": hard_hits},
        })

    # ----- structure & bar math -----
    srm = data.get("structure_rhyme_map", {}) or {}
    sections = srm.get("sections", []) or []
    bars_sum = 0
    for s in sections:
        try:
            bars_sum += int(s.get("bars", 0) or 0)
        except (TypeError, ValueError):
            pass
    total_bars = int(srm.get("total_bars", 0) or 0)
    info["bars_sum"] = bars_sum
    info["total_bars"] = total_bars
    if total_bars and bars_sum != total_bars:
        errors.append({
            "code": "bars_mismatch",
            "message": f"Section bars sum to {bars_sum} but total_bars is {total_bars}.",
            "meta": {"sum": bars_sum, "declared": total_bars},
        })

    bpm = srm.get("bpm")
    if isinstance(bpm, int) and bpm > 0 and total_bars > 0:
        computed = compute_strict_duration(total_bars, bpm)
        info["computed_strict_duration"] = computed
        reported = (srm.get("strict_duration") or "").strip()
        if reported and reported != computed:
            warnings.append({
                "code": "strict_duration_mismatch",
                "message": f"strict_duration reported '{reported}' vs computed '{computed}'.",
            })

        practical = _parse_practical_target(srm.get("practical_target") or "")
        if practical:
            info["practical_target_seconds"] = practical
            if practical["high"] >= MAX_DURATION_SEC:
                errors.append({
                    "code": "practical_target_over_4_min",
                    "message": f"Practical target upper bound ≥ 4:00.",
                })

    # ----- rhyme variety -----
    schemes = [s.get("rhyme_scheme", "") or "" for s in sections]
    sung_schemes = [s for s in schemes if s and s.lower() != "instrumental"]
    if len(sung_schemes) >= 3 and len(set(sung_schemes)) == 1:
        warnings.append({
            "code": "identical_rhymes",
            "message": "All sung sections share the same rhyme scheme.",
        })
    verse = next(
        (s for s in sections if "verse" in (s.get("label") or "").lower()),
        None,
    )
    chorus = next(
        (s for s in sections
         if "chorus" in (s.get("label") or "").lower()
         and "post" not in (s.get("label") or "").lower()
         and "pre" not in (s.get("label") or "").lower()),
        None,
    )
    if verse and chorus and verse.get("rhyme_scheme") and chorus.get("rhyme_scheme"):
        if verse.get("rhyme_scheme") == chorus.get("rhyme_scheme"):
            warnings.append({
                "code": "verse_chorus_same_rhyme",
                "message": f"Verse and chorus share rhyme scheme '{verse.get('rhyme_scheme')}'.",
            })

    # ----- section energy notes -----
    for s in sections:
        note = (s.get("energy_note") or "").strip()
        wc = len(note.split())
        if not (3 <= wc <= 12):
            warnings.append({
                "code": "energy_note_length",
                "message": f"Section '{s.get('label')}' energy note word count is {wc} (target 4–8).",
            })

    return {"errors": errors, "warnings": warnings, "info": info}
