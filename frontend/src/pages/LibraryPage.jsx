import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Copy, ExternalLink, Trash2, Sparkles, Loader2 } from "lucide-react";
import { toast } from "sonner";
import sunoApi from "@/lib/api";
import { LIB } from "@/constants/testIds";

const LibraryPage = () => {
  const [items, setItems] = useState(null);
  const [busyId, setBusyId] = useState(null);
  const navigate = useNavigate();

  const fetchItems = async () => {
    try {
      const data = await sunoApi.library.list();
      setItems(data);
    } catch (e) {
      toast.error("Failed to load library");
      setItems([]);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const copyStyle = async (item) => {
    try {
      await navigator.clipboard.writeText(item.payload?.style_prompt || "");
      toast.success("Style Prompt copied");
    } catch (e) {
      toast.error("Copy failed");
    }
  };

  const remove = async (id) => {
    setBusyId(id);
    try {
      await sunoApi.library.delete(id);
      setItems((curr) => curr.filter((x) => x.id !== id));
      toast.success("Deleted");
    } catch (e) {
      toast.error("Delete failed");
    } finally {
      setBusyId(null);
    }
  };

  if (items === null) {
    return (
      <div className="py-16 flex items-center justify-center text-muted-foreground">
        <Loader2 className="animate-spin mr-2" size={16} /> Loading library…
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="py-16 text-center" data-testid={LIB.empty}>
        <h2 className="text-xl font-semibold mb-2">No saved generations yet</h2>
        <p className="text-sm text-muted-foreground mb-5">Generate a prompt and hit Save to build your library.</p>
        <Button onClick={() => navigate("/")}><Sparkles size={14} className="mr-1.5" /> Go to Generator</Button>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <header className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">Library</h1>
          <p className="text-sm text-muted-foreground mt-1">{items.length} saved generation{items.length === 1 ? "" : "s"}.</p>
        </div>
      </header>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((it) => {
          const sp = it.payload?.style_prompt || "";
          const preset = it.payload?.scales?.preset_name;
          const tempo = it.payload?.structure_rhyme_map?.italian_tempo;
          const bpm = it.payload?.structure_rhyme_map?.bpm;
          const date = new Date(it.created_at).toLocaleString();
          return (
            <Card key={it.id} className="border bg-card" data-testid={LIB.card(it.id)}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-semibold leading-tight line-clamp-1">{it.title}</CardTitle>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {preset && <Badge variant="outline" className="text-[10px] bg-primary/10 border-primary/40">{preset}</Badge>}
                  {tempo && <Badge variant="outline" className="text-[10px]">{tempo}{bpm ? ` · ${bpm} BPM` : ""}</Badge>}
                  <Badge variant="outline" className="text-[10px]">{it.mode || "ai"} mode</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="font-mono text-[12px] leading-5 text-muted-foreground bg-secondary/40 border rounded-md p-2.5 max-h-32 overflow-hidden whitespace-pre-wrap line-clamp-6">
                  {sp.slice(0, 360) || "(no style prompt)"}
                </div>
                <div className="flex items-center justify-between mt-3">
                  <span className="text-[11px] text-muted-foreground">{date}</span>
                  <div className="flex items-center gap-1">
                    <Button size="sm" variant="ghost" onClick={() => copyStyle(it)} data-testid={LIB.copy(it.id)}>
                      <Copy size={13} />
                    </Button>
                    <Button size="sm" variant="secondary" onClick={() => navigate(`/?load=${it.id}`)} data-testid={LIB.open(it.id)}>
                      <ExternalLink size={13} /> <span className="ml-1 text-xs">Open</span>
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => remove(it.id)} disabled={busyId === it.id} data-testid={LIB.delete(it.id)} aria-label="Delete">
                      {busyId === it.id ? <Loader2 className="animate-spin" size={13} /> : <Trash2 size={13} className="text-[hsl(var(--destructive))]" />}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default LibraryPage;
