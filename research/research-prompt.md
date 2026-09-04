# Product Deep-Dive Research Prompt

Use this prompt to research any {{brand.name}} SKU (or topic) BEFORE writing any carousel copy. Output is a structured markdown doc that gets cached at `research/cache/<sku_slug>.md`.

The richer this layer, the punchier the final carousel can be. Don't skimp.

---

## Prompt template

> You are a senior food + culture researcher building intel for an Instagram carousel about **{PRODUCT_NAME}** — part of the **{LINE}** range from {{brand.name}}, a premium packaged-food brand with the Explorer archetype.
>
> The carousel will be 5 slides. Your research must give the copywriter so much rich, surprising, verifiable material that every line on every slide earns its place. No filler. No generic snack-marketing fluff.
>
> Produce a markdown doc with these EXACT sections. Be specific, be sourced, be unexpected.
>
> ## 1. Category context
> What broader category does this product live in? Name the category and two or three adjacent ones it is often confused with. Define it for someone who has never tried it. 2-3 sentences.
>
> ## 2. Cultural / historical roots
> Where does this category come from? Trace it across at least four cultures, giving the local name and a one-line description for each. For a flavour-specific SKU rather than a base product, do the same deep dive on that flavour's own origin instead.
>
> ## 3. Process / craft
> How is it actually made? Walk through 3–5 steps. What temperature, what time, what does the puff/render/cure look like? What separates a good version from a bad version? This is what differentiates premium from mass-market.
>
> ## 4. Nutritional truth (verified)
> Real macros per 100g (protein, fat, sat fat, carbs, sugar, sodium). What's surprising vs. what people assume? Compare to 2–3 reference foods (e.g. "more protein than chicken breast", "less carbs than potato chips"). Flag any false claims that competitors make.
>
> ## 5. Sensory profile
> Taste notes like a sommelier. Use 5–8 concrete sensory verbs (puff, snap, crackle, render, lift, shatter, cure, smoke, bloom, finish). Cover: aroma, first bite, mid-bite, finish, mouthfeel.
>
> ## 6. Pairing ideas (5+ options)
> What does this product eat well with? Cover drinks (beer, wine, whisky, cocktails), foods (salads, eggs, cheese boards, rice bowls), occasions (game day, hosting, road trip, post-gym).
>
> ## 7. Fun / surprising facts (8+ items)
> Things that make people stop scrolling. Give a mix of three kinds, each with a source:
> a nutrition surprise (a figure from the pack, compared against a familiar reference food);
> a cultural surprise (a tradition, festival or national day attached to the category);
> and a sensory surprise (something about how it is made that explains how it eats).
> Every claim carries its source. A hook you cannot source is not a hook, it is a liability.
>
> ## 8. Competitive context
> What is the category default, and what does this brand do differently? Name the shortcut most of the category takes, then state what this brand does instead and what it costs to do it that way. One sentence each, both sourced.
>
> ## 9. Hook angles (8+ candidates)
> Each hook is a candidate Slide 1 headline. Voice: bold, direct, sentence case, period-punctuated, concrete sensory. Examples:
> - "Meet [Product]."
> - "What is [Product]?"
> - "[Product] is older than you think."
> - "The [adjective] you've been missing."
> - "[Specific surprising claim]."
> - "[Sensory verb] [noun]."
> - "Wait — [Product] is [counterintuitive claim]?"
> - "[Number] reasons [Product] hits different."
>
> ## 10. Story connections (the through-line)
> Identify ONE story idea that could connect 5 slides into a single narrative. Specify how each slide picks up where the last left off. This is the spine the synthesis phase uses.
>
> ---
>
> Constraints:
> - Verify any claim with a source where possible (Wikipedia, NIH, USDA FoodData Central, food history books)
> - If you don't know, say "unverified" rather than make it up
> - British spelling
> - Don't use marketing-speak ("perfect", "ultimate", "amazing", "delicious"). Use sensory + factual language.

---

## How to invoke

1. Check `research/cache/<sku_slug>.md` first — if exists and < 90 days old, use it.
2. Otherwise: use Claude (or the WebSearch + WebFetch tools) with the prompt above.
3. Save the output to `research/cache/<sku_slug>.md`.
4. Pass to synthesis prompt next.
