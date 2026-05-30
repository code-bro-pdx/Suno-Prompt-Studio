import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetTrigger } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CircleHelp, Library, Sparkles, AudioWaveform, Sun, Moon } from "lucide-react";
import { NAV } from "@/constants/testIds";
import HelpDrawerContent from "@/components/layout/HelpDrawerContent";

const Layout = ({ children }) => {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    const root = document.documentElement;
    setIsDark(root.classList.contains("dark"));
  }, []);

  const toggleTheme = () => {
    const root = document.documentElement;
    if (root.classList.contains("dark")) {
      root.classList.remove("dark");
      setIsDark(false);
    } else {
      root.classList.add("dark");
      setIsDark(true);
    }
  };

  return (
    <div className="relative min-h-screen">
      <div className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
        <div className="mx-auto max-w-[1320px] px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2.5" data-testid={NAV.brand}>
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/15 text-primary border border-primary/30">
              <AudioWaveform size={18} strokeWidth={2.2} />
            </span>
            <div className="leading-tight">
              <div className="text-sm font-semibold tracking-tight">Suno Prompt Studio</div>
              <div className="text-[11px] text-muted-foreground -mt-0.5">Architected for power users</div>
            </div>
          </NavLink>
          <nav className="flex items-center gap-1">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-colors duration-150 ${
                  isActive ? "bg-secondary text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-secondary/60"
                }`
              }
              data-testid={NAV.generator}
            >
              <Sparkles size={15} /> Generator
            </NavLink>
            <NavLink
              to="/library"
              className={({ isActive }) =>
                `inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-colors duration-150 ${
                  isActive ? "bg-secondary text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-secondary/60"
                }`
              }
              data-testid={NAV.library}
            >
              <Library size={15} /> Library
            </NavLink>
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="sm" className="text-muted-foreground" data-testid={NAV.help}>
                  <CircleHelp size={15} /> Help
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="sm:max-w-[520px] overflow-y-auto" data-testid="help-drawer-content">
                <SheetHeader>
                  <SheetTitle>Field guide</SheetTitle>
                  <SheetDescription>Conventions distilled from the Suno reference docs.</SheetDescription>
                </SheetHeader>
                <HelpDrawerContent />
              </SheetContent>
            </Sheet>
            <Button
              variant="ghost"
              size="sm"
              className="text-muted-foreground"
              onClick={toggleTheme}
              aria-label="Toggle theme"
              data-testid={NAV.theme}
            >
              {isDark ? <Sun size={15} /> : <Moon size={15} />}
            </Button>
          </nav>
        </div>
      </div>
      <div className="relative z-10 suno-hero-gradient">
        <div className="mx-auto max-w-[1320px] px-4 sm:px-6 lg:px-8 py-6 lg:py-8">{children}</div>
      </div>
    </div>
  );
};

export default Layout;
