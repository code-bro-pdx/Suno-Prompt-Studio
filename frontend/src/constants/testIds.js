// Centralised data-testid constants for the Suno Prompt Generator
export const HOME = {
  emergentLink: "emergent-home-link",
};

export const NAV = {
  brand: "top-nav-brand",
  generator: "top-nav-generator-link",
  library: "top-nav-library-link",
  help: "top-nav-help-button",
  theme: "top-nav-theme-toggle",
};

export const MODE = {
  tabs: "mode-switcher-tabs",
  ai: "mode-switcher-ai",
  form: "mode-switcher-form",
  hybrid: "mode-switcher-hybrid",
};

export const GEN = {
  conceptTextarea: "concept-input-textarea",
  generateButton: "generator-generate-button",
  fillFormButton: "generator-fill-form-button",
  assembleButton: "generator-assemble-button",
  saveButton: "generator-save-button",
  emptyState: "generator-empty-state",
};

export const OUT = {
  tabs: "outputs-tabs",
  tabStyle: "outputs-tab-style-prompt",
  tabExclude: "outputs-tab-exclude-styles",
  tabLyrics: "outputs-tab-lyrics",
  tabScales: "outputs-tab-recommended-scales",
  tabMap: "outputs-tab-structure-rhyme-map",
  copy: (key) => `output-copy-button-${key}`,
  monoBlock: (key) => `output-mono-block-${key}`,
  styleCharCounter: "style-prompt-char-counter",
  emptyState: "outputs-empty-state",
};

export const VAL = {
  panel: "validation-panel",
  errors: "validation-errors-list",
  warnings: "validation-warnings-list",
  bannedHighlight: "banned-word-highlight",
  barMath: "bar-math-validation-row",
};

export const LIB = {
  empty: "library-empty-state",
  card: (id) => `library-item-card-${id}`,
  open: (id) => `library-item-open-button-${id}`,
  copy: (id) => `library-item-copy-style-button-${id}`,
  delete: (id) => `library-item-delete-button-${id}`,
};
