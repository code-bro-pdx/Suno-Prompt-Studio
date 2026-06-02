import { useEffect, useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sparkles, Loader2, Plus, X } from "lucide-react";
import { GEN } from "@/constants/testIds";
import { useKnowledge } from "@/hooks/useKnowledge";

const defaultForm = () => ({
  title: "",
  era: "2020s",
  bpm: 120,
  italian_tempo: "Allegro",
  time_signature: "4/4",
  mother_genre: "Pop",
  subgenres: [{ name: "Dance-Pop", weight_percent: 70 }, { name: "Tropical House", weight_percent: 30 }],
  mood: "Bright, nostalgic, summery",
  instruments: [{ type: "Synth", model: "Roland Juno-106", play_method: "sustained pads" }],
  vocal_gender: "Female",
  vocal_range: "Female Mezzo-Soprano A3-A5",
  vocal_textures: ["breathy", "warm"],
  mix: "Wet",
  section_order: ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Pre-Chorus]", "[Chorus]", "[Bridge]", "[Final Chorus]", "[Outro]"],
  exclude_eras: ["1980s", "1990s"],
  exclude_genres: ["Metal", "Country", "Hip-Hop"],
  lyrical_world: "",
});

const FormInputPanel = ({ form, setForm, onSubmit, busy }) => {
  const { data: k } = useKnowledge();
  useEffect(() => {
    if (!form) setForm(defaultForm());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!form) return null;

  const update = (patch) => setForm({ ...form, ...patch });

  const addSubgenre = () => update({ subgenres: [...(form.subgenres || []), { name: "", weight_percent: 20 }] });
  const removeSubgenre = (i) => update({ subgenres: form.subgenres.filter((_, idx) => idx !== i) });
  const setSubgenre = (i, patch) => update({ subgenres: form.subgenres.map((s, idx) => idx === i ? { ...s, ...patch } : s) });

  const addInstrument = () => update({ instruments: [...(form.instruments || []), { type: "", model: "", play_method: "" }] });
  const removeInstrument = (i) => update({ instruments: form.instruments.filter((_, idx) => idx !== i) });
  const setInstrument = (i, patch) => update({ instruments: form.instruments.map((s, idx) => idx === i ? { ...s, ...patch } : s) });

  const toggleArray = (key, value) => {
    const arr = form[key] || [];
    update({ [key]: arr.includes(value) ? arr.filter((x) => x !== value) : [...arr, value] });
  };

  const toggleSection = (label) => toggleArray("section_order", label);

  return (
    <Card className="border bg-card">
      <CardHeader className="flex flex-row items-start justify-between gap-3 space-y-0 pb-3">
        <div>
          <CardTitle className="text-sm font-semibold">Structured form</CardTitle>
          <CardDescription className="text-xs mt-1">
            Fields map to the Suno Descriptive Prompt format. Edit anything, then assemble.
          </CardDescription>
        </div>
        <Button size="sm" onClick={onSubmit} disabled={busy} className="h-9" data-testid={GEN.assembleButton}>
          {busy === "assemble" ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
          <span className="ml-1.5 text-xs font-semibold">{busy === "assemble" ? "Assembling…" : "Assemble"}</span>
        </Button>
      </CardHeader>
      <CardContent>
        <ScrollArea className="suno-mono-scroll" style={{ maxHeight: "min(72vh, 720px)" }}>
          <div className="grid gap-5 pr-3">
            {/* Identity */}
            <Group title="Identity">
              <Field label="Working title">
                <Input value={form.title} onChange={(e) => update({ title: e.target.value })} placeholder="Salt & Sparks" />
              </Field>
              <Field label="Era">
                <Input value={form.era} onChange={(e) => update({ era: e.target.value })} />
              </Field>
              <Field label="BPM">
                <Input type="number" min={40} max={220} value={form.bpm} onChange={(e) => update({ bpm: parseInt(e.target.value || "0", 10) })} />
              </Field>
              <Field label="Italian tempo">
                <select
                  value={form.italian_tempo}
                  onChange={(e) => update({ italian_tempo: e.target.value })}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  {(k?.italian_tempos || []).map((t) => (
                    <option key={t.name} value={t.name}>{t.name} ({t.bpm_range} BPM)</option>
                  ))}
                </select>
              </Field>
              <Field label="Time signature">
                <Input value={form.time_signature} onChange={(e) => update({ time_signature: e.target.value })} />
              </Field>
              <Field label="Mix">
                <select
                  value={form.mix}
                  onChange={(e) => update({ mix: e.target.value })}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  {(k?.mix_types || []).map((m) => (
                    <option key={m.name} value={m.name}>{m.name} — {m.feel}</option>
                  ))}
                </select>
              </Field>
            </Group>

            {/* Genre */}
            <Group title="Genre & subgenre blend">
              <Field label="Mother genre">
                <select
                  value={form.mother_genre}
                  onChange={(e) => update({ mother_genre: e.target.value })}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  {(k?.mother_genres || []).map((g) => (
                    <option key={g} value={g}>{g}</option>
                  ))}
                </select>
              </Field>
              <Field label="Mood">
                <Input value={form.mood} onChange={(e) => update({ mood: e.target.value })} />
              </Field>
              <div className="sm:col-span-2 space-y-2">
                <Label className="text-xs uppercase tracking-wide text-muted-foreground">Subgenres (with weight %)</Label>
                <div className="space-y-2">
                  {(form.subgenres || []).map((s, i) => (
                    <div key={i} className="flex gap-2 items-center">
                      <SubgenreCombo
                        value={s.name}
                        options={k?.common_subgenres || []}
                        onChange={(v) => setSubgenre(i, { name: v })}
                      />
                      <Input
                        type="number"
                        min={0}
                        max={100}
                        value={s.weight_percent}
                        onChange={(e) => setSubgenre(i, { weight_percent: parseInt(e.target.value || "0", 10) })}
                        className="w-20"
                      />
                      <Button size="sm" variant="ghost" onClick={() => removeSubgenre(i)} aria-label="Remove">
                        <X size={14} />
                      </Button>
                    </div>
                  ))}
                  <Button size="sm" variant="secondary" onClick={addSubgenre} className="h-8">
                    <Plus size={14} /> <span className="ml-1 text-xs">Add subgenre</span>
                  </Button>
                </div>
              </div>
            </Group>

            {/* Instruments */}
            <Group title="Instruments">
              <div className="sm:col-span-2 space-y-2">
                {(form.instruments || []).map((it, i) => (
                  <div key={i} className="grid grid-cols-1 sm:grid-cols-[140px,1fr,1fr,auto] gap-2">
                    <Input placeholder="Type (Synth)" value={it.type} onChange={(e) => setInstrument(i, { type: e.target.value })} />
                    <Input placeholder="Model (Roland Juno-106)" value={it.model} onChange={(e) => setInstrument(i, { model: e.target.value })} />
                    <Input placeholder="Play method (arpeggio, legato…)" value={it.play_method} onChange={(e) => setInstrument(i, { play_method: e.target.value })} />
                    <Button size="sm" variant="ghost" onClick={() => removeInstrument(i)} aria-label="Remove">
                      <X size={14} />
                    </Button>
                  </div>
                ))}
                <Button size="sm" variant="secondary" onClick={addInstrument} className="h-8">
                  <Plus size={14} /> <span className="ml-1 text-xs">Add instrument</span>
                </Button>
              </div>
            </Group>

            {/* Vocals */}
            <Group title="Vocals">
              <Field label="Gender">
                <select
                  value={form.vocal_gender}
                  onChange={(e) => update({ vocal_gender: e.target.value })}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Non-binary">Non-binary</option>
                </select>
              </Field>
              <Field label="Technical range">
                <select
                  value={form.vocal_range}
                  onChange={(e) => update({ vocal_range: e.target.value })}
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  {(k?.vocal_ranges || []).map((v) => (
                    <option key={v.label} value={`${v.label} ${v.range}`}>{v.label} {v.range}</option>
                  ))}
                </select>
              </Field>
              <div className="sm:col-span-2 space-y-2">
                <Label className="text-xs uppercase tracking-wide text-muted-foreground">Vocal textures</Label>
                <div className="flex flex-wrap gap-1.5">
                  {(k?.vocal_textures || []).map((t) => (
                    <button
                      key={t}
                      type="button"
                      onClick={() => toggleArray("vocal_textures", t)}
                      className={`px-2 py-1 rounded-md border text-[12px] font-mono transition-colors ${
                        form.vocal_textures?.includes(t) ? "bg-primary/15 border-primary/50 text-foreground" : "bg-secondary/40 border-border text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>
            </Group>

            {/* Structure */}
            <Group title="Structure (section order)">
              <div className="sm:col-span-2 space-y-2">
                <p className="text-xs text-muted-foreground">Click to toggle the sections you want. Order is preserved as they appear here.</p>
                <div className="flex flex-wrap gap-1.5">
                  {(k?.section_meta_tags || []).map((tag) => {
                    const active = form.section_order?.includes(tag);
                    return (
                      <button
                        key={tag}
                        type="button"
                        onClick={() => toggleSection(tag)}
                        className={`px-2 py-1 rounded-md border text-[11px] font-mono transition-colors ${
                          active ? "bg-primary/15 border-primary/50 text-foreground" : "bg-secondary/40 border-border text-muted-foreground hover:text-foreground"
                        }`}
                      >
                        {tag}
                      </button>
                    );
                  })}
                </div>
                <div className="text-xs font-mono text-muted-foreground">Current order: {form.section_order?.join(" → ") || "—"}</div>
              </div>
            </Group>

            {/* Exclusions */}
            <Group title="Exclusions">
              <div className="sm:col-span-2 space-y-2">
                <Label className="text-xs uppercase tracking-wide text-muted-foreground">Exclude eras</Label>
                <div className="flex flex-wrap gap-1.5">
                  {["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"].map((era) => (
                    <button
                      key={era}
                      type="button"
                      onClick={() => toggleArray("exclude_eras", era)}
                      className={`px-2 py-1 rounded-md border text-[11px] font-mono transition-colors ${
                        form.exclude_eras?.includes(era) ? "bg-destructive/15 border-destructive/50 text-foreground" : "bg-secondary/40 border-border text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {era}
                    </button>
                  ))}
                </div>
              </div>
              <div className="sm:col-span-2 space-y-2">
                <Label className="text-xs uppercase tracking-wide text-muted-foreground">Exclude genres</Label>
                <div className="flex flex-wrap gap-1.5">
                  {(k?.mother_genres || []).map((g) => (
                    <button
                      key={g}
                      type="button"
                      onClick={() => toggleArray("exclude_genres", g)}
                      className={`px-2 py-1 rounded-md border text-[11px] font-mono transition-colors ${
                        form.exclude_genres?.includes(g) ? "bg-destructive/15 border-destructive/50 text-foreground" : "bg-secondary/40 border-border text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>
            </Group>

            {/* Lyrical world */}
            <Group title="Lyrical world (optional)">
              <div className="sm:col-span-2">
                <Textarea
                  rows={3}
                  value={form.lyrical_world}
                  onChange={(e) => update({ lyrical_world: e.target.value })}
                  placeholder="e.g. surreal dream-logic, image-led, hook-shaped writing; minimal narrative; second-person POV"
                  className="font-mono text-[13px] bg-secondary/40"
                />
              </div>
            </Group>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

const Group = ({ title, children }) => (
  <div className="rounded-xl border bg-secondary/30 p-3 sm:p-4">
    <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-3">{title}</div>
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">{children}</div>
  </div>
);

const Field = ({ label, children }) => (
  <div className="space-y-1.5">
    <Label className="text-xs uppercase tracking-wide text-muted-foreground">{label}</Label>
    {children}
  </div>
);

const SubgenreCombo = ({ value, options, onChange }) => {
  return (
    <>
      <Input
        list="subgenre-options"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Drift Phonk, Dance-Pop, etc."
        className="flex-1"
      />
      <datalist id="subgenre-options">
        {options.map((opt) => (
          <option key={opt} value={opt} />
        ))}
      </datalist>
    </>
  );
};

export default FormInputPanel;
export { defaultForm };
