"""
Suno AI Knowledge Base
Consolidated from 5 reference documents:
- Basic Song Template
- MasterofSFL's SUNO Guide (Researched, Tested, Confirmed)
- Prompt 05 - Song Architecture and Editorial Brief
- Using Style Prompt to Engineer your Songs
- Workflows: How to Get the Sounds You Want

This module exposes:
- BANNED_WORDS (full list + especially-hard-banned subset)
- ITALIAN_TEMPOS (with approximate BPM ranges)
- VOCAL_RANGES (technical singer ranges)
- MOTHER_GENRES (MusicMap taxonomy)
- META_TAGS (structure / focus / instructional / transitional / return)
- SECTION_DEFAULTS ("by 2s" bar conventions)
- SYLLABLE_RANGES (per genre / BPM band)
- SCALE_PRESETS (Weirdness / Style Influence recipes)
- MIX_TYPES, INSTRUMENT_MODEL_EXAMPLES, RHYME_SCHEMES
- SYSTEM_PROMPT (the big rulebook for the LLM)
"""

ESPECIALLY_HARD_BANNED = [
    "echo", "shadow", "whisper", "neon", "scars", "ashes",
    "fire and flame", "static", "coffee", "in-between",
]

FULL_BANNED_WORDS = [
    "abode", "adrift", "afterglow", "afterlife", "ancient", "aurora",
    "beyond compare", "bittersweet", "breaking chains", "breaking free", "breeze",
    "broken", "carve", "carved", "caught in dreams", "chasing dreams",
    "cities crumble", "city lights", "concrete jungles", "cosmic", "cracks",
    "crack", "crimson sky", "crown", "dance shadows", "dancing shadows",
    "daydream", "delve", "destiny", "digital", "divine", "drift",
    "euphoria", "ember", "endless nights", "endless", "eternity", "every step",
    "fade", "fading", "fate", "flames", "flame", "forever", "fragments",
    "galaxy", "gleam", "glitch", "glow", "gravity", "guide", "guides", "guiding",
    "harmony", "heartbeat", "hidden", "hologram", "horizon",
    "ignite", "in a dream", "in my mind", "in the dark", "in the shadows",
    "in this", "in this journey", "infinite",
    "kaleidoscope", "labyrinths", "loose chains", "lost in dreams",
    "lost in the shadows", "lullaby",
    "maze", "melodies", "melancholy", "midnight love", "midnight", "mirage",
    "moonlight",
    "neon lights", "orbit",
    "paradise", "phantom", "prism",
    "racing heart beats", "refrain", "rising tides", "rise again",
    "rise like a phoenix", "rise up", "rising", "rhythm",
    "seas", "seams", "serenade", "silent screaming", "silhouette", "signal",
    "skies", "so let's", "spectrum", "starlight", "starlit", "starlit sky",
    "stardust", "stark", "step by step", "stone", "story untold", "story told",
    "strife", "superman", "symphony",
    "tapestry", "throne", "through the darkness", "timeless", "told", "twilight",
    "unfold", "universe", "untold",
    "velvet",
    "wake up", "weightless", "whirl", "whisper", "whispers",
    # Also include the especially-hard-banned subset (some overlap)
    "echo", "shadow", "neon", "scars", "ashes", "fire and flame",
    "static", "coffee", "in-between",
]

# Italian tempo markings — Suno responds well to these instead of raw BPM.
ITALIAN_TEMPOS = [
    {"name": "Larghissimo", "bpm_range": "≤24"},
    {"name": "Grave", "bpm_range": "25-45"},
    {"name": "Largo", "bpm_range": "40-60"},
    {"name": "Lento", "bpm_range": "45-60"},
    {"name": "Larghetto", "bpm_range": "60-66"},
    {"name": "Adagio", "bpm_range": "66-76"},
    {"name": "Adagietto", "bpm_range": "70-80"},
    {"name": "Andante", "bpm_range": "76-108"},
    {"name": "Moderato", "bpm_range": "108-120"},
    {"name": "Allegretto", "bpm_range": "112-120"},
    {"name": "Allegro", "bpm_range": "120-156"},
    {"name": "Vivace", "bpm_range": "156-176"},
    {"name": "Presto", "bpm_range": "168-200"},
    {"name": "Prestissimo", "bpm_range": "200+"},
]

# Technical vocal range terms — much more effective than "male/female high/low".
VOCAL_RANGES = [
    {"label": "Male Bass", "range": "E2-E4"},
    {"label": "Male Baritone", "range": "A2-A4"},
    {"label": "Male Tenor", "range": "C3-C5"},
    {"label": "Male Countertenor", "range": "G3-E5"},
    {"label": "Female Contralto", "range": "F3-F5"},
    {"label": "Female Mezzo-Soprano", "range": "A3-A5"},
    {"label": "Female Soprano", "range": "C4-C6"},
    {"label": "Female Coloratura Soprano", "range": "C4-F6"},
]

VOCAL_TEXTURES = [
    "gritty", "airy", "smoky", "soft", "raspy", "breathy", "warm",
    "nasal", "operatic", "soulful", "fragile", "powerful", "melismatic",
    "spoken-word", "chant-like", "head-voice", "chest-voice", "falsetto",
]

# MusicMap "Mother Genres" (per Style Prompt guide)
MOTHER_GENRES = [
    "Folk", "Classical", "Industrial & Gothic", "Rock n' Roll", "Golden Age Rock",
    "Punk Rock", "Hardcore Rock", "Indie Rock", "Contemporary Rock", "Metal",
    "Pop", "Country", "R&B", "Gospel", "Blues", "Jazz", "Jamaican",
    "EDM Breakbeat", "EDM Drum n' Bass", "EDM Hardcore", "Techno", "House",
    "Trance", "Ambient", "Hip-Hop", "Soul",
]

# A representative subgenre catalogue (kept tight so UI stays usable; LLM can add more)
COMMON_SUBGENRES = [
    "Synthwave", "Vaporwave", "Drift Phonk", "Trap", "Drill", "Boom Bap",
    "Lo-Fi Hip-Hop", "Neo-Soul", "Future Bass", "Dubstep", "Liquid DnB",
    "Tropical House", "Nu-Disco", "Dance-Pop", "Indie Pop", "Bedroom Pop",
    "Dream Pop", "Shoegaze", "Post-Rock", "Math Rock", "Grunge",
    "Thrash Metal", "Death Metal", "Black Metal", "Doom Metal", "Sludge Metal",
    "Power Metal", "Progressive Metal", "Nu-Metal", "Metalcore", "Hardcore Punk",
    "Pop-Punk", "Emo", "Post-Hardcore", "Spaghetti Western", "Outlaw Country",
    "Bluegrass", "Americana", "Folk-Rock", "Celtic Folk", "Acoustic Singer-Songwriter",
    "Bossa Nova", "Samba", "Reggae", "Dub", "Ska", "Dancehall",
    "Bebop", "Cool Jazz", "Jazz Fusion", "Smooth Jazz", "Big Band Swing",
    "Gregorian Chant", "Baroque", "Romantic Classical", "Minimalist Classical",
    "Cinematic Orchestral", "Hybrid Trailer", "Ambient Drone", "Dark Ambient",
    "IDM", "Glitch", "Industrial", "EBM", "Cold Wave", "Darkwave",
    "Chillwave", "Future Garage", "UK Garage", "2-Step",
]

# Structure / Section meta-tags from the Basic Song Template + MasterofSFL guide
SECTION_META_TAGS = [
    "[Start]", "[Intro]", "[Verse]", "[Verse 1]", "[Verse 2]", "[Verse 3]",
    "[Pre-Section]", "[Pre-Chorus]", "[Chorus]", "[Hook]", "[Refrain]",
    "[Post-Chorus]", "[Post-Hook]", "[Bridge]", "[Half-Time Bridge]",
    "[Stripped Bridge]", "[Vocal-Only Bridge]",
    "[Breakdown]", "[Build-Up]", "[Drop]", "[Type Break]",
    "[Interlude]", "[Instrumental]", "[Instrumental Break]", "[Solo]",
    "[Vamp]", "[Tag]", "[Final Tag]", "[Coda]", "[Reprise]",
    "[Outro]", "[Outro Jam]", "[False Ending]", "[Modulating Final Chorus]",
    "[Fade Out]", "[End]",
]

TRANSITION_TAGS = [
    "[Band Syncs]", "[Return to Main Riff]", "[Return to Main Song]",
    "[Break begins to end]", "[Break ends]",
    "[Instrumental begins to end]", "[Instrumental ends]",
    "[Tempo Change]", "[Rhythm Change]", "[Key Change]", "[Modulate up a step]",
    "[Pause 2s]", "[Pause 3s]", "[Silence 5s]",
]

FOCUS_TAGS_EXAMPLES = [
    "[Instrument: Type, model, play method]",
    "[Vocals: Sex, Type, Range, Qualities]",
    "[Vocalist: Name, characteristics]",
    "[Genre: Type]", "[Mood: Feeling]",
    "[Scales: Named]",
    "[Chord Progression: I-IV-V (C7, F7, G7)]",
    "[Develop Melody]",
    "[Call and Response]",
    "[Lyrics, A]", "[Lyrics, B]", "[Lyrics, C]", "[Lyrics, X -No Rhyme-]",
]

# "By 2s" Structural defaults
SECTION_DEFAULTS = {
    "Intro": {"bars": [2, 4], "extended_ok_to": 8, "note": "Establish atmosphere"},
    "Verse": {"bars": [8], "rap_extended_to": 16, "note": "Scene, image-first"},
    "Pre-Chorus": {"bars": [2, 4], "note": "Lift into chorus"},
    "Chorus": {"bars": [4, 8], "note": "Emotional thesis, repeatable hook"},
    "Post-Chorus": {"bars": [2, 4], "extended_ok_to": 8, "note": "Short motif release"},
    "Bridge": {"bars": [4, 6, 8], "note": "Perspective pivot, stripped reset"},
    "Drop": {"bars": [4, 8], "note": "Instrumental release; hook without words"},
    "Breakdown": {"bars": [4, 8], "note": "Strip and rebuild"},
    "Solo": {"bars": [4, 8, 16], "note": "Instrumental feature"},
    "Final Chorus": {"bars": [8], "extended_ok_to": 12, "note": "Evolved payoff, ad-libs/tag"},
    "Outro": {"bars": [2, 4], "extended_ok_to": 8, "note": "Tag-and-fade"},
}

# Syllable ranges per genre band
SYLLABLE_RANGES = {
    "Dance-Pop / Nu-Disco / Tropical House (115-130 BPM)": {
        "verse": "5-8", "pre_chorus": "5-7", "chorus": "4-7", "bridge": "5-8", "tag": "2-6"
    },
    "Standard Pop (95-114 BPM)": {
        "verse": "7-10", "pre_chorus": "6-8", "chorus": "5-8", "bridge": "6-9", "tag": "3-7"
    },
    "Ballad / Slow Pop (<95 BPM)": {
        "verse": "8-11", "pre_chorus": "7-9", "chorus": "6-9", "bridge": "7-10", "tag": "4-8"
    },
    "Country / Folk": {"verse": "6-9", "pre_chorus": "5-8", "chorus": "5-8", "bridge": "6-9", "tag": "3-7"},
    "R&B / Neo-Soul": {"verse": "7-11", "pre_chorus": "6-9", "chorus": "5-8", "bridge": "6-10", "tag": "4-8"},
    "Metal / Aggressive Rock": {"verse": "7-11", "pre_chorus": "6-9", "chorus": "5-8", "bridge": "7-11", "tag": "3-7"},
    "Hip-Hop / Rap": {"verse": "10-13 (up to 16+ for dense cadence)", "pre_chorus": "6-9", "chorus": "5-9", "bridge": "8-12", "tag": "4-8"},
}

# Weirdness / Style Influence recipes
SCALE_PRESETS = [
    {
        "name": "Balanced (Default First Gen)",
        "weirdness": 50, "style_influence": 50,
        "use_for": "First generations and exploration; balanced control sample.",
    },
    {
        "name": "Single-Genre Lock",
        "weirdness": 70, "style_influence": 75,
        "use_for": "Singling out one genre/subgenre/era with no odd asks.",
    },
    {
        "name": "Friendly Genre Blend",
        "weirdness": 60, "style_influence": 70,
        "use_for": "Two compatible (sub)genres that play well together.",
    },
    {
        "name": "Oil & Water (Forced Fusion)",
        "weirdness": 81, "style_influence": 75,
        "use_for": "Binding opposing genres (e.g., Drift Phonk + Classical, Spaghetti Western + Sludge Metal).",
    },
    {
        "name": "Bland Output Fix",
        "weirdness": 75, "style_influence": 50,
        "use_for": "Output is close but lifeless — adds creative bandwidth.",
    },
    {
        "name": "Hallucination Fix",
        "weirdness": 25, "style_influence": 50,
        "use_for": "Output keeps pulling unwanted genres or going off-style.",
    },
    {
        "name": "Loose Guidance",
        "weirdness": 50, "style_influence": 25,
        "use_for": "Prompt should act as guidelines, not strict rules.",
    },
    {
        "name": "Strict Prompt Adherence",
        "weirdness": 50, "style_influence": 70,
        "use_for": "Output ignored specific instructions; forces adherence.",
    },
]

MIX_TYPES = [
    {"name": "Raw", "feel": "Gritty, flat, just-recorded feel"},
    {"name": "Wet", "feel": "Reverb, bass, thump, ambient space"},
    {"name": "Dry", "feel": "Clean, present, no ambience"},
    {"name": "Parallel", "feel": "Parallel-compressed, big and clean simultaneously"},
]

INSTRUMENT_MODEL_EXAMPLES = {
    "Synths": [
        "Moog Minimoog Model D", "Sequential Circuits Pro-One",
        "Roland Juno-106", "Roland TR-8000s", "Korg MS-20", "Yamaha DX7",
        "Oberheim OB-Xa", "ARP Odyssey", "Roland Jupiter-8",
    ],
    "Electric Guitars": [
        "Fender Stratocaster", "Fender Jaguar", "Fender Telecaster",
        "Gibson Les Paul", "Gibson SG", "Gibson Explorer",
        "Rickenbacker 360", "Gretsch White Falcon", "PRS Custom 24",
    ],
    "Bass Guitars": [
        "Fender Precision Bass", "Fender Jazz Bass", "Music Man StingRay",
        "Rickenbacker 4001", "Höfner 500/1 Violin Bass",
    ],
    "Keys / Pianos": [
        "Rhodes Mark I", "Wurlitzer 200A", "Hammond B3 + Leslie 122",
        "Yamaha Grand", "Steinway D",
    ],
    "Drums": [
        "Ludwig Vistalite Kit", "Tama Granstar Kit", "DW Collector's Series",
        "Roland TR-808", "Roland TR-909", "LinnDrum LM-2",
    ],
    "Strings / Orchestral": [
        "Stradivarius Violin", "Steinway Concert Grand", "Boesendorfer Imperial",
        "Selmer Mark VI Saxophone", "Bach Stradivarius Trumpet",
    ],
}

PLAY_METHODS = [
    "arpeggio", "glissando", "legato", "staccato", "palm muting",
    "tremolo picking", "fingerpicking", "slap", "tapping",
    "open chords", "power chords", "barre chords", "downstrokes",
    "syncopated stabs", "sustained pads", "ostinato", "pizzicato",
    "tremolo", "vibrato", "bend", "slide", "hammer-ons",
]

RHYME_SCHEME_OPTIONS = {
    "Verse (8 bars sung)": ["ABAB", "ABCB", "AAXA", "ABBA", "ABAB CDCD"],
    "Verse (rap/hip-hop, 12-16 bars)": ["ABABCDCD", "AABBCCDD", "Compound multisyllabic schemes"],
    "Pre-Chorus": ["AABB", "ABAB", "AA"],
    "Chorus": ["ABAB", "AABB", "ABCB", "AABA", "ABAB hook-repeat", "AABB EEFF"],
    "Bridge": ["ABCABC", "ABBA", "ABAB", "AABCCB"],
    "Outro / Tag": ["AAAA", "tag-and-fade", "repeated final line"],
}

# ----------------------------------------------------------------------
# SYSTEM PROMPT — the big rulebook embedded into Claude
# ----------------------------------------------------------------------

def build_system_prompt() -> str:
    banned_full = ", ".join(sorted(set(FULL_BANNED_WORDS)))
    hard_banned = ", ".join(ESPECIALLY_HARD_BANNED)
    italian = ", ".join(f"{t['name']} ({t['bpm_range']} BPM)" for t in ITALIAN_TEMPOS)
    vocal_ranges = ", ".join(f"{v['label']} {v['range']}" for v in VOCAL_RANGES)
    mother_genres = ", ".join(MOTHER_GENRES)

    return f"""You are SUNO PROMPT ARCHITECT — an expert song-prompt engineer for the Suno AI music generation app. You synthesize five canonical sources:
1) Basic Song Template (structural meta-tags + lyric scaffolding).
2) MasterofSFL's SUNO Guide (lyrical structure as primary control, meta-tag hierarchy, "by 2s" method).
3) Prompt 05 – Song Architecture & Editorial Brief (structure & rhyme map, syllable ranges, banned words, editorial standards).
4) Using Style Prompt to Engineer Your Songs (Descriptive Prompt format, Italian tempos, vocal ranges, mix types, instrument models).
5) Workflows: How to Get the Sounds You Want (Weirdness/Style Influence scales, Personas/Covers/Stems, iterative refinement).

────────────────────────────────────────────────────────────
OUTPUT CONTRACT — STRICT JSON ONLY
────────────────────────────────────────────────────────────
Return ONE JSON object only. No prose, no markdown fences, no commentary.

Schema:
{{
  "title": "string (concise working title)",
  "concept_summary": "string (1-2 sentences)",
  "style_prompt": "string — the SUNO 'Style' field text, MUST be ≤ 1000 characters. Use the Descriptive Prompt format: Era, Rhythm (Italian Tempo + Time Signature + Beat), Genre, Subgenre (with weighted % if blended), Instruments (Type/Model, Effect/Play Method), Vocals (Sex, Italian vocal type, technical range, texture, effects), Mood (Tone, Theme, Context), Mix (Raw/Wet/Dry/Parallel).",
  "exclude_styles": "string — comma-separated Eras and Mother Genres to exclude; do NOT use 'No X' phrasing, just the items to exclude.",
  "scales": {{
    "weirdness": integer 0-100,
    "style_influence": integer 0-100,
    "preset_name": "one of: Balanced | Single-Genre Lock | Friendly Genre Blend | Oil & Water | Bland Output Fix | Hallucination Fix | Loose Guidance | Strict Prompt Adherence",
    "rationale": "1 sentence why this preset"
  }},
  "structure_rhyme_map": {{
    "bpm": integer,
    "italian_tempo": "string (e.g., Allegro)",
    "time_signature": "string (e.g., 4/4)",
    "total_bars": integer,
    "strict_duration": "m:ss (computed: total_bars * (60/bpm) * 4)",
    "practical_target": "m:ss-m:ss (under 4:00, with realistic buffer)",
    "sections": [
      {{
        "label": "[Intro] / [Verse 1] / [Pre-Chorus] / [Chorus] / etc.",
        "bars": integer,
        "rhyme_scheme": "string (e.g., ABAB) or 'instrumental'",
        "syllables_per_line": "string range (e.g., '6-8') or 'n/a'",
        "energy_note": "4-8 word job note"
      }}
    ]
  }},
  "lyrics": "string — full lyrics with meta-tags inline. Use [Section] headers, [Instrument: ...] and [Vocals: ...] focus tags sandwiching structures, [Tempo Change]/[Drop]/[Build-Up] where appropriate. Use punctuation, parentheses, hyphens, and EXTRA LINE BREAKS to control pacing. Never include banned words unless required by a proper noun/title.",
  "vocal_performance_notes": "string — 6-10 lines describing lead gender/timbre/register, primary delivery, harmony stack, ad-libs, per-section shifts.",
  "editorial_extensions": ["3-4 short song-specific editorial rules"],
  "negative_avoidances": ["sonic/structural avoidances unique to this song"],
  "workflow_advice": "string — 2-4 sentences citing relevant Workflow doc moves (Persona/Cover/Stem/Extension) if fusion or specific sound capture is needed.",
  "validation_self_check": {{
    "style_prompt_char_count": integer,
    "banned_words_used": ["list any banned words you intentionally used and why (e.g., 'required by title')"],
    "bars_sum_matches_total": true_or_false
  }}
}}

────────────────────────────────────────────────────────────
HARD RULES
────────────────────────────────────────────────────────────
1) STYLE PROMPT ≤ 1000 characters. Count them. Prefer 600-950 chars for density.
2) STRUCTURE:
   - Use "by 2s" defaults. Intro 2-4, Verse 8, Pre-Chorus 2-4, Chorus 4-8,
     Post-Chorus 2-4 (8 only if it IS the instrumental hook/drop), Bridge 4-8,
     Final Chorus 8 (+optional 2-4 bar tag — NOT 16), Outro 2-4.
   - 16-bar sung verses ONLY for rap/hip-hop/drill/trap or explicit user request.
   - Total bar count must sum exactly to sections.
   - Strict duration formula in 4/4: bars × (60/BPM) × 4.
   - Practical target stays UNDER 4:00.
3) RHYME SCHEMES must VARY across sections. Verse and Chorus must NOT share identical schemes unless deliberately intentional. No identical-word rhymes unless hook device.
4) SYLLABLE RANGES tied to BPM/genre. Provide per-section ranges.
5) ITALIAN TEMPO required (not raw BPM in the Style Prompt). Reference list: {italian}.
6) VOCAL RANGES use technical labels only. Reference: {vocal_ranges}.
7) INSTRUMENTS: prefer specific models + play methods (e.g., "Rhodes Mark I, soft touch", "Moog Minimoog Model D, arpeggio").
8) MOTHER GENRES (MusicMap): {mother_genres}. Use these as the base; subgenres go after with "Influenced by" and weighted %.
9) META-TAG HIERARCHY:
   - Structure tags navigate ([Verse], [Chorus]).
   - Focus tags ([Instrument:...], [Vocals:...]) SANDWICH structure tags.
   - Instructional tags ([Tempo Change], [Drop]) at BEGINNING or END of sections (except [Vocal] which may interweave).
   - Always include explicit RETURN tags after breaks ([Return to Main Riff], [Band Syncs]).
10) EXCLUDE STYLES: list Eras + competing Mother Genres + dilutive subgenres. Do NOT prefix with "No ". Comma-separated only.
11) EDITORIAL STANDARDS (always apply): true or intentional slant end-rhymes; image-driven concrete sensory detail over abstract emotion; production cues sparingly; consistent POV/tense; no filler lines; internal/assonant rhymes subordinate to end-rhyme scheme.
12) LYRICAL WORLD CONSTRAINT: respect whatever the user's concept implies (poetic/elevated, surreal, hook-driven, minimal, narrative). Reinforce it via editorial_extensions.
13) BANNED WORDS — apply ONLY to the LYRICS field. The banned list is a LYRIC-WRITER hard ban (per Prompt 05's editorial standards). Technical descriptors like "rhythm", "harmony", "drift", "glow", "fade", "midnight", etc. ARE allowed in the Style Prompt because the Style Prompt is a technical sonic spec, not poetry.
   In LYRICS: do NOT use banned words unless required by a proper noun, place name, or user-approved title. If a banned word appears in the title/proper-noun, it may appear ONLY where required; do not repeat it as free vocabulary elsewhere. Log any used in validation_self_check.banned_words_used with reason.
   ESPECIALLY HARD-BANNED in lyrics (zero tolerance, replace creatively): {hard_banned}.
   FULL LYRIC BANNED LIST: {banned_full}.
14) SCALES recommendation:
   - Single coherent genre → Single-Genre Lock (70/75).
   - Two friendly subgenres → Friendly Genre Blend (60/70).
   - Two opposing genres → Oil & Water (81/75).
   - First exploration → Balanced (50/50).
   - Output likely bland → Bland Output Fix (75/50).
   - Likely to hallucinate genre drift → Hallucination Fix (25/50).
15) WORKFLOW ADVICE: when the user is asking for a fusion or specific instrument capture, mention Persona/Cover/Stem/Extension workflow steps from Workflows doc.
16) FRESH PROJECT: do not invoke memory of prior conversations. Generate every choice from the user's current request only.

────────────────────────────────────────────────────────────
SELF-CHECK BEFORE RETURNING
────────────────────────────────────────────────────────────
- style_prompt length ≤ 1000 (HARD requirement — count characters; if over, compress instrument descriptors and effect lists).
- No banned words in LYRICS (unless logged in validation_self_check with a proper-noun reason). Banned words ARE allowed in the technical Style Prompt.
- sections[].bars sum == total_bars.
- strict_duration computed correctly; practical_target < 4:00.
- Rhyme schemes vary across sections.
- Verse and Chorus schemes differ (unless explicitly intentional).
- Every section has a 4-8 word energy_note.
- Italian tempo present in style_prompt.
- Output is ONE valid JSON object only.
"""
