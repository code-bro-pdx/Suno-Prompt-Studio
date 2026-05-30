# plan.md — Suno AI Song Prompt Generator (Updated)

## 1. Objectives
- Deliver a production-ready MVP web app that generates **high-quality Suno prompts** using embedded knowledge from the 5 provided documents.
- Support **Hybrid generation**:
  1) **AI Mode** (natural language → Claude Sonnet 4.5),
  2) **Form Mode** (structured fields → Claude-assembled output),
  3) **Hybrid** (AI fills the form → user edits → assemble).
- Output **all required artifacts** in one generation:
  - **Style Prompt** (≤1000 chars)
  - **Exclude Styles**
  - **Lyrics w/ meta-tags** (with focus/instruction/transition tag conventions)
  - **Recommended Weirdness / Style Influence** (preset + values)
  - **Structure & Rhyme Map** (bars, syllables, rhyme schemes, duration math)
- Enforce strict governance:
  - **Banned words list enforced for Lyrics** (per Prompt 05 editorial constraints)
  - **Bar-count sum + bar/BPM duration validation**, practical target under 4:00
  - Rhyme/energy-note sanity warnings (where applicable)
- Provide a **no-auth prompt library** (MongoDB persistence) with reopen/copy flows.
- Ensure reliability under platform constraints by using an **async job pattern** for long-running generations:
  - `POST /api/generate` / `POST /api/assemble` return **job_id immediately**
  - Client polls `GET /api/jobs/{id}` until `done` or `error`

**Current status:** Objectives for MVP are met; core functionality shipped and validated end-to-end.

---

## 2. Implementation Steps

### Phase 1 — Core LLM + Validation POC (COMPLETED)
**User stories (completed)**
1. As a user, I can paste a song concept and get all 5 outputs in one response.
2. As a user, I can see if banned words were used and where.
3. As a user, I can verify the Style Prompt is ≤1000 characters.
4. As a user, I can see bar-math duration and whether it stays under 4:00.
5. As a user, I can see syllable-range guidance per section.

**What was built**
- A consolidated **system prompt / rulebook** embedding:
  - Descriptive Prompt format, meta-tag hierarchy, “by 2s” section defaults
  - Mother genres + subgenre blending, Italian tempos, technical vocal ranges
  - Instrument model examples, mix types
  - Scale-setting heuristics / presets
  - Prompt 05 editorial requirements + banned word list enforcement (lyrics)
- **Strict JSON output contract** from the LLM.
- Python harness + validators to verify:
  - Style prompt char limit
  - Lyrics banned words detection
  - Bars sum == total, strict duration math, practical target < 4:00
  - Rhyme scheme variety warnings
  - Energy note length warnings
- **Auto-repair** pattern: if validation errors occur, the model is prompted once to correct them.

**POC exit criteria (met)**
- Consistent JSON parsing and validation success with repair loop.

---

### Phase 2 — V1 App Development (FastAPI + React + MongoDB) (COMPLETED)
**User stories (completed)**
1. Generate prompts via **AI Mode** and copy each output block.
2. Generate prompts via **Form Mode** and get all outputs.
3. **AI fills the form** from concept, user edits, then assemble.
4. See validation errors/warnings and iterate.
5. Save generations to a **library** and reopen/copy later.

**Backend (FastAPI) — implemented**
- Knowledge endpoint:
  - `GET /api/knowledge` returns taxonomies and lists for UI (genres, tempos, vocal ranges, presets, tags, banned words).
- Async generation endpoints (to avoid 60s ingress timeouts):
  - `POST /api/generate` → `{ job_id }` (AI Mode)
  - `POST /api/assemble` → `{ job_id }` (Form Mode)
  - `GET /api/jobs/{id}` → `{ status, result | error }`
- Hybrid helper:
  - `POST /api/fill-form` → structured form payload
- Validation:
  - `POST /api/validate` → structured report `{ errors, warnings, info }`
- Library CRUD (no auth):
  - `POST /api/library`, `GET /api/library`, `GET /api/library/{id}`, `DELETE /api/library/{id}`

**Key services / modules — implemented**
- `llm_service.py`: Claude Sonnet 4.5 via emergentintegrations, JSON extraction, repair prompt.
- `validators.py`: char-limit, lyrics banned words, bar math, duration thresholds, rhyme/energy note warnings.
- `jobs.py`: MongoDB-backed job queue (`queued|running|done|error`) + background scheduling.
- `suno_knowledge.py`: consolidated knowledge base (taxonomies, presets, system rules).

**Frontend (React + shadcn/ui) — implemented**
- Pages:
  - **Generator**: three modes (AI/Form/Hybrid)
  - **Library**: saved prompt sets with open/copy/delete
- Generator UX:
  - AI Mode: concept textarea + examples + Generate
  - Form Mode: structured fields (era, tempo, genre blend, instruments, vocals, mix, structure, exclusions)
  - Hybrid: AI concept + “Fill form” + editable form + Assemble
  - Outputs: tabbed panel for Style/Exclude/Lyrics/Scales/Map (+ Notes)
  - Validation panel: errors/warnings + stats (style chars, bar sum, strict duration, banned count)
  - Lyrics renderer highlights tags and banned words inline
  - Workflow Coach panel: contextual tips based on scale preset
  - GenerationProgress panel: visible while polling async jobs

**E2E test status**
- Testing agent report: **98.5% overall pass rate**, **zero critical bugs**, **zero frontend issues**.
- Core issue found in iteration 1 (k8s ingress 60s timeout) resolved via async job pattern.

---

### Phase 3 — Quality, Workflows, and Reliability Enhancements (OPTIONAL / NEXT)
**User stories (proposed)**
1. As a user, I can generate **multiple variants** (x2/x4) and compare outputs side-by-side.
2. As a user, I can export a generation as:
   - `.txt` blocks for Suno fields
   - `.md` bundle
   - JSON download
3. As a user, I can maintain **multi-revision history** per song concept (iterations, notes, deltas).
4. As a user, I can create/share **public links** (read-only) to a saved generation.
5. As a user, I can simulate advanced workflows (Persona/Cover/Stems) as guided steps.

**Enhancements (recommended)**
- Variant generation:
  - batch job creation + rate-limiting; compare UI (diffs in style prompt/lyrics/map)
- Export tooling:
  - “Export bundle” button producing a single package with all artifacts
- Library upgrades:
  - group items by “Song Project” with revision timeline
  - tags/filters/search (genre, tempo, scale preset)
- Validation upgrades:
  - optional softer banning (flag vs block), configurable per user
  - improved syllable counting heuristics
  - stronger rhyme diversity checks and section rules enforcement

**End of Phase 3: one E2E test round**
- Variants compare, exports, revision history, link-sharing.

---

### Phase 4 — Optional next steps (post-v1)
- Authentication (if needed), team workspaces, shared libraries.
- Advanced structure editor:
  - drag-and-drop section ordering
  - auto bar-math recompute and duration preview
  - “by 2s” guardrails + overrides
- Persona/Stem workflow simulator:
  - step-by-step wizard for Persona creation from stems, cover iteration recipes

---

## 3. Next Actions (immediate)
1. (Optional) Decide which Phase 3 upgrades to prioritize first:
   - variants/compare, export bundles, revision history, share links.
2. Add small UX improvements:
   - job ETA estimate (based on average completion time)
   - “Cancel job” endpoint + UI affordance (if desired)
3. Add library ergonomics:
   - search + filters, pin favorites, tags.

---

## 4. Success Criteria
**MVP (achieved)**
- **Core reliability**: JSON schema adherence with auto-repair; async jobs avoid gateway timeouts.
- **Governance**: lyrics banned words flagged/avoided; validation visible and actionable.
- **Correctness**: Style Prompt ≤1000 chars; bar-math computed; practical target under 4:00.
- **Usability**: AI/Form/Hybrid modes, copy buttons, save/reopen flow, and clear progress UI.
- **Stability**: E2E tests pass across generator + library flows.

**Phase 3+ goals**
- Faster iteration loops (variants/compare), better project organization (revision history), and improved portability (exports/share links).