{
  "meta": {
    "product": "Suno AI Song Prompt Generator",
    "app_type": "saas_app / hybrid_fullstack",
    "design_personality": [
      "studio-grade",
      "editorial",
      "dense-but-readable",
      "confident",
      "precision tooling",
      "dark-first with warm analog accents"
    ],
    "north_star": "Make long-form prompt + lyrics output feel like a premium DAW panel: crisp typography, clear hierarchy, fast copy actions, and unmistakable validation feedback."
  },

  "brand_attributes": {
    "tone": ["professional", "technical", "creative"],
    "keywords": ["analog gear", "mix console", "prompt engineering", "structured control"],
    "do_not": [
      "No transparent backgrounds",
      "No flashy gradients covering large areas",
      "No purple-heavy AI aesthetic",
      "No centered reading layouts"
    ]
  },

  "design_tokens": {
    "fonts": {
      "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');",
      "font_sans": "'Space Grotesk', ui-sans-serif, system-ui",
      "font_mono": "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
    },

    "typography_scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-base md:text-lg font-medium text-muted-foreground",
      "h3": "text-lg font-semibold",
      "body": "text-sm md:text-base",
      "small": "text-xs text-muted-foreground",
      "mono_block": "font-mono text-[13px] leading-6"
    },

    "spacing": {
      "page_padding": "px-4 sm:px-6 lg:px-8",
      "section_gap": "gap-6 lg:gap-8",
      "card_padding": "p-4 sm:p-5",
      "dense_row": "py-2",
      "comfortable_row": "py-3"
    },

    "radius": {
      "--radius": "0.75rem",
      "card": "rounded-xl",
      "button": "rounded-lg",
      "input": "rounded-md",
      "pill": "rounded-full"
    },

    "shadows": {
      "card": "shadow-[0_1px_0_rgba(255,255,255,0.04),0_12px_30px_rgba(0,0,0,0.35)]",
      "popover": "shadow-[0_10px_30px_rgba(0,0,0,0.45)]",
      "focus_ring": "ring-2 ring-offset-2"
    },

    "color_system": {
      "notes": [
        "Use HSL tokens in index.css to align with shadcn theming.",
        "Dark mode is default for this product; also provide a polished light mode.",
        "Warm amber is the primary accent (analog gear vibe). Teal is secondary for info/coach tips.",
        "Avoid purple gradients per rules; keep gradients subtle and decorative only."
      ],

      "dark": {
        "background": "222 18% 7%",
        "foreground": "210 20% 96%",

        "card": "222 18% 9%",
        "card-foreground": "210 20% 96%",

        "popover": "222 18% 9%",
        "popover-foreground": "210 20% 96%",

        "primary": "38 92% 56%",
        "primary-foreground": "222 18% 10%",

        "secondary": "222 14% 14%",
        "secondary-foreground": "210 20% 96%",

        "muted": "222 12% 14%",
        "muted-foreground": "215 12% 70%",

        "accent": "222 14% 14%",
        "accent-foreground": "210 20% 96%",

        "border": "222 12% 18%",
        "input": "222 12% 18%",
        "ring": "38 92% 56%",

        "semantic": {
          "success": "142 70% 45%",
          "warning": "38 92% 56%",
          "error": "0 84% 60%",
          "info": "190 85% 45%"
        },

        "surfaces": {
          "surface_1": "222 18% 9%",
          "surface_2": "222 16% 11%",
          "surface_3": "222 14% 13%"
        }
      },

      "light": {
        "background": "40 33% 98%",
        "foreground": "222 18% 12%",

        "card": "0 0% 100%",
        "card-foreground": "222 18% 12%",

        "popover": "0 0% 100%",
        "popover-foreground": "222 18% 12%",

        "primary": "28 92% 48%",
        "primary-foreground": "0 0% 100%",

        "secondary": "40 20% 94%",
        "secondary-foreground": "222 18% 12%",

        "muted": "40 20% 94%",
        "muted-foreground": "222 10% 40%",

        "accent": "40 20% 94%",
        "accent-foreground": "222 18% 12%",

        "border": "222 10% 86%",
        "input": "222 10% 86%",
        "ring": "28 92% 48%",

        "semantic": {
          "success": "142 55% 35%",
          "warning": "28 92% 48%",
          "error": "0 72% 50%",
          "info": "190 70% 35%"
        },

        "surfaces": {
          "surface_1": "0 0% 100%",
          "surface_2": "40 33% 97%",
          "surface_3": "40 20% 94%"
        }
      },

      "allowed_gradients": {
        "rule": "Decorative only; max ~20% viewport; never on text-heavy blocks; never on small UI elements.",
        "dark_hero_overlay": "radial-gradient(900px circle at 20% 10%, rgba(245,158,11,0.14), transparent 55%), radial-gradient(700px circle at 80% 0%, rgba(34,211,238,0.10), transparent 50%)",
        "light_hero_overlay": "radial-gradient(900px circle at 20% 10%, rgba(249,115,22,0.12), transparent 55%), radial-gradient(700px circle at 80% 0%, rgba(34,211,238,0.10), transparent 50%)"
      },

      "noise_texture": {
        "usage": "Apply subtle noise overlay to page background only (not cards) to avoid flatness.",
        "css_snippet": ".noise-overlay{position:relative;} .noise-overlay:before{content:'';position:absolute;inset:0;pointer-events:none;background-image:url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22120%22 height=%22120%22%3E%3Cfilter id=%22n%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%222%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22120%22 height=%22120%22 filter=%22url(%23n)%22 opacity=%220.08%22/%3E%3C/svg%3E');mix-blend-mode:overlay;opacity:.35;border-radius:inherit;}"
      }
    }
  },

  "layout_and_grid": {
    "top_level": {
      "container": "max-w-[1280px] mx-auto",
      "page_structure": "Top Nav (sticky) + main workspace (2-column on desktop) + optional right Workflow Coach panel",
      "desktop_grid": "lg:grid lg:grid-cols-[minmax(520px,1fr)_minmax(520px,1fr)] lg:gap-6",
      "coach_panel": "xl:grid-cols-[minmax(520px,1fr)_minmax(520px,1fr)_360px]"
    },
    "reading_flow": [
      "Left column: inputs + validation summary",
      "Right column: outputs (tabbed cards) + copy actions",
      "Workflow Coach: contextual tips, collapsible on smaller screens"
    ],
    "responsive": {
      "mobile": "Single column; outputs below inputs; coach becomes Drawer/Sheet",
      "tablet": "Two sections stacked with sticky output tabs header",
      "desktop": "Two-column split; outputs scroll independently using ScrollArea"
    }
  },

  "component_path": {
    "shadcn_primary": [
      "/app/frontend/src/components/ui/button.jsx",
      "/app/frontend/src/components/ui/card.jsx",
      "/app/frontend/src/components/ui/tabs.jsx",
      "/app/frontend/src/components/ui/badge.jsx",
      "/app/frontend/src/components/ui/textarea.jsx",
      "/app/frontend/src/components/ui/input.jsx",
      "/app/frontend/src/components/ui/select.jsx",
      "/app/frontend/src/components/ui/slider.jsx",
      "/app/frontend/src/components/ui/switch.jsx",
      "/app/frontend/src/components/ui/table.jsx",
      "/app/frontend/src/components/ui/scroll-area.jsx",
      "/app/frontend/src/components/ui/separator.jsx",
      "/app/frontend/src/components/ui/sheet.jsx",
      "/app/frontend/src/components/ui/drawer.jsx",
      "/app/frontend/src/components/ui/tooltip.jsx",
      "/app/frontend/src/components/ui/sonner.jsx"
    ],
    "optional": [
      "Flowbite: use only for inspiration; implement with shadcn primitives",
      "21st.dev: use patterns (bento grids, command palette) but implement locally"
    ]
  },

  "core_patterns": {
    "top_nav": {
      "layout": "Sticky top bar with subtle border; left brand mark + name; right nav links + About/Help button",
      "classes": "sticky top-0 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 border-b",
      "brand_mark": "Simple 12px dot-grid or waveform glyph (lucide icon) in amber",
      "nav_link": {
        "default": "text-sm text-muted-foreground hover:text-foreground",
        "active": "text-foreground",
        "data_testids": {
          "generator_link": "top-nav-generator-link",
          "library_link": "top-nav-library-link",
          "help_button": "top-nav-help-button"
        }
      }
    },

    "mode_switcher": {
      "component": "Tabs",
      "tabs": ["AI Mode", "Form Mode", "Hybrid"],
      "placement": "Top of Generator page, above inputs",
      "style": "Segmented control feel: TabsList as rounded-full, subtle inset border",
      "classes": {
        "tabs_list": "inline-flex rounded-full bg-secondary p-1 border",
        "tab": "rounded-full px-3 py-1.5 text-sm data-[state=active]:bg-background data-[state=active]:shadow-sm",
        "tab_active_accent": "data-[state=active]:ring-1 data-[state=active]:ring-ring"
      },
      "data_testids": {
        "tabs_root": "mode-switcher-tabs",
        "ai_tab": "mode-switcher-ai",
        "form_tab": "mode-switcher-form",
        "hybrid_tab": "mode-switcher-hybrid"
      }
    },

    "input_panel": {
      "pattern": "Card with section headers + dense form rows",
      "header": "Title + short helper text + right-aligned Generate button",
      "form_layout": "Use 2-column grid on md+ for compactness; keep labels above inputs on mobile",
      "classes": {
        "card": "rounded-xl border bg-card text-card-foreground",
        "section_title": "text-sm font-semibold tracking-tight",
        "helper": "text-xs text-muted-foreground",
        "grid": "grid grid-cols-1 md:grid-cols-2 gap-4",
        "row": "space-y-2"
      },
      "data_testids": {
        "concept_textarea": "concept-input-textarea",
        "generate_button": "generator-generate-button",
        "save_button": "generator-save-button"
      }
    },

    "output_card_pattern": {
      "goal": "Make outputs feel like copyable 'console blocks' with strong hierarchy and zero ambiguity.",
      "structure": [
        "CardHeader: title + right-side actions (Copy, Save-to-library optional)",
        "CardContent: monospace output block (ScrollArea if long)",
        "Footer (optional): char counter / meta info / last generated timestamp"
      ],
      "copy_button": {
        "placement": "Top-right in header; always visible",
        "component": "Button variant=secondary size=sm + Tooltip",
        "icon": "lucide-react Copy",
        "classes": "h-8 px-2.5",
        "micro_interaction": "On click: brief success toast via sonner + button label swaps to 'Copied' for 900ms",
        "data_testid": "output-copy-button-<output-key>"
      },
      "char_counter": {
        "placement": "Right side of header or footer for Style Prompt only",
        "style": "Monospace, muted; turns amber at >900 chars; turns red at >1000",
        "classes": "font-mono text-xs tabular-nums",
        "data_testid": "style-prompt-char-counter"
      },
      "mono_output_block": {
        "component": "ScrollArea wrapping a <pre> or <div> with whitespace-pre-wrap",
        "classes": "font-mono text-[13px] leading-6 bg-secondary/40 border rounded-lg p-3 sm:p-4 whitespace-pre-wrap break-words selection:bg-[hsl(var(--primary)/0.25)]",
        "no_transparency": "Use solid bg-secondary/40 (Tailwind opacity is fine; not transparent backgrounds).",
        "data_testid": "output-mono-block-<output-key>"
      },
      "syntax_highlighting_lyrics": {
        "approach": "Lightweight token styling (no heavy editor) using regex split for Suno meta-tags like [Verse], [Chorus], [Bridge], [Intro], [Outro], [Hook].",
        "tag_style": "Badge-like inline spans: amber border + slightly darker background",
        "classes": {
          "tag": "inline-flex items-center rounded-md border px-2 py-0.5 font-mono text-xs bg-[hsl(var(--primary)/0.10)] border-[hsl(var(--primary)/0.35)] text-foreground",
          "lyric_text": "text-foreground",
          "muted": "text-muted-foreground"
        },
        "data_testid": "lyrics-syntax-highlighted"
      }
    },

    "outputs_tabs": {
      "component": "Tabs",
      "tabs": [
        "Style Prompt",
        "Exclude Styles",
        "Lyrics",
        "Recommended Scales",
        "Structure & Rhyme Map"
      ],
      "layout": "TabsList sticky within output column on desktop; keep visible while scrolling outputs",
      "classes": {
        "tabs_list": "sticky top-[64px] z-10 bg-background/95 backdrop-blur border rounded-xl p-1",
        "tab": "text-xs sm:text-sm px-2.5 py-1.5 rounded-lg data-[state=active]:bg-secondary data-[state=active]:text-foreground",
        "tab_badge": "ml-2"
      },
      "data_testids": {
        "tabs_root": "outputs-tabs",
        "tab_style": "outputs-tab-style-prompt",
        "tab_exclude": "outputs-tab-exclude-styles",
        "tab_lyrics": "outputs-tab-lyrics",
        "tab_scales": "outputs-tab-recommended-scales",
        "tab_map": "outputs-tab-structure-rhyme-map"
      }
    },

    "validation_panel": {
      "pattern": "Dedicated Card directly under inputs; also show inline highlights in outputs.",
      "priority": "Errors always above warnings; show counts in header badges.",
      "semantic_colors": {
        "error": {
          "badge": "bg-[hsl(var(--destructive)/0.15)] text-[hsl(var(--destructive))] border-[hsl(var(--destructive)/0.35)]",
          "left_border": "border-l-4 border-l-[hsl(var(--destructive))]"
        },
        "warning": {
          "badge": "bg-[hsl(var(--primary)/0.12)] text-foreground border-[hsl(var(--primary)/0.35)]",
          "left_border": "border-l-4 border-l-[hsl(var(--primary))]"
        },
        "info": {
          "badge": "bg-[hsl(var(--chart-2)/0.14)] text-foreground border-[hsl(var(--chart-2)/0.35)]",
          "left_border": "border-l-4 border-l-[hsl(var(--chart-2))]"
        }
      },
      "banned_word_inline_highlight": {
        "where": "In lyrics output and in concept input preview",
        "style": "Underline + subtle red background chip; keep readable",
        "classes": "px-1 rounded-sm bg-[hsl(var(--destructive)/0.18)] text-foreground underline decoration-[hsl(var(--destructive))] decoration-2 underline-offset-2",
        "data_testid": "banned-word-highlight"
      },
      "bar_math_warning": {
        "presentation": "Show computed duration + bars + BPM math in a compact mono row; highlight mismatch",
        "classes": "font-mono text-xs tabular-nums",
        "data_testid": "bar-math-validation-row"
      },
      "data_testids": {
        "panel": "validation-panel",
        "error_list": "validation-errors-list",
        "warning_list": "validation-warnings-list"
      }
    },

    "structure_rhyme_map_table": {
      "component": "Table",
      "columns": [
        "Section",
        "Bars",
        "Syllables/Line",
        "Rhyme Scheme",
        "Notes"
      ],
      "density": "Dense but scannable; use tabular-nums; right-align numeric columns",
      "classes": {
        "table_wrap": "rounded-xl border overflow-hidden",
        "thead": "bg-secondary/60",
        "th": "text-xs font-semibold text-muted-foreground",
        "td": "text-sm",
        "num": "font-mono text-[13px] tabular-nums text-right",
        "row_hover": "hover:bg-secondary/40"
      },
      "empty_state": "Show a single row with muted text: 'Generate to see the map.'",
      "data_testids": {
        "table": "structure-rhyme-map-table",
        "row": "structure-rhyme-map-row-<index>"
      }
    },

    "recommended_scales": {
      "pattern": "Two sliders + preset badge + short explanation",
      "components": ["Slider", "Badge", "Card"],
      "layout": "Two-column on md+; each slider row shows value in mono",
      "classes": {
        "value": "font-mono text-xs tabular-nums",
        "preset_badge": "border bg-secondary/50"
      },
      "data_testids": {
        "weirdness_slider": "scales-weirdness-slider",
        "style_influence_slider": "scales-style-influence-slider",
        "preset_badge": "scales-preset-badge"
      }
    },

    "workflow_coach_panel": {
      "pattern": "Right-side Card with collapsible sections; on mobile open via Sheet",
      "components": ["Sheet", "Accordion", "Badge"],
      "content": "Contextual tips keyed off selected preset/mode (e.g., Oil & Water).",
      "classes": {
        "panel": "rounded-xl border bg-card",
        "tip": "text-sm leading-6",
        "callout": "rounded-lg border bg-secondary/40 p-3"
      },
      "data_testids": {
        "open_button": "workflow-coach-open-button",
        "panel": "workflow-coach-panel"
      }
    },

    "library_grid": {
      "pattern": "Card grid with strong metadata hierarchy + quick actions",
      "grid": "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4",
      "card": {
        "layout": "Title row + metadata chips + preview snippet + footer actions",
        "title": "text-base font-semibold line-clamp-1",
        "meta": "flex flex-wrap gap-2",
        "snippet": "font-mono text-xs text-muted-foreground line-clamp-4",
        "footer": "flex items-center justify-between pt-3"
      },
      "actions": {
        "open": "Button variant=secondary size=sm",
        "copy_style": "Button variant=ghost size=sm",
        "data_testids": {
          "card": "library-item-card-<id>",
          "open": "library-item-open-button-<id>",
          "copy": "library-item-copy-style-button-<id>"
        }
      },
      "empty_state": {
        "headline": "No saved generations yet",
        "body": "Generate a prompt and hit Save to build your library.",
        "cta": "Go to Generator",
        "data_testid": "library-empty-state"
      }
    },

    "about_help_drawer": {
      "component": "Sheet or Drawer (mobile)",
      "content": [
        "Banned words rules",
        "Structure conventions",
        "Scale presets cheat sheet",
        "Copy + save workflow"
      ],
      "classes": "max-w-[520px]",
      "data_testids": {
        "open": "help-drawer-open-button",
        "content": "help-drawer-content"
      }
    }
  },

  "iconography": {
    "library": "lucide-react",
    "recommended_icons": {
      "brand": "Waveform",
      "generate": "Sparkles",
      "copy": "Copy",
      "save": "BookmarkPlus",
      "library": "Library",
      "warning": "TriangleAlert",
      "error": "CircleX",
      "info": "Info",
      "help": "CircleHelp",
      "settings": "SlidersHorizontal"
    },
    "rules": [
      "Use 16px icons in buttons; 18px in headers.",
      "Keep stroke width consistent (lucide default)."
    ]
  },

  "motion_guidelines": {
    "principles": [
      "Subtle, tool-like motion (no bouncy overshoot).",
      "Prefer opacity + small translateY entrance for panels.",
      "Respect prefers-reduced-motion."
    ],
    "durations": {
      "fast": "120ms",
      "base": "180ms",
      "slow": "240ms"
    },
    "easings": {
      "standard": "cubic-bezier(0.2, 0.8, 0.2, 1)",
      "out": "cubic-bezier(0.16, 1, 0.3, 1)"
    },
    "micro_interactions": {
      "buttons": "hover: slight brightness + border emphasis; active: scale-[0.98]",
      "tabs": "active tab fades background in; no sliding underline",
      "copy": "toast + temporary label change",
      "validation": "when errors appear, animate in with opacity + translateY-1"
    },
    "implementation": {
      "tailwind": "transition-colors duration-150 ease-out (avoid transition-all)",
      "framer_motion_optional": {
        "install": "npm i framer-motion",
        "use_cases": ["panel entrance", "tab content fade", "coach drawer"],
        "note": "Optional; keep minimal to avoid perf issues in dense UI."
      }
    }
  },

  "accessibility": {
    "contrast": [
      "All text on dark surfaces must meet WCAG AA; use muted-foreground only for secondary text.",
      "Never place muted text on secondary/40 backgrounds without testing."
    ],
    "focus": "Use visible ring with ring color = --ring and ring-offset = background.",
    "keyboard": [
      "Tabs, Select, Slider, Sheet must be fully keyboard navigable (shadcn defaults)."
    ],
    "content": [
      "Long outputs must be scrollable with ScrollArea; avoid huge page scroll jumps.",
      "Use aria-label on icon-only buttons (Copy, Save)."
    ]
  },

  "empty_states": {
    "generator": {
      "when": "Before first generation",
      "pattern": "Card with short checklist + example prompt chips",
      "example_chips": [
        "'90s trip-hop noir, brushed drums, vinyl hiss'",
        "'uplifting indie folk duet, stomp-clap, 120 BPM'",
        "'minimal techno, 128 BPM, hypnotic bass, dry mix'"
      ],
      "data_testid": "generator-empty-state"
    },
    "outputs": {
      "when": "No output yet",
      "copy": "Generate to see results here.",
      "data_testid": "outputs-empty-state"
    }
  },

  "image_urls": {
    "policy": "This is a tool-first SaaS; avoid stock photography in core UI. Use subtle abstract backgrounds only if needed.",
    "recommended": [
      {
        "category": "decorative",
        "description": "Optional subtle abstract texture for About/Help drawer header (not behind text blocks).",
        "image_url": ""
      }
    ]
  },

  "implementation_notes_for_main_agent": {
    "theme_default": "Set <html class='dark'> by default; provide a toggle later if desired.",
    "css_updates": [
      "Replace current shadcn tokens in /app/frontend/src/index.css with the token values above.",
      "Remove CRA starter centering styles in App.css (App-header align center) and rely on Tailwind layout.",
      "Add Google Fonts import at top of index.css and set body font-family to var(--font-sans) via Tailwind base layer or CSS."
    ],
    "data_testid_rule": "Every button/input/tab trigger/copy action/save action/error row must include data-testid in kebab-case.",
    "outputs": {
      "rendering": "Use <pre> with whitespace-pre-wrap for prompts/lyrics; wrap in ScrollArea for long content.",
      "copy": "Use navigator.clipboard.writeText + sonner toast."
    },
    "no_transparent_backgrounds": "Avoid glassmorphism; use solid card backgrounds (bg-card, bg-secondary/40 is acceptable as it remains opaque enough)."
  },

  "GENERAL_UI_UX_DESIGN_GUIDELINES": "- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n- NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals."
}
