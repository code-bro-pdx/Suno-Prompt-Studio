import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Copy, Check } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { OUT } from "@/constants/testIds";

const OutputCard = ({
  outputKey,
  title,
  description,
  content,
  rightHeader,
  renderContent,
  maxHeight = "min(60vh, 560px)",
}) => {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(content || "");
      setCopied(true);
      toast.success(`${title} copied`);
      setTimeout(() => setCopied(false), 1200);
    } catch (e) {
      toast.error("Copy failed");
    }
  };
  return (
    <Card className="border bg-card shadow-[0_1px_0_rgba(255,255,255,0.04),0_12px_30px_rgba(0,0,0,0.20)]">
      <CardHeader className="flex flex-row items-start justify-between gap-3 space-y-0 pb-3">
        <div className="min-w-0">
          <CardTitle className="text-sm font-semibold">{title}</CardTitle>
          {description && (
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
          )}
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {rightHeader}
          <Button
            variant="secondary"
            size="sm"
            onClick={copy}
            className="h-8 px-2.5 transition-colors duration-150"
            data-testid={OUT.copy(outputKey)}
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
            <span className="ml-1.5 text-xs">{copied ? "Copied" : "Copy"}</span>
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="suno-mono-scroll" style={{ maxHeight }}>
          <div
            className="font-mono text-[13px] leading-6 bg-secondary/40 border rounded-lg p-3 sm:p-4 whitespace-pre-wrap break-words selection:bg-[hsl(var(--primary)/0.25)]"
            data-testid={OUT.monoBlock(outputKey)}
          >
            {renderContent ? renderContent() : (content || "—")}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default OutputCard;
