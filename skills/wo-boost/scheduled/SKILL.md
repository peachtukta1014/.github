---
name: wo-boost-scheduled
description: >-
  scheduled identity lock + boot entry + dispatch boost text (scope fixed inside).
  Use when dispatching TO scheduled, or when scheduled boots after a chat clear.
path: /var/minis/shared/skills/wo-boost/scheduled/SKILL.md
---

# scheduled — boot + dispatch lock (Wela (เวลา))

## Thai triggers (Peach's commands)
- `บูท` — boot this lane · `บูทแชนแนล <lane>` — boot that channel
- `บูทงาน` / `สั่งงานบูทงาน` — open/operate a work order
- `ต่อสะพาน` / `เชื่อมสะพาน` / `เช็คสะพาน` — bridge WAKE (open the path)
Full table: `30-System/CHANNEL_SHARED_RULES.md` (§Trigger lexicon). Never confuse
`บูท` (boot a lane) with `บูทงาน` (open a work order).
- **Trigger lexicon — single home:** `30-System/CHANNEL_SHARED_RULES.md` — section Trigger lexicon.

> Every `70-Lanes/...` and `30-System/...` path is relative to that root.

> **TOOLMAP (source of truth, lives on VM):** `/opt/vault/vm-hq-core/30-System/TOOLMAP.md` — read it at boot, right after identity, before any shell call. The VM is home; this device is only the key. Shell = MCP `ws_exec` (always runs as `ubuntu`; root mode retired 2026-11-17 — privileged calls go over SSH: `wo-loop shell "sudo -n <allowlisted script>"`, single home `30-System/CHANNEL_SHARED_RULES.md` RULE 4). Device-side script paths: skill `vm-key` (`/var/minis/skills/vm-key/SKILL.md`).

## Boot (receiving side)
> **Mandatory VM shell pattern — ALL VM shell use, not only boot (Peach 2026-11-08):** ssh once to open the VM door + WS tunnel (14301→4301), then use `ws_dispatch` (WS-VM direct) as the primary fast path for all boot/shell work. If the tunnel/port drops, run one `om-ssh` round to reopen, then resume WS. Never use bare `om-boot` on this device — no `om-boot` on PATH here.
1. First round (ssh): `/var/minis/shared/tools/bin/om-ssh 'bash /opt/vault/vm-hq-core/bin/om-boot scheduled'` — identity ok/miss, board rows, pad resume, complete count.
- **Boot protocol — single home:** `30-System/AGENT_BOOT.md`; tool map: `30-System/TOOLMAP.md`. Never restate either here.
5. Read `/opt/vault/vm-hq-core/70-Lanes/scheduled/identity/SOUL.md` (single copy) and `/opt/vault/vm-hq-core/70-Lanes/scheduled/scratchpad.json` resume block via `om-ssh 'cat ...'` or MCP `vm_read_file`; continue, never restart.
6. Rules: `/opt/vault/vm-hq-core/30-System/CHANNEL_SHARED_RULES.md` (boot order, reply, evidence).

## Dispatch boost (GM sending TO scheduled)
Prepend this block to every dispatch message:

```
[IDENTITY LOCK] You are Wela (เวลา) (scope `scheduled`). Not another channel, not the GM,
not พีช. Reply only as `scheduled` with the same job_id. Resume from your pad.
Plan-first: the order is already written in `/opt/vault/vm-hq-core/70-Lanes/scheduled/scratchpad.json`.
```

## Reply contract
`[REPLY] ACK|RESULT | <job_id> | from=scheduled | to=<origin> | <one line>` via
`/var/minis/shared/tools/bin/sse_dispatch.py`; proof = HTTP 201 + inbox_id.

## Evidence
mtime + grep count + exit code. Finished work -> `/opt/vault/vm-hq-core/70-Lanes/scheduled/complete/` +
`complete/COMPLETE_INDEX.md`; clear the board row.

## wo-loop — one grouped entry (Peach 2026-11-09, all channels)
Dispatch / complete / boot / shell / board / ws all go through ONE wrapper:
`/var/minis/shared/tools/wo-loop/wo-loop` (VM mirror: `/opt/vault/vm-hq-core/tools/bin/wo-loop/wo-loop`).
`wo-loop dispatch` = the MAIN ORDER PATH; `wo-loop complete` = the MAIN CLOSE PATH
(self-close per RULE 2 of CHANNEL_SHARED_RULES); `wo-loop boot` = channel boot
(`om-boot` is VM-only); `wo-loop shell` = VM shell via om-ssh; `wo-loop board` =
read-only status; `wo-loop ws` = WS-VM direct fast path. Thin wrapper ONLY —
canonical scripts unchanged (RULE 1). Details: `/var/minis/shared/tools/wo-loop/SKILL.md`.

## Transport
One rule, one file: `/opt/vault/vm-hq-core/30-System/TRANSPORT_WS_FIRST.md`.
`ws_exec` (WS) is primary, `om-ssh` is fallback, dispatch/complete/SSE/board are
already WS-first. Read that file; do not restate the rule here.
