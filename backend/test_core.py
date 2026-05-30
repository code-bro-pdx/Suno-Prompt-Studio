"""POC: Validate that Claude Sonnet 4.5 generates a valid Suno prompt JSON
that respects the banned-words rule, 1000-char style-prompt limit, and
structural commitment rules.

Run: python /app/backend/test_core.py
"""
import asyncio
import json
import os
import re
import sys
from pathlib import Path

# Ensure local imports work
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: E402

from suno_knowledge import (  # noqa: E402
    ESPECIALLY_HARD_BANNED,
    FULL_BANNED_WORDS,
    build_system_prompt,
)

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")
MODEL_NAME = "claude-sonnet-4-5-20250929"


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of LLM output, even if wrapped in fences."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))
    obj_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if obj_match:
        return json.loads(obj_match.group(0))
    raise ValueError("No JSON object found in LLM response")


def check_banned_words(text: str) -> list[str]:
    text_lower = text.lower()
    hits: list[str] = []
    # Whole-word match for single words; substring for multi-word phrases
    for word in set(FULL_BANNED_WORDS):
        pattern = rf"(?<![a-z]){re.escape(word.lower())}(?![a-z])"
        if re.search(pattern, text_lower):
            hits.append(word)
    return sorted(set(hits))


def validate_output(data: dict) -> dict:
    report = {"errors": [], "warnings": [], "info": {}}

    # 1) style_prompt length
    sp = data.get("style_prompt", "")
    sp_len = len(sp)
    report["info"]["style_prompt_char_count"] = sp_len
    if sp_len == 0:
        report["errors"].append("style_prompt is empty")
    if sp_len > 1000:
        report["errors"].append(f"style_prompt length {sp_len} exceeds 1000")

    # 2) banned words — LYRICS ONLY (Style Prompt is technical, exempt)
    lyrics = data.get("lyrics", "")
    ly_bans = check_banned_words(lyrics)
    if ly_bans:
        allowed = data.get("validation_self_check", {}).get("banned_words_used") or []
        allowed_lower = {w.lower() for w in allowed}
        unauthorized = [w for w in ly_bans if w.lower() not in allowed_lower]
        if unauthorized:
            report["errors"].append(f"unauthorized banned words in lyrics: {unauthorized}")
        else:
            report["warnings"].append(f"banned words in lyrics (logged): {ly_bans}")

    # Especially-hard-banned check (zero tolerance in lyrics)
    hard_hits = [w for w in ly_bans if w.lower() in ESPECIALLY_HARD_BANNED]
    if hard_hits:
        report["errors"].append(f"especially-hard-banned in lyrics: {hard_hits}")

    # 3) bar count consistency
    srm = data.get("structure_rhyme_map", {})
    sections = srm.get("sections", []) or []
    bars_sum = sum(int(s.get("bars", 0) or 0) for s in sections)
    total_bars = int(srm.get("total_bars", 0) or 0)
    report["info"]["bars_sum"] = bars_sum
    report["info"]["total_bars"] = total_bars
    if bars_sum != total_bars:
        report["errors"].append(
            f"bars sum {bars_sum} != total_bars {total_bars}"
        )

    # 4) strict duration math
    bpm = srm.get("bpm")
    if isinstance(bpm, int) and bpm > 0 and total_bars > 0:
        strict_sec = total_bars * (60.0 / bpm) * 4
        m, s = divmod(int(round(strict_sec)), 60)
        computed = f"{m}:{s:02d}"
        reported = srm.get("strict_duration", "")
        report["info"]["computed_strict_duration"] = computed
        if reported and reported.strip() != computed:
            report["warnings"].append(
                f"strict_duration reported '{reported}' vs computed '{computed}'"
            )
        # under 4:00 sanity for practical target string
        practical = (srm.get("practical_target") or "").strip()
        # parse upper bound
        m_match = re.search(r"(\d+):(\d{2})\s*-\s*(\d+):(\d{2})", practical)
        if m_match:
            upper_min, upper_sec = int(m_match.group(3)), int(m_match.group(4))
            if upper_min >= 4:
                report["errors"].append(
                    f"practical_target upper bound >= 4:00 ({practical})"
                )

    # 5) rhyme scheme variety
    schemes = [s.get("rhyme_scheme", "") for s in sections]
    sung = [s for s in schemes if s and s.lower() != "instrumental"]
    if len(sung) >= 3 and len(set(sung)) == 1:
        report["warnings"].append("all sung sections share identical rhyme scheme")

    # 6) verse vs chorus distinct
    verse = next((s for s in sections if "verse" in s.get("label", "").lower()), None)
    chorus = next((s for s in sections if "chorus" in s.get("label", "").lower() and "post" not in s.get("label","").lower()), None)
    if verse and chorus and verse.get("rhyme_scheme") == chorus.get("rhyme_scheme"):
        report["warnings"].append(
            f"verse and chorus share scheme: {verse.get('rhyme_scheme')}"
        )

    # 7) energy_note length
    for s in sections:
        note = (s.get("energy_note") or "").strip()
        wc = len(note.split())
        if not (3 <= wc <= 10):
            report["warnings"].append(
                f"section {s.get('label')} energy_note word count {wc} (target 4-8)"
            )

    return report


async def run_one(label: str, user_concept: str, max_repairs: int = 2) -> dict:
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"poc-{label}",
        system_message=build_system_prompt(),
    ).with_model("anthropic", MODEL_NAME).with_params(max_tokens=12000)

    print(f"\n{'=' * 70}\n>>> RUN: {label}\n{'=' * 70}")
    print(f"Concept: {user_concept[:200]}")
    response = await chat.send_message(UserMessage(text=user_concept))
    print(f"\n--- RAW RESPONSE LENGTH: {len(response)} chars ---")
    try:
        data = extract_json(response)
    except Exception as e:
        print(f"!! JSON PARSE FAILED: {e}")
        print(response[:2000])
        return {"label": label, "ok": False, "reason": "json parse"}

    report = validate_output(data)

    # Repair loop: if errors, feed them back once
    repairs = 0
    while report["errors"] and repairs < max_repairs:
        repairs += 1
        print(f"\n!! Errors detected, attempting repair {repairs}/{max_repairs}")
        print(f"   {report['errors']}")
        repair_msg = (
            "Your previous JSON had these HARD violations. Fix ALL of them and return a corrected "
            "JSON object with the SAME schema:\n- "
            + "\n- ".join(report["errors"])
            + "\n\nReminder: banned words apply to LYRICS only (not Style Prompt). "
            "If style_prompt > 1000 chars, compress instrument descriptors. "
            "Ensure bars sum equals total_bars. Return one JSON object only."
        )
        response = await chat.send_message(UserMessage(text=repair_msg))
        try:
            data = extract_json(response)
        except Exception as e:
            print(f"   repair json parse failed: {e}")
            break
        report = validate_output(data)

    print(f"\n--- TITLE: {data.get('title')} ---")
    print(f"--- STYLE PROMPT ({report['info']['style_prompt_char_count']} chars) ---")
    print(data.get("style_prompt", "")[:600])
    print(f"\n--- EXCLUDE STYLES ---")
    print(data.get("exclude_styles", "")[:400])
    print(f"\n--- SCALES: {data.get('scales')}")
    print(f"\n--- STRUCTURE total_bars={report['info'].get('total_bars')} sum={report['info'].get('bars_sum')} ---")
    for s in data.get("structure_rhyme_map", {}).get("sections", []):
        print(f"  {s.get('label'):28s} {s.get('bars'):>3} bars  rhyme={s.get('rhyme_scheme'):<14} syl={s.get('syllables_per_line'):<10} job='{s.get('energy_note')}'")
    print(f"\n--- VALIDATION REPORT (after {repairs} repair(s)) ---")
    print(json.dumps(report, indent=2))

    ok = not report["errors"]
    return {"label": label, "ok": ok, "report": report, "data": data, "repairs": repairs}


async def main():
    if not EMERGENT_LLM_KEY:
        print("ERROR: EMERGENT_LLM_KEY not set")
        sys.exit(1)

    # Two cases: one friendly blend, one Oil & Water fusion
    test_cases = [
        (
            "dance-pop-summer",
            "A summery dance-pop song about reconnecting with a childhood friend at a beach bonfire. Female lead vocal, tempo around 122 BPM, 4/4 time. Tropical-house influence layered behind dance-pop. Wet mix. About 3 minutes long.",
        ),
        (
            "drift-phonk-classical-fusion",
            "Drift Phonk fused with Classical strings, late-night urban driving mood. Male baritone melodic-rap lead. Hip-hop beat, andante tempo. This is intentionally Oil & Water — opposing genres binding together. About 3:15.",
        ),
    ]

    results = []
    for label, concept in test_cases:
        try:
            r = await run_one(label, concept)
        except Exception as e:
            print(f"!! RUN {label} FAILED: {e}")
            r = {"label": label, "ok": False, "reason": str(e)}
        results.append(r)

    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in results:
        status = "OK ✅" if r.get("ok") else "FAIL ❌"
        errs = r.get("report", {}).get("errors", []) if r.get("report") else r.get("reason")
        print(f"{status:8s}  {r['label']:35s}  {errs}")

    passed = sum(1 for r in results if r.get("ok"))
    print(f"\n{passed}/{len(results)} runs passed all hard validations")
    sys.exit(0 if passed == len(results) else 2)


if __name__ == "__main__":
    asyncio.run(main())
