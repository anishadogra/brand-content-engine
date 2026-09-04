---
name: figma-carousel-pipeline
description: End-to-end pipeline for designing and building Instagram carousels for {{brand.name}} ({{product.line_a}} + {{product.line_b}} lines) natively in Figma. Use whenever the user asks for a {{brand.name}} carousel, IG swipeable post, multi-slide product story, or a content batch. Runs a 4-phase pipeline — Research → Synthesize → Build (in Figma via use_figma MCP) → QA — with deep product research baked in so every slide is punchy, intriguing, and narratively connected.
---

# {{brand.name}} Figma Carousel Skill

End-to-end carousel builder for {{brand.name}}. Outputs a real, editable Figma file with 1080×1350 frames per slide, plus PNGs ready for Instagram.

## When to trigger

- "Make a {{brand.name}} carousel about X"
- "Spotlight carousel for [{{sku.flavour_1}} / {{sku.heat_1}} / {{sku.heritage_1}} / etc.]"
- "Carousel batch for the new launches"
- "Build a {{product.line_b}} story for IG"
- Calendar-driven: "Do this week's {{brand.name}} carousels from the calendar"

## Hard rules (NEVER violate)

1. **Pack pixels are sacred.** Never let any AI alter the pack itself. Strip white backgrounds via Pillow → transparent PNG, then composite. The pack inside must match the source byte-for-byte.
2. **No misleading numbers on the pack pill.** Never put a nutrition figure next to the product name on the pack pill — readers parse it as pack weight. Use `"FLAVOUR · {{PRODUCT_LINE_A}}"` only. Nutrition figures live on the dedicated proof slide, with the unit and the basis stated in full.
3. **Build natively in Figma via the `use_figma` MCP.** Never fall back to HTML rendering. The user wants editable Figma frames.
4. **Brand tokens are locked.** Colours, type, voice all live in `reference/brand-tokens.json`. No new colours per carousel.
5. **British spelling.** "flavour", "colour", "centred".
6. **Voice:** bold, direct, confident. Sentence case. Left-aligned. No "maybe / try / might". Period-punctuated. Lead with flavour.
7. **Slide count: minimum 5.** Sweet spot 5–6.
8. **Always show every slide inline.** Screenshot via `get_screenshot` MCP and read inline before asking for approval. Never hand over just a Figma URL.
9. **Information must be punchy + intriguing + narratively connected.** This is the reason for the Research phase. Every slide should make the viewer want to swipe to the next. The 5 slides should read as one connected story, not 5 facts in isolation.
10. **Never recreate the wordmark in a substitute font.** A custom wordmark has letterforms no free font matches, and the mismatch is obvious to anyone who knows the brand. Place the official lockup asset as a single image — `{{brand.assets.lockup_primary}}`, or `{{brand.assets.lockup_inverse}}` on dark backgrounds. The same applies to any pack design-language element: use the source asset, never rebuild it.
11. **Layout must be structurally aligned.** Text, images, graphics — every element must sit on the grid. Nothing crooked. Nothing floating awkwardly. Test by squinting: does the slide read as orderly and clean? If not, fix alignment before shipping. Specifically:
    - All text x-positions snap to the 72px margin or aligned columns
    - Image cards have consistent card-bg colour + corner radius (28px)
    - Equal vertical spacing between repeating elements (checks list, recipe steps)
    - No element sits between two grid columns — pick one
    - Pill/badge baseline aligns to a sensible reference (card edge, not floating mid-card)
    - Stat unit ("g") sits on the same baseline as the bottom of the stat number, not floating

## 4-Phase Pipeline

### Phase 1 — RESEARCH (deepest layer; gives every slide its substance)

For each product / topic, run the prompt at `research/research-prompt.md`. Output a structured research doc covering:

| Layer | What it captures |
|---|---|
| Category context | What is the broader category? ({{product.line_a}}, dry-cured sausage, etc.) |
| Cultural / historical roots | Where does it come from? Who eats it? What's its name in different cultures? |
| Process / craft | How is it made? Why does this method matter? |
| Nutritional truth | Verified specs (protein, fat, carbs, etc.) — NOT marketing claims |
| Sensory profile | Taste notes — sweet, salty, smoky, hot, umami, etc. — written like a sommelier |
| Pairings | What does it eat well with? Drinks, dishes, occasions |
| Fun facts / surprising stats | Things that intrigue. A nutrition figure against a familiar reference food, a cultural tradition attached to the category, or something about the process that explains how it eats. Each one sourced. |
| Competitive context | What makes THIS product different from the category default? |
| Hook angles | 5–8 candidate headline directions, each in {{brand.name}} voice |

Cache the research at `research/cache/<sku_slug>.md` so subsequent carousels for the same SKU don't re-research.

### Phase 2 — SYNTHESIZE (research → carousel JSON spec)

Use the prompt at `research/synthesis-prompt.md`. Steps:

1. **Pick a narrative arc** from `reference/narrative-arcs.md` based on intent (spotlight, category explainer, recipe, founder story, etc.)
2. **Pick the strongest hook** from the research's hook angles (the one most likely to stop a scroll)
3. **Map research facts to slides** so the 5 slides read as one connected story, not isolated facts:
   - Slide 1 (hook) sets up the curiosity
   - Slide 2 (deepens) — origin story OR taste note OR surprising claim that pays off the hook
   - Slide 3 (proof) — the data that earns trust
   - Slide 4 (utility) — recipe / use case / range, so they imagine using it
   - Slide 5 (CTA) — handle, tagline, follow ask
4. **Tighten copy ruthlessly.** Each line must earn its place. Remove every "we believe", "we think", "the perfect snack". Punch up verbs.
5. **Output as JSON** matching the schema in `reference/slide-templates.md`

### Phase 3 — BUILD (drive Figma via use_figma MCP)

See full Figma build sequence in `reference/figma-build-recipe.md`. Critical sequence:

1. Call `whoami` → get planKey
2. `create_new_file` (planKey, fileName, editorType: "design")
3. **Set up design system** via `use_figma`:
   - Rename "Page 1" → "🎨 Design System", create "📱 Carousels" page
   - Create colour variables ({{brand.name}} Brand collection) bound to the 11 brand colours
   - Create text styles for eyebrow / hero / headline / body / etc.
4. **Upload the official {{brand.name}} lockup** (`assets/logo/lockup_primary.png` and `lockup_reverse.png`) FIRST. These replace the symbol+wordmark chrome on every slide. NEVER recreate the wordmark in a font.
5. **Strip pack image backgrounds** to transparent PNG via Pillow (`scripts/strip_white_bg.py`) BEFORE upload.
6. **Upload assets** via `upload_assets` (one call per asset; POST file via curl to returned submitUrl). Capture each `imageHash` for later use.
7. **Build slides** in one large `use_figma` call using the proven slide builders (hero / quote / proof / difference / recipe / origin / range / cta). See `reference/slide-builders.js` for the canonical implementations.
8. **Wrap each carousel** in a row frame so we can screenshot whole carousels at once.
9. **Alignment QA pass before screenshot:** read each slide and verify every element snaps to the grid. Misaligned text, off-baseline pills, floating decorations — all fix-before-ship.

### Phase 4 — QA

Before declaring done:
- ✅ Every slide has chrome: {{brand.name}} symbol top-left, page counter top-right, footer line at bottom
- ✅ No misleading numbers on pack pill
- ✅ Pack image backgrounds transparent (not white squares)
- ✅ No text overlap (especially origin slides — keep headline col 460 wide, body col starts x=540)
- ✅ Screenshot every carousel as a row + show inline
- ✅ Provide Figma URL + offer to export PNGs

## Bug log (don't repeat these)

These were caught during the first run on 2026-05-02 — encoded so future runs avoid them:

1. **letterSpacing in PERCENT mode is the percentage value directly.** Don't multiply by 100. `{value: 14, unit: "PERCENT"}` = 14%. Multiplying gave 1400% spacing → each character on its own line.
2. **Width-constrained text needs `textAutoResize = "HEIGHT"` BEFORE resize.** Without it, text either truncates or auto-fits-to-content.
3. **`figma.loadAllPagesAsync` is not supported in the headless plugin env.** Iterate `figma.root.children` directly.
4. **Helvetica is NOT in Figma's font list (headless env).** Substitute with Inter Bold/Regular for primary text. Archivo Black is the display font (free Google Fonts substitute for Okine, which is proprietary).
5. **Position downstream elements based on actual `.height` of rendered text**, not on `\n`-counted line heights — text wraps unexpectedly when it doesn't fit width, throwing off computed positions and causing overlap.
6. **Origin template needs headline column ≤ 460 wide** because body column starts at x=540. Otherwise headline overlaps body. Also keep origin headline font ≤ 80pt to prevent mid-word breaks.
7. **`upload_assets` returns `placedOnNodeId` only sometimes** — follow up with explicit `setFills([{type:"IMAGE", scaleMode, imageHash}])` via `use_figma` to guarantee placement.

## Files

```
~/.claude/skills/figma-carousel-pipeline/
├── SKILL.md                                # this file
├── reference/
│   ├── brand-tokens.json                   # colours, type, voice
│   ├── slide-templates.md                  # 8 templates + JSON schemas
│   ├── narrative-arcs.md                   # 8 arc patterns
│   ├── voice-guide.md                      # tone rules + headline pack
│   ├── figma-build-recipe.md               # step-by-step Figma MCP sequence
│   └── slide-builders.js                   # canonical JS builders for use_figma
├── research/
│   ├── research-prompt.md                  # the deep-dive prompt
│   ├── synthesis-prompt.md                 # research → JSON spec prompt
│   └── cache/
│       ├── sku_flavour_1.md
│       ├── korean_chilli.md
│       ├── sku_heritage_4.md
│       ├── ghost_chilli.md
│       ├── smoked_pink_salt.md
│       ├── sour_cream_onion.md
│       ├── lemon_pepper.md
│       ├── sku_heritage_1.md
│       ├── sku_heritage_2.md
│       ├── pepper_bites.md
│       └── sku_heritage_3.md
├── scripts/
│   ├── strip_white_bg.py                   # pack JPG → transparent PNG
│   └── upload_helper.sh                    # multi-file curl POST helper
└── examples/
    └── 2026-05-02-eight-carousels.md       # the first batch (Figma URL + IDs)
```

## Outputs

- A live Figma file (URL) with 8 carousel rows × 5 slides each
- All 40 slides exported as 1080×1350 PNGs (sRGB, ready for IG) into `~/.claude/skills/figma-carousel-pipeline/output/<run_slug>/`
- A `manifest.json` per run with carousel/slide → file mapping
