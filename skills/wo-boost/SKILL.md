---
name: wo-boost
description: Work-order skill (dispatch / ACK / close). LOCATOR FIRST — commands are final, do not search.
---

# wo-boost

```json
{
  "locator": {
    "skill_file": "/var/minis/skills/wo-boost/SKILL.md",
    "per_scope_detail": "/var/minis/shared/skills/wo-boost/<scope>/SKILL.md",
    "dispatch": "/var/minis/shared/tools/bin/ws_dispatch.py",
    "complete": "/var/minis/shared/tools/bin/ws_complete.py",
    "message": "/var/minis/shared/tools/bin/sse_dispatch.py",
    "board_read": "/var/minis/shared/tools/bin/board_check.py",
    "vm_board": "/srv/repos/hq/vm-hq-core/mission-control/board/CENTRAL_WORK_BOARD.md",
    "vm_pad": "/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/scratchpad.json",
    "vm_scope": "/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/SCOPE.md",
    "protocol_map": "/srv/repos/hq/vm-hq-core/PROTOCOL/00_INDEX.md",
    "assignments": "/srv/repos/hq/vm-hq-core/30-System/ASSIGNMENTS.md"
  }
}
```

## The only three commands

```bash
# 1) order work for another lane (cross-lane allowed, RULE 10)
python3 /var/minis/shared/tools/bin/ws_dispatch.py --to <lane> --from <me> --reply-to <me> \
  --job WO-<lane>-<slug>-<YYYYMMDD>-01 --title "<one line>" --checklist "a,b,c"

# 2) close your own work (RULE 2 — never edit the pad by hand)
python3 /var/minis/shared/tools/bin/ws_complete.py --to <lane> --from <lane> --reply-to <origin> \
  --job <JOB> --summary "<what changed + proof>" --report-file <path.md>

# 3) message only (no pad, no board)
python3 /var/minis/shared/tools/bin/sse_dispatch.py --to <lane> --from <me> --job <JOB> --task reply \
  --type RESULT --params '{"text":"..."}'
```

## Rules for this skill

- Job id format is fixed: `WO-<lane>-<slug>-<YYYYMMDD>-NN`. Never invent another shape.
- One asset = one owner (`ASSIGNMENTS.md`). If the work belongs to another lane, dispatch it — do not edit their files.
- Before touching a shared script or service: read `PROTOCOL/00_INDEX.md` for "depended on by", then `rg` the callers.
- No ACK/RESULT = the job is not done. The lane that took the order clears its own board row.
- Report to Peach in Thai: what → measurable result → risk → what she must decide.

## CI: do not poll (Peach 2026-11-14)

Open the PR and stop. The CI aggregator sends one event per outcome
(`PR #N is ready` + auto squash-merge, `PR #N has a problem: <check> <url>`, `deploy ...`).
Never run `gh pr checks` / `gh run watch` / delivery re-reads to watch for green — wait for the
event. Read GitHub only when an event says something failed and you need that job's log.
