# known-drift — live defects reflex knows about, and their fix

Append here when a defect is found. Never delete an entry that is still unfixed; mark it FIXED
with the date instead. This file is the reason a lane does not have to rediscover a break.

| # | Defect | Status | Fix / proof |
|---|---|---|---|
| 1 | Six doc ids pointed at MOVED stubs after the 2026-11-21 consolidation: `boot.order`, `rule.shared`, `rule.priv`, `rule.lane`, `map.tool`, `wire.transport` | **FIXED 2026-11-21 15:31** | re-pointed in `registry/docids.json` (5 -> `AGENT.md` incl. `rule.priv` #RULE 4, `map.tool` -> `TOOLS.md`), then `gen_docmap.py --write`. Proof: `scripts/check` -> `bad=0 / total=15` |
| 2 | `bin/om-boot` printed those six ids as read-on-demand, so every boot resolving them got a stub | **FIXED** by #1 | same |
| 3 | Two spellings of the VM root (`/opt/vault/...` symlink vs `/srv/repos/hq/...` real) | **OPEN** | declare `/srv/repos/hq/vm-hq-core` canonical; never print the symlink form |
| 4 | `gen_docmap.py` returns rc=0 without `--write`, writing nothing | **OPEN (by design, but a trap)** | always pass `--write`; verify by **mtime**, not exit code |
| 5 | 16 T1 doc ids are over their 80-line budget and stay `OVER` | **OPEN** | decide per id: shorten the entry, or raise the budget with a reason |
| 6 | `find <dir> -type f` returns 0 on this VM while the tree is full | **KNOWN** | never use `find`; use `rg --files` |
| 7 | `bin/control_watch` / a doc-id-stub check is NOT in the linter set, so #1 was invisible to every checker | **OPEN** | add `scripts/check` to CI (`reflex` step 15) |

## Why this list exists
Defect #1 was live for hours: `om-boot` offered six ids that resolved to stubs. No existing
checker caught it — `check_surfaces`, `ssot_check`, `chain_index`, `gen_ssot_index` and
`identity_check` were all green. **A pointer can rot while every gate stays green**, which is
exactly what `scripts/check` is for.
