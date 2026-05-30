# plan.md — Suno AI Song Prompt Generator

## 1. Objectives
- Build an MVP web app that generates **high-quality Suno prompts** using embedded knowledge from the 5 provided documents.
- Support **Hybrid generation**: (1) Form → assembled outputs, (2) AI Mode (natural language → Claude), (3) AI fills the form.
- Output **all required artifacts**: **Style Prompt (≤1000 chars)**, **Exclude Styles**, **Lyrics w/ meta-tags**, **Recommended Weirdness/Style Influence**, **Structure & Rhyme Map** (bars, syllables, rhyme schemes).
- Enforce strict governance: **banned words list**, **bar-count vs BPM validation**, **syllable range validation**, and format compliance.
- Provide a **no-auth prompt library** (browser-based UX, persisted to MongoDB; optional local fallback).

---

## 2. Implementation Steps

### Phase 1 — Core LLM + Validation POC (isolation; do not proceed until solid)
**User stories**
1. As a user, I can paste a song concept and get all 5 outputs in one response.
2. As a user, I can see if any banned words were used and where.
3. As a user, I can verify the Style Prompt is ≤1000 characters.
4. As a user, I can see bar-math duration and whether it stays under 4:00.
5. As a user, I can see syllable-range validation warnings per section.

**Steps**
- Create a minimal Python script to call **Emergent LLM (Claude Sonnet 4.5)**.
- Build a **single “system prompt”** that embeds the essential taxonomies/rules:
  - Descriptive Prompt format
  - Meta-tag taxonomy + Basic Song Template structure
  - Mother Genres taxonomy (MusicMap)
  - Italian tempo markers list
  - Vocal ranges list
  - Common instrument models list
  - Scale-setting heuristics (50/50 etc.)
  - Section conventions (“by 2s”, compact section defaults)
  - Rhyme scheme guidance per section
  - Mix types (Raw/Wet/Dry/Parallel)
  - **Full banned list** + exception rule
- Define a **strict JSON output contract** from the LLM for reliability:
  - `style_prompt`, `exclude_styles`, `lyrics`, `scales`, `structure_rhyme_map`, `validation_notes`
- Implement a local validator module (Python) that checks:
  - Style prompt length ≤1000
  - Banned words presence (case-insensitive, near-match handling where feasible)
  - Bars sum, strict bar-math duration formula, practical target < 4:00
  - Syllable range checks per section (heuristic syllable counter)
- Iterate prompt + schema until:
  - JSON parses consistently
  - banned words are avoided
  - structure map is coherent and compact

**POC exit criteria**
- 10 consecutive runs produce valid JSON and pass validations (or produce explicit, actionable validation errors).

---

### Phase 2 — V1 App Development (FastAPI + React + MongoDB)
**User stories**
1. As a user, I can generate prompts via **AI Mode** (natural language) and copy each output block.
2. As a user, I can generate prompts via **Form Mode** and still get all outputs.
3. As a user, I can ask AI to **fill the form** from my concept, then edit fields before generating.
4. As a user, I can see validation errors (banned words, bar/BPM mismatch, syllable issues) and regenerate.
5. As a user, I can save a generated set to a **library** and reopen/copy later.

**Backend (FastAPI)**
- Endpoints:
  - `POST /api/generate` (AI mode): concept → LLM → JSON → validate → return
  - `POST /api/assemble` (form mode): structured fields → deterministic assembly + optional LLM polish → validate → return
  - `POST /api/fill-form` (AI helper): concept → structured form JSON
  - `POST /api/validate` (standalone): payload → validation report
  - `GET/POST/DELETE /api/library` (MongoDB CRUD; no auth)
- Services:
  - `llm_client` using Emergent universal key + Claude Sonnet 4.5
  - `prompt_assembler` (Descriptive Prompt formatter + Exclude formatter + section template generator)
  - `validators` (banned words, char limit, bar math, syllables)
- Data model (MongoDB): prompt sets with metadata (title, genre, bpm, created_at, outputs, validation status)

**Frontend (React + shadcn/ui)**
- Pages:
  - Generator: mode switch (AI / Form / Hybrid)
  - Library: saved prompt sets
- Generator UX:
  - AI Mode: textarea + “Generate”
  - Form Mode: fields for era/tempo/time sig/genre/subgenre/instruments/vocals/mood/mix + exclusions + structure prefs
  - Hybrid: “AI fill form” → editable form → generate
  - Output tabs/cards with copy buttons for each: Style / Exclude / Lyrics / Scales / Structure Map
  - Validation panel: errors vs warnings; highlight banned word matches
- Persistence:
  - Save to MongoDB
  - Optional localStorage cache for last 10 generations

**End of Phase 2: one E2E test round**
- Run through: AI Mode generate → validation → save → reopen → copy.
- Run through: AI fill form → adjust → assemble → save.

---

### Phase 3 — Quality, Workflows, and Reliability Enhancements
**User stories**
1. As a user, I can pick “Fusion difficulty” and get recommended workflow steps (Personas/Covers/Stems).
2. As a user, I can select “Oil & Water” blending and see the suggested 81/75 settings.
3. As a user, I can get “Exclude Styles” suggestions based on chosen genre/era.
4. As a user, I can generate multiple variants (x2/x4) and compare outputs.
5. As a user, I can export a prompt set as JSON/Markdown.

**Enhancements**
- Add a “Workflow Coach” panel (from Workflows doc):
  - iterative generation guidance + naming conventions + when to use stems/personas
- Add “Variant generation” (batch calls, rate-limited)
- Improve validators:
  - better syllable counting (hyphenation rules)
  - stronger near-match banned detection
  - rhyme-scheme sanity checks (section diversity)
- Add “Prompt linting” UI: flags generic tags, suggests instrument models/vocal ranges/Italian tempos.

**End of Phase 3: one E2E test round**
- Variants compare, export, and workflow coach correctness.

---

### Phase 4 — Optional next steps (post-v1)
- Auth (only if requested), shared libraries, persona templates, team workspaces.
- Advanced structure editor (drag-drop sections, auto bar-math recompute).

---

## 3. Next Actions (immediate)
1. Write the **POC system prompt + JSON schema** and the Python test harness for Claude Sonnet 4.5.
2. Implement validators (banned words, 1000-char, bar math, syllables) and iterate until stable.
3. Scaffold FastAPI + React app; wire `/api/generate` to the proven POC prompt.
4. Build Generator UI (AI/Form/Hybrid), outputs panel, validation panel.
5. Add MongoDB library CRUD + library UI.

---

## 4. Success Criteria
- **Core reliability**: LLM returns valid JSON in >95% of runs; app retries/repairs on schema failures.
- **Governance**: banned words are never present in final outputs (or are explicitly flagged with regeneration required).
- **Correctness**: Style Prompt always ≤1000 chars; bar-math duration computed and practical target <4:00.
- **Usability**: user can generate via AI or form in <60 seconds and copy/save outputs easily.
- **Stability**: E2E tests pass for generate → validate → save → reopen → export/copy flows.
