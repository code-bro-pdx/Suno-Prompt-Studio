import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CircleX, TriangleAlert, Info } from "lucide-react";
import { VAL } from "@/constants/testIds";

const Row = ({ tone, text }) => (
  <li
    className={`flex items-start gap-2 rounded-lg border bg-card p-2.5 ${
      tone === "error"
        ? "border-l-4 border-l-[hsl(var(--destructive))]"
        : tone === "warn"
        ? "border-l-4 border-l-[hsl(var(--primary))]"
        : "border-l-4 border-l-[hsl(var(--chart-2))]"
    }`}
  >
    <span className={"mt-0.5 " + (tone === "error" ? "text-[hsl(var(--destructive))]" : tone === "warn" ? "text-[hsl(var(--primary))]" : "text-[hsl(var(--chart-2))]")}>
      {tone === "error" ? <CircleX size={14} /> : tone === "warn" ? <TriangleAlert size={14} /> : <Info size={14} />}
    </span>
    <span className="text-sm leading-5">{text}</span>
  </li>
);

const ValidationPanel = ({ validation }) => {
  if (!validation) return null;
  const { errors = [], warnings = [], info = {} } = validation;
  const ok = errors.length === 0 && warnings.length === 0;
  return (
    <Card className="border bg-card" data-testid={VAL.panel}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
        <CardTitle className="text-sm font-semibold">Validation</CardTitle>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="bg-[hsl(var(--destructive)/0.15)] text-[hsl(var(--destructive))] border-[hsl(var(--destructive)/0.40)]">
            {errors.length} errors
          </Badge>
          <Badge variant="outline" className="bg-[hsl(var(--primary)/0.12)] text-foreground border-[hsl(var(--primary)/0.40)]">
            {warnings.length} warnings
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {ok && (
          <div className="rounded-lg border border-[hsl(var(--chart-3)/0.45)] bg-[hsl(var(--chart-3)/0.10)] text-sm p-3">
            All hard checks passed. Ready to copy or save.
          </div>
        )}
        {errors.length > 0 && (
          <ul className="space-y-2" data-testid={VAL.errors}>
            {errors.map((e, i) => (
              <Row key={`e${i}`} tone="error" text={e.message || e.code} />
            ))}
          </ul>
        )}
        {warnings.length > 0 && (
          <ul className="space-y-2" data-testid={VAL.warnings}>
            {warnings.map((w, i) => (
              <Row key={`w${i}`} tone="warn" text={w.message || w.code} />
            ))}
          </ul>
        )}
        <div
          className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1"
          data-testid={VAL.barMath}
        >
          <Stat label="Style chars" value={info.style_prompt_char_count ?? "—"} accent={info.style_prompt_char_count > 1000 ? "error" : info.style_prompt_char_count > 950 ? "warn" : "ok"} />
          <Stat label="Bars sum" value={`${info.bars_sum ?? "—"} / ${info.total_bars ?? "—"}`} accent={info.bars_sum && info.total_bars && info.bars_sum === info.total_bars ? "ok" : info.total_bars ? "error" : "muted"} />
          <Stat label="Strict duration" value={info.computed_strict_duration ?? "—"} accent="ok" />
          <Stat label="Banned in lyrics" value={(info.banned_words_in_lyrics?.length ?? 0).toString()} accent={(info.banned_words_in_lyrics?.length || 0) ? "error" : "ok"} />
        </div>
      </CardContent>
    </Card>
  );
};

const Stat = ({ label, value, accent }) => (
  <div className={`rounded-lg border bg-secondary/40 p-2.5 ${accent === "error" ? "border-[hsl(var(--destructive)/0.40)]" : accent === "warn" ? "border-[hsl(var(--primary)/0.40)]" : ""}`}>
    <div className="text-[11px] uppercase tracking-wide text-muted-foreground">{label}</div>
    <div className="font-mono text-sm tabular-nums mt-0.5">{value}</div>
  </div>
);

export default ValidationPanel;
