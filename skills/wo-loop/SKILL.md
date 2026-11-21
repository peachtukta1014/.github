---
name: wo-loop
description: Boot a lane, then run the whole work-order loop — dispatch, board, pad, close, report, PR, exec. The single toolkit for working with other lanes. Use on "/boot <lane>", when ordering or closing work, or when a lane needs its identity, pad and board.
---

# wo-loop

ONE skill: **boot a lane, then run the work loop**. (Merged from `boot` + `wo-loop`, 2026-11-21.)

## 1. Boot — start here

```
WHERE  VM /opt/vault/vm-hq-core/bin/om-boot
RUN    wo-loop boot <scope>          (ws_exec opens the tunnel itself; falls back to ssh vm-ts)
READ   /opt/vault/vm-hq-core/70-Lanes/<scope>/SCOPE.md · PROTOCOL/00_INDEX.md
DON'T  no ls/find/md5 before boot · no om-sync during boot
```

Lane names: ปั้นแป้ง=code · ข้าวของ=files · เกมมิ่ง=gaming · เกี๊ยว=hokkien · จี้=jii · ข้าวเรียม=research · เวลา=scheduled · กุ้งทอง=seafood · ชาเย็น=tea · หมึกสาย=webhook

Unknown scope? `lane-id` resolves this chat session → lane
(bindings: `memory/config/session_bind.json`; offline card: `shared/lanes/<lane>.md`).

After boot report: identity loaded · pad tasks · board rows · what must be done now.
Scripts are symlinks to the single real copy — never duplicate them (RULE 11).

- **Which lane am I** → `references/lane-identity.md` (bindings → live identity from `70-Lanes/<lane>/identity/` → offline card).
- **The key to the VM** → `references/vm-key.md` (which local script lives where, which door to use).

## 2. VM-side command (`wo-loop <command>`)

```bash
ws_exec.py --command "wo-loop <command> --scope <lane> [options]"
```

| command | what it does |
|---|---|
| `boot <scope>` | identity + SCOPE + pad + board (one VM command) |
| `sp status --scope <lane>` | pad state for a lane |
| `sp update/note` | change active_job / status / next_action |
| `pad --lane <lane> --log "..." [--status] [--next-action]` | write the scratchpad |
| `item --lane <lane> --n <N> --status done --evidence "..."` | tick a checklist item |
| `close --lane <lane> --result "..." [--evidence] [--tick 1,2,3]` | close the WO + clear the board |
| `board [--scope <lane>]` | read the central board |
| `report --lane <lane> --title "..."` | render a Peach report |
| `pr <branch> <title> [body-file]` | commit + push + open PR |
| `exec "<command>"` | run a shell command on the VM |
| `render --lane <lane>` | re-render pad/board |

## 3. Device-side commands

```bash
# order work for another lane (cross-lane allowed, RULE 10)
python3 ws_dispatch.py --to <lane> --from <me> --reply-to <me> \
  --job WO-<lane>-<slug>-<YYYYMMDD>-01 --title "<one line>" --checklist "a,b,c"

# close your own work (RULE 2 — never edit the pad by hand)
python3 ws_complete.py --to <lane> --from <lane> --reply-to <origin> \
  --job <JOB> --summary "<what changed + proof>" --report-file <path.md>

# message only (no pad, no board)
python3 sse_dispatch.py --to <lane> --from <me> --job <JOB> --task reply \
  --type RESULT --params '{"text":"..."}'
```

## Rules

- **RULE 0 — ask before assuming.** Peach drives by voice; words are misspelled. Confirm what she means before searching or acting.
- Job id format is fixed: `WO-<lane>-<slug>-<YYYYMMDD>-NN`. Never invent another shape.
- One asset = one owner (`ASSIGNMENTS.md`). The skills repo is **shared (no owner)**; everything else belongs to a lane → dispatch, do not edit.
- Before touching a shared script or service: read `PROTOCOL/00_INDEX.md` for "depended on by", then `rg` the callers.
- No ACK/RESULT = the job is not done. The lane that took the order clears its own board row.
- Report to Peach in Thai: what → measurable result → risk → what she must decide.
- **SCRATCHPAD HARD RULE:** before ending any turn that did work, update the pad
  (`wo-loop pad --lane <lane> --log "..." --status "..." --next-action "..."`). If it is not on the pad, it did not happen.

## CI: do not poll (Peach 2026-11-14)

Open the PR and stop. The CI aggregator sends one event per outcome
(`PR #N is ready` + auto squash-merge, `PR #N has a problem: <check> <url>`, `deploy ...`).
Never run `gh pr checks` / `gh run watch` — wait for the event.

## Reference files (this folder)

| file | read it for |
|---|---|
| `references/lane-identity.md` | who this session is (lane-id, live identity, offline card) |
| `references/vm-key.md` | the device-side script map and which door to use |
| `references/routing.md` | lane routing / dispatch detail |
| `references/env.md` | environment and paths |

## Locator

```json
{
  "skill_file": "/srv/repos/skills-shared/skills/wo-loop/SKILL.md",
  "per_scope_detail": "/srv/repos/skills-shared/skills/wo-loop/<scope>/SKILL.md",
  "vm_wo_loop": "/usr/local/bin/wo-loop",
  "vm_pad": "/opt/vault/vm-hq-core/70-Lanes/<scope>/scratchpad.json",
  "vm_scope": "/opt/vault/vm-hq-core/70-Lanes/<scope>/SCOPE.md",
  "vm_board": "/opt/vault/vm-hq-core/mission-control/board/CENTRAL_WORK_BOARD.md",
  "assignments": "/opt/vault/vm-hq-core/30-System/ASSIGNMENTS.md",
  "protocol_map": "/opt/vault/vm-hq-core/PROTOCOL/00_INDEX.md",
  "dispatch": "ws_dispatch.py",
  "complete": "ws_complete.py",
  "message": "sse_dispatch.py",
  "board_read": "board_check.py",
  "ws_exec": "ws_exec.py"
}
```
