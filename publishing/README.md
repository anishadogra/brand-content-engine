---
name: linkedin-image-auto-poster
description: Build a Make.com scenario that auto-posts pre-approved image posts to a LinkedIn Company Page on a schedule, driven by a Google Sheet queue and image files stored in Google Drive. Use whenever a user wants an automated LinkedIn posting pipeline where each row in a Sheet (caption + CTA + hashtags + a Drive image file) is published to a LinkedIn organization page, then the row is flagged "Posted". Client-agnostic — works for any brand, any org URN, any cadence. Encodes the exact blueprint, the column-index vs column-letter rule, the CSV→Sheet "Untitled" tab gotcha, the activate-before-run rule, and the supervised-test-then-deactivate safety gate.
---

# LinkedIn Image Auto-Poster (Make.com)

End-to-end skill for standing up a **scheduled, queue-driven LinkedIn image poster** on Make.com. The source of truth is a **Google Sheet** (one row = one post) plus **image files in Google Drive**. Make reads the next approved row, pulls its image from Drive, posts it to a LinkedIn **Company/Organization page**, and writes the result back to the Sheet.

**This skill is client-agnostic.** {{brand.name}} was the first build; the same machine works for any brand — only the org URN, sheet ID, Drive folder, connections, and cadence change. Do not bake client specifics into the reusable parts.

## When to invoke

- "Auto-post to LinkedIn from a Google Sheet / Drive"
- "Schedule LinkedIn company-page posts", "alternate-day LinkedIn poster", "content calendar → LinkedIn"
- Any Make.com scenario of the shape: **Sheet queue → Drive image → LinkedIn image post → mark row Posted**
- Building/repairing a scenario that posts `linkedin:CreateCompanyImagePost` from sheet data

## Architecture (4 modules, sequential)

```
[1] google-sheets:filterRows      → next row where Status = Approved (limit 1)
[2] google-drive:getAFile         → download image by Drive File ID from row
[3] linkedin:CreateCompanyImagePost → publish to org page (image = Drive binary)
[4] google-sheets:updateRow       → set Status=Posted, timestamp, post URL
```

Module IDs in the blueprint are `1, 3, 4, 5` (the Drive module is id `3`, LinkedIn is id `4`, updateRow is id `5`). Keep that numbering — the mappers reference `{{1.…}}` (sheet row) and `{{3.data}}` / `{{4.id}}`.

## The Google Sheet contract (14 columns, A–N)

Build the queue with **headers in row 1** and these columns. Make references them **by 0-based index** in mappers:

| Idx | Col | Field | Notes |
|-----|-----|-------|-------|
| 0 | A | Post ID | e.g. `LI-01` |
| 1 | B | Post Date | human-readable, display only |
| 2 | C | Product Line / Category | |
| 3 | D | Flavour / Theme | |
| 4 | E | Angle | |
| 5 | F | Title | used in LinkedIn post `title` field |
| 6 | G | Creative Filename | display + altText |
| 7 | H | **Drive File ID** | the image file id in Drive — drives module 2 |
| 8 | I | Caption | main body |
| 9 | J | CTA | appended after caption |
| 10 | K | Hashtags | appended last |
| 11 | L | **Status** | `Approved` → poster picks it up; becomes `Posted` |
| 12 | M | Posted Timestamp | written back by module 4 |
| 13 | N | Post URL | written back by module 4 |

Adapt column set per client, but **keep Status, Drive File ID, and the caption/CTA/hashtags trio**. If you change the column count, update `tableFirstRow` (e.g. `A1:N1`) everywhere.

## CRITICAL GOTCHAS (these cost real debugging time — do not relearn them)

1. **Column LETTER for the filter, column INDEX for everything else.**
   - `filterRows` filter uses the **letter**: `"filter":[[{"a":"L","b":"Approved","o":"text:equal"}]]`.
   - Every value mapper uses the **0-based index in backticks**: `{{1.`8`}}` is column I (Caption), `{{1.`11`}}` is Status. Mixing these up silently breaks mapping.

2. **A CSV converted to a Google Sheet does NOT have a tab named "Sheet1".**
   When you create the queue by uploading CSV with `contentMimeType:"text/csv"` (auto-converts to a Sheet), the single tab is usually named **"Untitled"**, not "Sheet1". Using the wrong `sheetId` fails with:
   `400 INVALID_ARGUMENT - Unable to parse range: 'Sheet1'!L2:L1000000`.
   **Discover the real tab name** with the Drive MCP `read_file_content` / `get_file_metadata` — the markdown output's first heading `# <TabName>` is the tab name. Set that exact string as `sheetId` in **both** module 1 (filterRows) and module 4 (updateRow). To avoid the guess entirely, prefer creating a **native** Google Sheet and naming the tab yourself, or rename the tab to a known value before wiring Make.

3. **A scenario must be ACTIVE before it can run.** `scenarios_run` on an inactive scenario returns `MakeError: Scenario is not activated`. Call `scenarios_activate` first, then `scenarios_run`.

4. **Activation does not fire immediately when the schedule is anchored to a future timestamp.** With `scheduling.between = ["<future>", null]`, activating just arms it — it won't post now. To test on demand, run `scenarios_run` with `responsive:true`.

5. **`scenarios_run` runs the WHOLE flow — a success = a real public post.** There is no cheap "module 1 only" test. If you must dry-test the sheet read without posting, temporarily point the Drive module (id 3) at an invalid file id so module 1 runs but module 3 fails before LinkedIn. Otherwise treat every run as live.

6. **updateRow needs `rowNumber:"{{1.`__ROW_NUMBER__`}}"`** to write back to the same row the filter found, plus `valueInputOption:"USER_ENTERED"` so the timestamp/URL render as text.

7. **"It keeps switching itself off" is almost always the org's monthly OPERATIONS budget, not a bug in this scenario.** Make operations are a single pool shared across ALL scenarios in the organization. When the org hits its monthly cap (e.g. 5,000 ops on the "Make Plan"), Make **auto-disables every active scenario** — the execution log shows a `stop` event with `authorName: null` / `authorId: null` (system, not a person). It does **not** auto-re-enable them after the monthly reset, so a scenario can sit dead for days until someone flips it back on. Diagnose with: `executions_list` (look for a null-author `stop`), then `organizations_get` (check `operations` vs `license.operations`, and `lastReset`/`nextReset`). This poster itself sips ~4 ops per post — it never exhausts the budget alone. The real culprits are **high-frequency pollers** (15-min `interval:900` scenarios = ~3k ops/month each). Prevention: keep idle pollers deactivated, and/or enable the org's auto-purchase of extra ops. A successful run shows `status:1`; a system-disable is a separate `stop` event — don't confuse the two.

   Related: when re-activating after any outage, Make sets `nextExec = activation time + interval`, which drifts the cadence off the intended grid. To restore a clean rhythm, reset `scheduling.between` to a fresh near-future anchor (`scenarios_update` with just the `scheduling` object) rather than re-sending the whole blueprint.

## Build workflow

1. **Audit available APIs first.** Confirm the three Make connections exist and are valid: Google Sheets, Google Drive, LinkedIn (each is an `__IMTCONN__` id). Confirm the LinkedIn connection is authorized for the target **organization** and you have its URN (`urn:li:organization:<id>`).
2. **Build the queue Sheet** in the client's Drive folder (14-col contract above), all rows `Status=Approved`. Confirm the real **tab name** (gotcha #2).
3. **Upload the creatives** to a Drive subfolder; capture each **Drive File ID** into column H. (Listing the folder via Drive MCP `search_files` with `parentId='<folder>'` returns the ids.)
4. **Create/patch the scenario** from `references/blueprint_template.json`. Fill the placeholders (see that file). Set scheduling: `type:"indefinitely"`, `between:["<first-run ISO+TZ>", null]`, `interval:<seconds>` (alternate-day = `172800`).
5. **Supervised test:** `scenarios_activate` → `scenarios_run` (`responsive:true`) → check `executions_get-detail` for SUCCESS → read the Sheet back and confirm the row flipped to `Posted` with a real `Post URL`.
6. **SAFETY GATE — `scenarios_deactivate` immediately after the test.** Do NOT leave the schedule live until the user has reviewed the live post and explicitly says go. Posting to a real public company page is high blast-radius; one supervised post ≠ permission to auto-run forever (see `feedback/Executing actions with care`).
7. **Hand off:** give the user the live post URL, the shareable Sheet link, and the Make scenario URL. Re-activate only on explicit go-ahead.

## Scenario URL format

`https://<zone>.make.com/<teamId>/scenarios/<scenarioId>/edit` (e.g. `https://eu2.make.com/1555422/scenarios/5914969/edit`). The zone (`eu1`/`eu2`/`us1`/`us2`) matches the org's Make region.

## Make MCP quick reference

- Server prefix: `mcp__21c06964-…__`
- `scenarios_get` (read blueprint), `scenarios_update` (patch blueprint — must send the FULL blueprint, not a diff), `scenarios_activate` / `scenarios_deactivate`, `scenarios_run` (`responsive:true` to run now), `executions_get-detail` (status).
- `scenarios_update` replaces the whole blueprint. Always `scenarios_get` first, edit the returned JSON, send it back intact.

## Optional: Telegram notifications (per-post ping + failure alert)

Clients usually want a "it posted" / "it broke" ping. **Prefer Telegram over CallMeBot WhatsApp** — CallMeBot is free but flaky (rotating activation numbers, 24h lockout if the key reply doesn't arrive in 2 min). Telegram's bot token is permanent and the send is a plain HTTP GET (1 op).

**Setup (token + chat id):**
1. User creates a bot via **@BotFather** → `/newbot` → gets a **token** like `8123456789:AA...`. Only the user can do this.
2. User opens the new bot and sends it any message (e.g. `hi`) — required before the bot can DM them.
3. Derive the **chat id**: GET `https://api.telegram.org/bot<token>/getUpdates` → read `result[].message.chat.id`.
   - **WebFetch caches 15 min per URL.** If `getUpdates` returns a stale empty `result`, bust the cache by changing the URL — append `?offset=-1&limit=10`.
4. Test: GET `https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>&text=<urlencoded>` → expect `{"ok":true}`.

**Wire into the scenario** — add as the LAST module (so a notify hiccup never blocks the post). Connectionless `http` app, no `__IMTCONN__`:
```json
{
  "id": 6, "module": "http:ActionSendData", "version": 3,
  "parameters": {"handleErrors": false, "useNewZLibDeCompress": true},
  "mapper": {
    "url": "https://api.telegram.org/bot<TOKEN>/sendMessage",
    "method": "get", "headers": [],
    "qs": [
      {"name": "chat_id", "value": "<CHAT_ID>"},
      {"name": "text", "value": "✅ Posted {{1.`0`}} · {{1.`5`}}\nhttps://www.linkedin.com/feed/update/{{4.id}}/"}
    ]
  },
  "metadata": {"designer": {"x": 1200, "y": 0}}
}
```
Make URL-encodes `qs` values (emoji, newline, the dynamic `{{…}}` tokens) automatically — don't pre-encode them in the blueprint.

**Failure alerting — know the two distinct cases:**
- **Run error** (LinkedIn API rejects, Drive file missing, etc.): catch with a Make **error handler** (`onerror` route on the LinkedIn/Drive module → a Telegram `http` module). This fires only when a module throws during a run.
- **Silent stop** (the ops-cap auto-disable from gotcha #7): the scenario does **not** run, so no error handler fires. Detect this with an **external heartbeat** (e.g. a cron on the user's machine, or an uptime monitor) — an in-org watchdog scenario would be killed by the same ops cap. Make also emails the org owner when operations run out; make sure that notification is on.

## Reusable assets

- `references/blueprint_template.json` — the full 4-module blueprint with `<<PLACEHOLDER>>` tokens.
- `references/sheet_schema.md` — the column contract + a header row you can paste/CSV.
