import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { OUT } from "@/constants/testIds";

const ScalesCard = ({ scales }) => {
  if (!scales) {
    return (
      <Card className="border bg-card">
        <CardHeader>
          <CardTitle className="text-sm font-semibold">Recommended Scales</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground italic">
          Generate to receive Weirdness / Style Influence recommendations.
        </CardContent>
      </Card>
    );
  }
  return (
    <Card className="border bg-card">
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-3">
        <div>
          <CardTitle className="text-sm font-semibold">Recommended Scales</CardTitle>
          <p className="text-xs text-muted-foreground mt-1">Suno Weirdness and Style Influence settings.</p>
        </div>
        <Badge
          variant="outline"
          className="bg-secondary/50 border-primary/40 text-foreground"
          data-testid="scales-preset-badge"
        >
          {scales.preset_name}
        </Badge>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2" data-testid="scales-weirdness">
          <div className="flex items-center justify-between">
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Weirdness</div>
            <div className="font-mono text-sm tabular-nums">{scales.weirdness}</div>
          </div>
          <Slider
            value={[scales.weirdness]}
            min={0}
            max={100}
            step={1}
            data-testid="scales-weirdness-slider"
            disabled
          />
        </div>
        <div className="space-y-2" data-testid="scales-style-influence">
          <div className="flex items-center justify-between">
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Style Influence</div>
            <div className="font-mono text-sm tabular-nums">{scales.style_influence}</div>
          </div>
          <Slider
            value={[scales.style_influence]}
            min={0}
            max={100}
            step={1}
            data-testid="scales-style-influence-slider"
            disabled
          />
        </div>
        {scales.rationale && (
          <div className="rounded-lg border bg-secondary/40 p-3 text-sm leading-6">
            {scales.rationale}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ScalesCard;
