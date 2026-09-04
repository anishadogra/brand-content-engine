# Slide Template Library — 8 Archetypes

Each template defines the JSON shape that the Figma builders consume. All slides are 1080×1350.

## Common fields (every slide)

| Field | Required | Example |
|---|---|---|
| `template` | yes | `"hero"` |
| `name` | yes | `"PC1_S01_hero"` (carousel + slide-num + template) |
| `bg` | yes | `"cream"` (token name from brand-tokens.json) |
| `ink` | yes | `"burgundy"` (primary text colour) |
| `accent` | yes | `"red"` (emphasis colour for color-split + eyebrow) |
| `eyebrow` | yes | `"NEW IN THE BAG"` (uppercase letter-spaced) |

## Templates

### 1. `hero`
Slide 1 of every carousel. Eyebrow + colour-split headline + pack image card.
```json
{
  "template": "hero",
  "h1": "Meet",
  "h2": "Smoked\nPaprika.",
  "packHash": "<imageHash>",
  "packMode": "FILL",
  "cardBg": "light_blue",
  "pill": "SMOKED PAPRIKA · {{PRODUCT_LINE_A}}"
}
```
Notes: `h1` rendered in `ink`, `h2` in `accent` for split-colour effect. `pill` MUST NOT contain misleading "Xg".

### 2. `quote`
Big pull quote on dark BG. Carries a taste note or one-liner.
```json
{
  "template": "quote",
  "q": "Sweet-sour heat.\nIndian roots.",
  "attr": "{{brand.name}} Flavour Lab"
}
```

### 3. `proof`
Stat hero (e.g. `55g PROTEIN PER 100G`) + checklist of benefits.
```json
{
  "template": "proof",
  "h1": "Crunch that",
  "h2": "actually does\nsomething.",
  "stat": { "v": "55", "u": "g", "l": "PROTEIN PER 100G", "s": "Pure the whole-cut raw material. Nothing padded." },
  "checks": ["Keto-friendly","Zero carbs","Gluten free","Sugar free","No added MSG","Natural collagen"]
}
```

### 4. `difference`
2×2 grid of 4 numbered tenets. The "why us" slide.
```json
{
  "template": "difference",
  "h1": "Made properly,",
  "h2": "made here.",
  "tenets": [
    { "n": "01", "t": "One whole cut.", "b": "No reformed pieces, no filler." },
    { "n": "02", "t": "High protein.",  "b": "State the figure per 100g, from the pack." },
    { "n": "03", "t": "Bold flavours.", "b": "Built around the base, not over it." },
    { "n": "04", "t": "Made to standard.", "b": "Sourced and packed to an export spec." }
  ]
}
```

### 5. `recipe`
3-step pairing/serving idea. Use case slide.
```json
{
  "template": "recipe",
  "h1": "Three ways to",
  "h2": "crunch.",
  "steps": [
    { "n": "01", "t": "Cold beer.", "b": "A pale lager cuts the tang." },
    { "n": "02", "t": "Salad topper.", "b": "Crush over a kachumber." },
    { "n": "03", "t": "Straight from the bag.", "b": "Open. Bite. Repeat." }
  ]
}
```

### 6. `origin`
Story slide on dark BG. Headline left, body paragraphs right, 4 footer columns.
**CRITICAL:** Headline column width = 460, body column starts at x=540. Don't overlap.
```json
{
  "template": "origin",
  "h1": "A snack the",
  "h2": "world has\nloved for\ncenturies.",
  "body": [
    "A one-line category definition for someone who has never tried it: what it physically is, and how it is made.",
    "One line of provenance: how old the category is, and two or three cultures that have their own name for it."
  ],
  "cols": [
    { "l": "SPAIN",       "v": "Chicharrón" },
    { "l": "PHILIPPINES", "v": "Chicharon" },
    { "l": "THAILAND",    "v": "Kaep Moo" },
    { "l": "INDIA · NOW", "v": "{{product.line_a}}" }
  ]
}
```

### 7. `range`
Family / range showcase. Big family image card.
```json
{
  "template": "range",
  "h1": "Taste the",
  "h2": "crunch.",
  "familyHash": "<imageHash of group shot>"
}
```

### 8. `cta`
Last slide. Handle + tagline + sub. Footer reads the brand tagline ("{{brand.tagline}}") instead of "SWIPE →".
```json
{
  "template": "cta",
  "handle": "{{brand.handle}}",
  "tag": "MORE CRUNCH.",
  "sub": "New drops, recipes, and the obsessions behind every bag."
}
```
