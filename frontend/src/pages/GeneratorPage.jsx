import { useEffect, useMemo, useState } from "react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookmarkPlus, Loader2 } from "lucide-react";
import { toast } from "sonner";
import AiInputPanel from "@/components/inputs/AiInputPanel";
import FormInputPanel, { defaultForm } from "@/components/inputs/FormInputPanel";
import ValidationPanel from "@/components/outputs/ValidationPanel";
import OutputsPanel from "@/components/outputs/OutputsPanel";
import WorkflowCoach from "@/components/inputs/WorkflowCoach";
import sunoApi from "@/lib/api";
import { useKnowledge } from "@/hooks/useKnowledge";
import { GEN, MODE } from "@/constants/testIds";

const GeneratorPage = () => {
  const [mode, setMode] = useState("ai");
  const [concept, setConcept] = useState("");
  const [form, setForm] = useState(defaultForm());
  const [busy, setBusy] = useState(null); // 'generate' | 'fill' | 'assemble' | 'save'
  const [progress, setProgress] = useState(null); // {label, attempt, status}
  const [result, setResult] = useState(null); // {payload, validation, repairs}
  const { data: knowledge } = useKnowledge();

  const bannedWords = useMemo(() => knowledge?.banned_words || [], [knowledge]);

  const onJobProgress = (label) => (job, attempt) => {
    setProgress({ label, attempt, status: job.status });
  };

  const handleGenerate = async () => {
    if (!concept.trim()) return;
    setBusy("generate");
    setProgress({ label: "queued", attempt: 0, status: "queued" });
    try {
      const r = await sunoApi.generate(concept, true, { onProgress: onJobProgress("generating") });
      setResult(r);
      toast.success("Prompt generated");
    } catch (e) {
      const msg = e?.response?.data?.detail || e.message || "Generation failed";
      toast.error(msg);
    } finally {
      setBusy(null);
      setProgress(null);
    }
  };

  const handleFillForm = async () => {
    if (!concept.trim()) return;
    setBusy("fill");
    try {
      const r = await sunoApi.fillForm(concept);
      const merged = { ...defaultForm(), ...(r.form || {}) };
      setForm(merged);
      setMode("form");
      toast.success("Form pre-filled — edit and Assemble");
    } catch (e) {
      const msg = e?.response?.data?.detail || e.message || "Fill form failed";
      toast.error(msg);
    } finally {
      setBusy(null);
    }
  };

  const handleAssemble = async () => {
    setBusy("assemble");
    setProgress({ label: "queued", attempt: 0, status: "queued" });
    try {
      const r = await sunoApi.assemble(form, true, { onProgress: onJobProgress("assembling") });
      setResult(r);
      toast.success("Prompt assembled from form");
    } catch (e) {
      const msg = e?.response?.data?.detail || e.message || "Assemble failed";
      toast.error(msg);
    } finally {
      setBusy(null);
      setProgress(null);
    }
  };

  const handleSave = async () => {
    if (!result?.payload) return;
    setBusy("save");
    try {
      await sunoApi.library.create({
        title: result.payload.title || "Untitled",
        concept,
        mode,
        payload: result.payload,
        validation: result.validation,
      });
      toast.success("Saved to library");
    } catch (e) {
      toast.error("Save failed");
    } finally {
      setBusy(null);
    }
  };

  // If a library item was loaded via /?load=<id> handle it
  useEffect(() => {
    const url = new URL(window.location.href);
    const id = url.searchParams.get("load");
    if (!id) return;
    (async () => {
      try {
        const item = await sunoApi.library.get(id);
        setResult({ payload: item.payload, validation: item.validation || { errors: [], warnings: [], info: {} }, repairs: 0 });
        setConcept(item.concept || "");
        if (item.mode) setMode(item.mode);
        toast.success(`Loaded “${item.title}” from library`);
        url.searchParams.delete("load");
        window.history.replaceState({}, "", url.toString());
      } catch (e) {
        toast.error("Failed to load library item");
      }
    })();
  }, []);

  return (
    <div className="space-y-5">
      <header className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3">
        <div>
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">Suno Song Prompt Studio</h1>
          <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
            Architected from five reference guides. Generate validated Style Prompts, Exclude Styles,
            tagged lyrics, scale settings, and a section-by-section structure map — enforced.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Tabs value={mode} onValueChange={setMode} data-testid={MODE.tabs}>
            <TabsList className="rounded-full bg-secondary/70 p-1 border">
              <TabsTrigger value="ai" className="rounded-full px-3 py-1.5 text-xs data-[state=active]:bg-background data-[state=active]:shadow-sm" data-testid={MODE.ai}>AI Mode</TabsTrigger>
              <TabsTrigger value="form" className="rounded-full px-3 py-1.5 text-xs data-[state=active]:bg-background data-[state=active]:shadow-sm" data-testid={MODE.form}>Form Mode</TabsTrigger>
              <TabsTrigger value="hybrid" className="rounded-full px-3 py-1.5 text-xs data-[state=active]:bg-background data-[state=active]:shadow-sm" data-testid={MODE.hybrid}>Hybrid</TabsTrigger>
            </TabsList>
          </Tabs>
          <Button
            size="sm"
            variant="secondary"
            disabled={!result || busy === "save"}
            onClick={handleSave}
            className="h-9"
            data-testid={GEN.saveButton}
          >
            {busy === "save" ? <Loader2 size={14} className="animate-spin" /> : <BookmarkPlus size={14} />}
            <span className="ml-1.5 text-xs">Save to library</span>
          </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_320px] gap-5">
        <div className="space-y-4">
          {mode === "ai" && (
            <AiInputPanel
              concept={concept}
              setConcept={setConcept}
              onGenerate={handleGenerate}
              busy={busy}
              busyLabel={"Generating…"}
              allowFillForm={false}
            />
          )}
          {mode === "form" && (
            <FormInputPanel form={form} setForm={setForm} onSubmit={handleAssemble} busy={busy} />
          )}
          {mode === "hybrid" && (
            <>
              <AiInputPanel
                concept={concept}
                setConcept={setConcept}
                onGenerate={handleGenerate}
                onFillForm={handleFillForm}
                busy={busy}
                busyLabel={"Generating…"}
                allowFillForm
              />
              <FormInputPanel form={form} setForm={setForm} onSubmit={handleAssemble} busy={busy} />
            </>
          )}
          <ValidationPanel validation={result?.validation} />
        </div>

        <div className="min-w-0">
          {busy && (busy === "generate" || busy === "assemble") ? (
            <GenerationProgress progress={progress} mode={busy} />
          ) : !result ? (
            <EmptyOutput mode={mode} />
          ) : (
            <OutputsPanel payload={result.payload} bannedWords={bannedWords} />
          )}
        </div>

        <div className="hidden xl:block">
          <WorkflowCoach scales={result?.payload?.scales} mode={mode} />
        </div>
      </div>
    </div>
  );
};

const EmptyOutput = ({ mode }) => (
  <Card className="border bg-card" data-testid={GEN.emptyState}>
    <CardHeader>
      <CardTitle className="text-sm font-semibold">Your outputs will appear here</CardTitle>
    </CardHeader>
    <CardContent className="text-sm text-muted-foreground space-y-3">
      <p>
        Five validated artifacts ready to paste into Suno:
      </p>
      <ul className="list-disc pl-5 space-y-1">
        <li>Style Prompt (≤1000 chars)</li>
        <li>Exclude Styles</li>
        <li>Lyrics with meta-tags</li>
        <li>Recommended Weirdness / Style Influence</li>
        <li>Structure &amp; Rhyme Map (bars, syllables, rhyme schemes)</li>
      </ul>
      <p className="text-xs italic">
        Switch modes any time: {mode === "ai" ? "AI Mode active" : mode === "form" ? "Form Mode active" : "Hybrid Mode active"}.
      </p>
    </CardContent>
  </Card>
);

const GenerationProgress = ({ progress, mode }) => {
  const label = mode === "assemble" ? "Assembling from form" : "Generating prompt";
  const status = progress?.status || "queued";
  return (
    <Card className="border bg-card" data-testid="generation-progress-panel">
      <CardHeader>
        <CardTitle className="text-sm font-semibold flex items-center gap-2">
          <Loader2 size={14} className="animate-spin text-primary" />
          {label}…
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-sm text-muted-foreground">
        <p>
          Claude Sonnet 4.5 is composing your full Suno prompt set. This usually takes
          <span className="text-foreground"> 25–80 seconds </span>
          (longer if auto-repair runs once).
        </p>
        <ul className="space-y-1 text-xs font-mono">
          <li>• Drafting Style Prompt &amp; Exclude Styles</li>
          <li>• Writing lyrics with meta-tags</li>
          <li>• Mapping bars, rhymes, and syllables</li>
          <li>• Validating against banned-word list</li>
        </ul>
        <div className="flex items-center justify-between text-xs">
          <span>Status: <span className="font-mono text-foreground">{status}</span></span>
          <span>Poll #{progress?.attempt ?? 0}</span>
        </div>
      </CardContent>
    </Card>
  );
};


export default GeneratorPage;
