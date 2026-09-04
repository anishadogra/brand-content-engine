# Queue Sheet Schema — LinkedIn Image Auto-Poster

One row = one scheduled LinkedIn post. **Headers in row 1.** Make references columns by **0-based index** in mappers (the index is shown below), and by **column letter** only inside the `filterRows` filter.

| Index | Col | Header | Purpose | Written by |
|-------|-----|--------|---------|-----------|
| 0 | A | Post ID | stable id, e.g. `LI-01` | you |
| 1 | B | Post Date | display only (the schedule controls timing, not this) | you |
| 2 | C | Product Line / Category | optional taxonomy | you |
| 3 | D | Flavour / Theme | optional taxonomy | you |
| 4 | E | Angle | optional taxonomy | you |
| 5 | F | Title | LinkedIn post `title` | you |
| 6 | G | Creative Filename | display + `altText` + `fileName` | you |
| 7 | H | **Drive File ID** | image to download (module 2) | you |
| 8 | I | Caption | post body (1st block) | you |
| 9 | J | CTA | post body (2nd block) | you |
| 10 | K | Hashtags | post body (3rd block) | you |
| 11 | L | **Status** | `Approved` = eligible; flips to `Posted` | you / module 4 |
| 12 | M | Posted Timestamp | run time in target TZ | module 4 |
| 13 | N | Post URL | live LinkedIn permalink | module 4 |

## Paste-ready header row (CSV)

```
Post ID,Post Date,Product Line,Flavour / Theme,Angle,Title,Creative Filename,Drive File ID,Caption,CTA,Hashtags,Status,Posted Timestamp,Post URL
```

## Notes

- The poster picks the **first** row with `Status = Approved` (limit 1) each run, oldest-first by sheet order.
- The LinkedIn body is assembled as `Caption\n\nCTA\n\nHashtags`. Keep each field clean — Make joins them.
- If you add/remove columns, change `tableFirstRow` (`A1:N1`) in BOTH sheet modules and re-index every `{{1.`N`}}`.
- Tab name: if the Sheet was created by converting a CSV, the tab is typically **`Untitled`**, not `Sheet1`. Confirm before wiring (see SKILL.md gotcha #2).
