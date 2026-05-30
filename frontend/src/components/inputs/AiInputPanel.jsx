import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Sparkles, Loader2, Wand2 } from "lucide-react";
import { GEN } from "@/constants/testIds";

const examples = [
  "'90s trip-hop noir, brushed drums, vinyl hiss, female alto, smoky club vibe.",
  "Uplifting indie folk duet about a found family, stomp-clap percussion, 118 BPM.",
  "Minimal techno, 128 BPM, hypnotic bass, dry industrial mix, Berlin warehouse.",
  "Spaghetti-western showdown fused with sludge metal, doomy, male tenor, lento.",
];

const AiInputPanel = ({ concept, setConcept, onGenerate, onFillForm, busy, busyLabel, allowFillForm }) => {
  return (
    <Card className="border bg-card">
      <CardHeader className="flex flex-row items-start justify-between gap-3 space-y-0 pb-3">
        <div>
          <CardTitle className="text-sm font-semibold">Describe your song</CardTitle>
          <CardDescription className="text-xs mt-1">
            Natural language. Mention era, genre, tempo, mood, vocals, mix — the more specific, the better.
          </CardDescription>
        </div>
        <div className="flex items-center gap-2">
          {allowFillForm && (
            <Button
              variant="secondary"
              size="sm"
              onClick={onFillForm}
              disabled={busy || !concept?.trim()}
              className="h-9"
              data-testid={GEN.fillFormButton}
            >
              {busy === "fill" ? <Loader2 size={14} className="animate-spin" /> : <Wand2 size={14} />}
              <span className="ml-1.5 text-xs">Fill form</span>
            </Button>
          )}
          <Button
            size="sm"
            onClick={onGenerate}
            disabled={busy || !concept?.trim()}
            className="h-9"
            data-testid={GEN.generateButton}
          >
            {busy === "generate" ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
            <span className="ml-1.5 text-xs font-semibold">
              {busy === "generate" ? (busyLabel || "Generating…") : "Generate"}
            </span>
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Textarea
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          rows={6}
          placeholder="e.g. A late-night driving song fusing Drift Phonk and Romantic classical strings. Male baritone melodic rap, andante tempo, wet reverb on strings, dry punch on 808s. About 3:15."
          className="font-mono text-[13px] leading-6 bg-secondary/40"
          data-testid={GEN.conceptTextarea}
        />
        <div className="mt-3 flex flex-wrap gap-1.5">
          {examples.map((ex, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setConcept(ex)}
              className="text-[11px] font-mono px-2 py-1 rounded-md border border-border bg-secondary/40 hover:bg-secondary text-muted-foreground hover:text-foreground transition-colors"
              data-testid={`concept-example-${i}`}
            >
              {ex}
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default AiInputPanel;
