import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles, Drum, Library as LibIcon } from "lucide-react";

const tipsByPreset = {
  "Oil & Water (Forced Fusion)": [
    "Generate one genre strong first, then convert via Cover or Persona.",
    "Pull stems from the strong genre; turn them into a Persona to re-implant on the second genre.",
    "Keep Style Influence high so the AI honours your blend description.",
  ],
  "Single-Genre Lock": [
    "Tight, recognisable genre execution. Use specific instrument models.",
    "Exclude adjacent eras and competing Mother Genres aggressively.",
  ],
  "Friendly Genre Blend": [
    "Use weighted percentages, e.g. Pop 65% / Tropical House 35%.",
    "Keep Weirdness moderate to preserve cohesion.",
  ],
  "Balanced (Default First Gen)": [
    "Ideal first generation; analyse the output and tune one scale at a time.",
    "Change only Weirdness or Style Influence (not both) between iterations.",
  ],
  "Bland Output Fix": [
    "If the result feels generic, push Weirdness up (try 75).",
    "Inject a more specific instrument model or vocal range to differentiate.",
  ],
  "Hallucination Fix": [
    "Drop Weirdness to 25. Tighten the Exclude Styles list.",
    "Add explicit RETURN tags ([Band Syncs], [Return to Main Riff]).",
  ],
};

const defaultTips = [
  "Generate, then change ONE setting at a time — Weirdness OR Style Influence.",
  "Use Personas for reusable instrument or vocal characters.",
  "Stems unlock isolation; create a Persona from a stem to lock a unique sound.",
];

const WorkflowCoach = ({ scales, mode }) => {
  const presetName = scales?.preset_name;
  const tips = (presetName && tipsByPreset[presetName]) || defaultTips;

  return (
    <Card className="border bg-card" data-testid="workflow-coach-panel">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
        <CardTitle className="text-sm font-semibold flex items-center gap-2">
          <Sparkles size={15} className="text-primary" />
          Workflow Coach
        </CardTitle>
        <Badge variant="outline" className="text-[11px]">{mode.toUpperCase()} mode</Badge>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="text-xs uppercase tracking-wide text-muted-foreground mb-2">
            {presetName ? `For “${presetName}”` : "Suggested moves"}
          </div>
          <ul className="space-y-2">
            {tips.map((t, i) => (
              <li key={i} className="flex items-start gap-2 text-sm leading-6">
                <span className="mt-1.5 inline-block h-1.5 w-1.5 rounded-full bg-primary shrink-0" />
                <span>{t}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border bg-secondary/40 p-3 text-xs leading-6">
          <div className="flex items-center gap-2 mb-1 text-foreground/90">
            <Drum size={13} /> Quick references
          </div>
          <ul className="space-y-1 pl-5 list-disc">
            <li>Italian tempos beat raw BPM in the Style Prompt.</li>
            <li>Technical vocal ranges (Tenor C3–C5) beat “high male”.</li>
            <li>Specific instrument models (Moog Minimoog Model D) beat “synth”.</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};

export default WorkflowCoach;
