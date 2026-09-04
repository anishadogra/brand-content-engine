# brand-content-engine

**A content production system for a brand, from voice definition through research and design to scheduled publishing.**

Five stages that hand off to each other with a defined artefact at each boundary, so no stage has to guess what the previous one meant.

---

## The stages

```
STRATEGY  →  VOICE  →  RESEARCH  →  PRODUCTION  →  PUBLISHING
```

| | |
|---|---|
| [`STRATEGY.md`](STRATEGY.md) | Pillars, cadence and what each format is for. The layer that stops "post more" being the plan. |
| [`voice/`](voice/) | A voice profile as a **schema**, not an adjective list — so a generated line can be checked against it rather than admired. |
| [`research/`](research/) | Two prompts: one to research a product before any copy exists, one to synthesise that into slide copy. Output is cached per SKU so the research is done once. |
| [`production/`](production/) | The four-phase build pipeline, narrative arcs, slide templates as JSON, and a brand-token schema. |
| [`publishing/`](publishing/) | Sheet-driven scheduling and auto-posting, with the blueprint and sheet schema. |

## Why research is a separate stage

The default failure of AI-generated brand content is that it is fluent about a product it knows nothing about. It will describe any snack as "irresistibly crunchy" and any service as "seamless," because those words fit anywhere — which is exactly why they land nowhere.

So the pipeline refuses to write copy until a research artefact exists: what the category actually is, where it comes from across several cultures, what makes this product different from the category default, and three kinds of hook — a nutrition figure against a familiar reference, a cultural tradition, a process detail that explains how it eats. **Each with a source.** A hook you cannot source is not a hook, it is a liability.

The research is cached per SKU, so it is done once and reused across every carousel about that product.

## Narrative arcs, not slide counts

[`production/narrative-arcs.md`](production/narrative-arcs.md) defines arcs — Spotlight, Heat, Origin — and each has a stated *use when*. A carousel is picked as an arc first and populated second, which is the difference between a story and eight slides in a row.

[`production/slide-templates.md`](production/slide-templates.md) then specifies each slide type as a JSON contract: which fields exist, which are required, what renders where. The generative step fills fields; it does not invent layout.

## Two rules carried over from real failures

**Never put a nutrition figure beside the product name on a pack pill.** Readers parse a number in that position as pack weight. Nutrition figures go on the dedicated proof slide with the unit and basis stated in full.

**Never rebuild a wordmark in a substitute font.** A custom wordmark has letterforms no free font matches, and the mismatch is obvious to anyone who knows the brand. Place the official lockup asset as a single image. The same applies to any pack design-language element.

Both are elaborated, with the incidents behind them, in [brand-fidelity-rules](https://github.com/anishadogra/brand-fidelity-rules).

## Configuration

Copy `production/brand-tokens.example.json` to `brand-tokens.json` and fill it in — palette, type ramp, per-line tokens, per-SKU tokens. It is gitignored. Templates reference `{{brand.name}}`, `{{product.line_a}}`, `{{brand.assets.lockup_primary}}`.

No client assets, palettes, product names or logos are included. The example token file keeps the structure and blanks every value.

## Requirements

The production stage drives Figma through an MCP `use_figma` tool. The research and synthesis stages are model prompts and are tool-agnostic. `scripts/strip_white_bg.py` needs Pillow. Publishing expects a sheet and an automation platform; the blueprint is included as a starting point.

MIT licensed.
