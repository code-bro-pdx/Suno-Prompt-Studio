import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

const Section = ({ title, children }) => (
  <div className="space-y-2">
    <div className="text-xs font-semibold tracking-wide uppercase text-muted-foreground">{title}</div>
    <div className="text-sm leading-6">{children}</div>
  </div>
);

const Pill = ({ children, tone = "default" }) => (
  <span
    className={`inline-flex items-center rounded-md border px-1.5 py-0.5 font-mono text-[11px] mr-1 mb-1 ${
      tone === "warn"
        ? "border-primary/40 bg-primary/10 text-foreground"
        : tone === "error"
        ? "border-destructive/40 bg-destructive/10 text-foreground"
        : "border-border bg-secondary/60 text-foreground"
    }`}
  >
    {children}
  </span>
);

const HelpDrawerContent = () => {
  return (
    <div className="py-6 space-y-6">
      <Section title="Quick rules">
        <ul className="list-disc pl-5 space-y-1.5">
          <li>Style Prompt must be ≤ 1000 characters.</li>
          <li>Total practical runtime stays under 4:00.</li>
          <li>Use Italian tempos (Allegro, Vivace…) in the Style Prompt instead of raw BPM.</li>
          <li>Use technical vocal ranges (Mezzo-Soprano A3–A5) instead of “high female”.</li>
          <li>Sandwich focus tags (Instrument, Vocals) around structure tags.</li>
        </ul>
      </Section>
      <Separator />
      <Section title="Scale presets (Weirdness / Style Influence)">
        <div className="grid gap-2">
          <div><Pill>50 / 50</Pill> Balanced first generation, exploration.</div>
          <div><Pill>70 / 75</Pill> Single-genre lock, tight control.</div>
          <div><Pill>60 / 70</Pill> Friendly genre blend (compatible subgenres).</div>
          <div><Pill tone="warn">81 / 75</Pill> Oil &amp; Water — forces opposing genres.</div>
          <div><Pill>75 / 50</Pill> Output is bland — add creative bandwidth.</div>
          <div><Pill>25 / 50</Pill> Hallucinating — tighten genre lane.</div>
          <div><Pill>50 / 70</Pill> Prompt being ignored — force adherence.</div>
        </div>
      </Section>
      <Separator />
      <Section title="By 2s structural defaults">
        <ul className="list-disc pl-5 space-y-1">
          <li>Intro 2–4, Verse 8, Pre-Chorus 2–4, Chorus 4–8.</li>
          <li>Post-Chorus 2–4 (8 only when it IS the instrumental hook).</li>
          <li>Bridge 4–8; Final Chorus 8 + optional 2–4 bar tag (never 16).</li>
          <li>16-bar sung verses only for rap/hip-hop/drill/trap.</li>
        </ul>
      </Section>
      <Separator />
      <Section title="Banned words — zero tolerance in lyrics">
        <div className="flex flex-wrap">
          {[
            "echo", "shadow", "whisper", "neon", "scars", "ashes",
            "fire and flame", "static", "coffee", "in-between",
          ].map((w) => (
            <Pill key={w} tone="error">
              {w}
            </Pill>
          ))}
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          A full list of ~150 additional cliches is enforced automatically. Banned
          words may only appear when required by a proper noun, title, or user-approved phrase.
        </p>
      </Section>
      <Separator />
      <Section title="Save → reuse">
        Every generation can be saved to the Library. Open a saved item to copy any field, or use it as a starting point for the next iteration.
      </Section>
    </div>
  );
};

export default HelpDrawerContent;
