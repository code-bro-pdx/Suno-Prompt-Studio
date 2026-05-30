import { useMemo } from "react";
import { VAL } from "@/constants/testIds";

const SECTION_TAG = /\[(Start|Intro|Verse(?:\s*\d+)?|Pre-Chorus|Chorus|Hook|Refrain|Post-Chorus|Post-Hook|Bridge|Half-Time Bridge|Stripped Bridge|Vocal-Only Bridge|Breakdown|Build-Up|Drop|Type Break|Interlude|Instrumental(?:\s*Break)?|Solo|Vamp|Tag|Final Tag|Coda|Reprise|Outro|Outro Jam|False Ending|Modulating Final Chorus|Fade Out|End)\]/i;
const FOCUS_TAG = /\[(Instrument|Vocals?|Vocalist|Genre|Mood|Scales?|Chord Progression|Develop Melody|Call and Response|Lyrics)[^\]]*\]/i;
const INSTR_TAG = /\[(Tempo Change|Rhythm Change|Key Change|Modulate[^\]]*|Band Syncs|Return[^\]]*|Break[^\]]*|Instrumental[^\]]*|Pause[^\]]*|Silence[^\]]*|Build[^\]]*|Drop[^\]]*)\]/i;
const ANY_TAG = /\[[^\]]+\]/;

const tokenise = (line) => {
  const tokens = [];
  let remaining = line;
  while (remaining.length) {
    const m = remaining.match(ANY_TAG);
    if (!m) {
      tokens.push({ type: "text", value: remaining });
      break;
    }
    const idx = m.index;
    if (idx > 0) tokens.push({ type: "text", value: remaining.slice(0, idx) });
    let tag = m[0];
    let type = "focus";
    if (SECTION_TAG.test(tag)) type = "section";
    else if (INSTR_TAG.test(tag)) type = "instr";
    else if (FOCUS_TAG.test(tag)) type = "focus";
    tokens.push({ type, value: tag });
    remaining = remaining.slice(idx + tag.length);
  }
  return tokens;
};

const tagClass = (t) => {
  if (t === "section")
    return "inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[11px] mr-1 bg-primary/15 border-primary/40 text-foreground";
  if (t === "instr")
    return "inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[11px] mr-1 bg-[hsl(var(--chart-2)/0.18)] border-[hsl(var(--chart-2)/0.40)] text-foreground";
  return "inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[11px] mr-1 bg-secondary/70 border-border text-foreground";
};

const makeBannedRegex = (words) => {
  if (!words || !words.length) return null;
  const escaped = words.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  // Word-boundary fallback covers most single-word cases; multi-word phrases included as-is.
  return new RegExp(`(?<![A-Za-z])(${escaped.join("|")})(?![A-Za-z])`, "gi");
};

const highlightBanned = (text, regex) => {
  if (!regex || !text) return [{ type: "text", value: text }];
  const out = [];
  let last = 0;
  let m;
  regex.lastIndex = 0;
  while ((m = regex.exec(text)) !== null) {
    if (m.index > last) out.push({ type: "text", value: text.slice(last, m.index) });
    out.push({ type: "banned", value: m[0] });
    last = m.index + m[0].length;
    if (m.index === regex.lastIndex) regex.lastIndex++;
  }
  if (last < text.length) out.push({ type: "text", value: text.slice(last) });
  return out;
};

const LyricsRenderer = ({ lyrics, bannedWords }) => {
  const regex = useMemo(() => makeBannedRegex(bannedWords), [bannedWords]);

  const lines = (lyrics || "").split(/\r?\n/);
  return (
    <div>
      {lines.map((line, i) => {
        if (!line.trim()) {
          return <div key={i} className="h-4" />;
        }
        const tokens = tokenise(line);
        return (
          <div key={i} className="min-h-[24px]">
            {tokens.map((t, j) => {
              if (t.type === "text") {
                const parts = highlightBanned(t.value, regex);
                return (
                  <span key={j}>
                    {parts.map((p, k) =>
                      p.type === "banned" ? (
                        <span
                          key={k}
                          className="px-1 rounded-sm bg-[hsl(var(--destructive)/0.18)] text-foreground underline decoration-[hsl(var(--destructive))] decoration-2 underline-offset-2"
                          data-testid={VAL.bannedHighlight}
                          title="Banned word per editorial rules"
                        >
                          {p.value}
                        </span>
                      ) : (
                        <span key={k}>{p.value}</span>
                      )
                    )}
                  </span>
                );
              }
              return (
                <span key={j} className={tagClass(t.type)}>
                  {t.value}
                </span>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

export default LyricsRenderer;
