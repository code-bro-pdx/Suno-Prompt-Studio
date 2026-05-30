import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import OutputCard from "@/components/outputs/OutputCard";
import LyricsRenderer from "@/components/outputs/LyricsRenderer";
import StructureTable from "@/components/outputs/StructureTable";
import ScalesCard from "@/components/outputs/ScalesCard";
import { OUT } from "@/constants/testIds";

const CharCounter = ({ length, max = 1000 }) => {
  const tone =
    length > max ? "text-[hsl(var(--destructive))]" :
    length > 900 ? "text-[hsl(var(--primary))]" :
    "text-muted-foreground";
  return (
    <span className={`font-mono text-xs tabular-nums ${tone}`} data-testid={OUT.styleCharCounter}>
      {length}/{max}
    </span>
  );
};

const OutputsPanel = ({ payload, bannedWords }) => {
  if (!payload) {
    return (
      <div
        className="rounded-xl border bg-card p-10 text-center text-sm text-muted-foreground"
        data-testid={OUT.emptyState}
      >
        Generate to see results here.
      </div>
    );
  }
  const sp = payload.style_prompt || "";
  const ex = payload.exclude_styles || "";
  const lyrics = payload.lyrics || "";
  const scales = payload.scales || null;
  const srm = payload.structure_rhyme_map || null;
  const vocalNotes = payload.vocal_performance_notes || "";
  const workflow = payload.workflow_advice || "";
  const editorialExt = payload.editorial_extensions || [];
  const avoidances = payload.negative_avoidances || [];

  return (
    <div className="space-y-4">
      <div className="flex items-baseline justify-between gap-3">
        <div>
          <div className="text-lg font-semibold tracking-tight">{payload.title || "Untitled"}</div>
          {payload.concept_summary && (
            <p className="text-sm text-muted-foreground mt-0.5">{payload.concept_summary}</p>
          )}
        </div>
      </div>
      <Tabs defaultValue="style" data-testid={OUT.tabs}>
        <TabsList className="flex flex-wrap gap-1 bg-secondary/60 p-1 rounded-lg border w-full justify-start h-auto">
          <TabsTrigger value="style" data-testid={OUT.tabStyle} className="data-[state=active]:bg-background data-[state=active]:shadow-sm">Style Prompt</TabsTrigger>
          <TabsTrigger value="exclude" data-testid={OUT.tabExclude}>Exclude Styles</TabsTrigger>
          <TabsTrigger value="lyrics" data-testid={OUT.tabLyrics}>Lyrics</TabsTrigger>
          <TabsTrigger value="scales" data-testid={OUT.tabScales}>Scales</TabsTrigger>
          <TabsTrigger value="map" data-testid={OUT.tabMap}>Structure Map</TabsTrigger>
          <TabsTrigger value="notes">Notes</TabsTrigger>
        </TabsList>

        <TabsContent value="style" className="mt-3">
          <OutputCard
            outputKey="style-prompt"
            title="Style Prompt"
            description="Paste into Suno's Style field. Must stay under 1000 characters."
            content={sp}
            rightHeader={<CharCounter length={sp.length} />}
          />
        </TabsContent>

        <TabsContent value="exclude" className="mt-3">
          <OutputCard
            outputKey="exclude-styles"
            title="Exclude Styles"
            description="Paste into Suno's Exclude Styles field. Plain comma-separated terms (no 'No' prefixes)."
            content={ex}
          />
        </TabsContent>

        <TabsContent value="lyrics" className="mt-3">
          <OutputCard
            outputKey="lyrics"
            title="Lyrics with meta-tags"
            description="Paste directly into Suno's Lyrics field. Banned words are highlighted."
            content={lyrics}
            renderContent={() => <LyricsRenderer lyrics={lyrics} bannedWords={bannedWords} />}
            maxHeight="min(70vh, 640px)"
          />
        </TabsContent>

        <TabsContent value="scales" className="mt-3">
          <ScalesCard scales={scales} />
        </TabsContent>

        <TabsContent value="map" className="mt-3">
          <div className="rounded-xl border bg-card p-4 sm:p-5">
            <div className="text-sm font-semibold mb-3">Structure &amp; Rhyme Map</div>
            <StructureTable srm={srm} />
          </div>
        </TabsContent>

        <TabsContent value="notes" className="mt-3 space-y-4">
          {vocalNotes && (
            <OutputCard
              outputKey="vocal-notes"
              title="Vocal & Performance Notes"
              description="6–10 line specification for the lead vocal across the song."
              content={vocalNotes}
            />
          )}
          {(editorialExt.length > 0 || avoidances.length > 0) && (
            <div className="grid md:grid-cols-2 gap-4">
              {editorialExt.length > 0 && (
                <div className="rounded-xl border bg-card p-4">
                  <div className="text-sm font-semibold mb-2">Editorial extensions</div>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {editorialExt.map((x, i) => <li key={i}>{x}</li>)}
                  </ul>
                </div>
              )}
              {avoidances.length > 0 && (
                <div className="rounded-xl border bg-card p-4">
                  <div className="text-sm font-semibold mb-2">Negative avoidances</div>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {avoidances.map((x, i) => <li key={i}>{x}</li>)}
                  </ul>
                </div>
              )}
            </div>
          )}
          {workflow && (
            <div className="rounded-xl border bg-card p-4">
              <div className="text-sm font-semibold mb-2">Workflow advice</div>
              <p className="text-sm leading-6">{workflow}</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default OutputsPanel;
