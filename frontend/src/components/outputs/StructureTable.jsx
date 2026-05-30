import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const StructureTable = ({ srm }) => {
  if (!srm || !Array.isArray(srm.sections)) {
    return (
      <div className="text-sm text-muted-foreground italic">Generate to see the map.</div>
    );
  }
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2 text-xs">
        <Badge variant="outline">BPM {srm.bpm ?? "—"}</Badge>
        <Badge variant="outline">{srm.italian_tempo ?? "—"}</Badge>
        <Badge variant="outline">{srm.time_signature ?? "—"}</Badge>
        <Badge variant="outline">Total {srm.total_bars ?? "—"} bars</Badge>
        <Badge variant="outline">Strict {srm.strict_duration ?? "—"}</Badge>
        <Badge variant="outline" className="bg-[hsl(var(--chart-2)/0.14)] border-[hsl(var(--chart-2)/0.35)]">
          Practical {srm.practical_target ?? "—"}
        </Badge>
      </div>
      <div className="rounded-xl border overflow-hidden">
        <Table>
          <TableHeader className="bg-secondary/60">
            <TableRow>
              <TableHead className="text-xs font-semibold text-muted-foreground">Section</TableHead>
              <TableHead className="text-xs font-semibold text-muted-foreground text-right">Bars</TableHead>
              <TableHead className="text-xs font-semibold text-muted-foreground">Rhyme</TableHead>
              <TableHead className="text-xs font-semibold text-muted-foreground">Syllables</TableHead>
              <TableHead className="text-xs font-semibold text-muted-foreground">Energy / Job</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {srm.sections.map((s, i) => (
              <TableRow key={i} data-testid={`structure-rhyme-map-row-${i}`} className="hover:bg-secondary/30">
                <TableCell className="font-mono text-[13px]">{s.label}</TableCell>
                <TableCell className="font-mono text-[13px] tabular-nums text-right">{s.bars}</TableCell>
                <TableCell className="font-mono text-[12px]">{s.rhyme_scheme}</TableCell>
                <TableCell className="font-mono text-[12px]">{s.syllables_per_line}</TableCell>
                <TableCell className="text-sm text-muted-foreground">{s.energy_note}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default StructureTable;
