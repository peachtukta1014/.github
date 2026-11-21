# tools — which tool leads where

**Do not restate the catalogue here.** The canonical home is `30-System/TOOL_CATALOGUE.md`
(12 categories, each entry answering `leads where` / `what for` / `destination` / `how to call`).

Read it through the tunnel:
```
scripts/tool <intent>            # prints the 12 headings + matching rows
```

## The one rule
**One entrance, many categories — never per-channel tool sets.** Every lane already has equal
access to every tool (Peach 2026-11-21; `AGENT.md` access model: read = everyone, write = owner).
Splitting tools per channel would contradict that and create N copies to keep in sync.

## Loading tiers (this is how "do not load everything at once" is implemented)
| Tier | Loaded | Cost |
|---|---|---|
| A | the 12 category lines in the catalogue header | ~12 lines, always |
| B | the members of the category you are about to work in | on intent |
| C | `tool_registry` / `SSOT_INDEX.md` | only when stuck |

## When the catalogue and reality disagree
The catalogue is a **pointer layer**. It never gates execution: a miscategorised tool still runs.
Report the disagreement and fix the row — do not create a second table.
`bin/doc_drift.py` carries the catalogue<->`TOOLS.md` §2b.1 pair so a disagreement is announced.
