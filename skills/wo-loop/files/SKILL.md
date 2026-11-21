---
name: wo-loop-files
description: >-
  files identity lock + boot entry + dispatch boost text (scope fixed inside).
  Use when dispatching TO files, or when files boots after a chat clear.
path: /srv/repos/hq/vm-hq-core/skills/wo-loop/files/SKILL.md
---

# files — boot + dispatch lock (KhaoKong (ข้าวของ))

## Thai triggers (Peach's commands)
- `บูท` — boot this lane · `บูทแชนแนล <lane>` — boot that channel
- `บูทงาน` / `สั่งงานบูทงาน` — open/operate a work order
- `ต่อสะพาน` / `เชื่อมสะพาน` / `เช็คสะพาน` — bridge WAKE (open the path)
Full table: `30-System/AGENT.md` (§Trigger lexicon). Never confuse
`บูท` (boot a lane) with `บูทงาน` (open a work order).

> **ROOT = `/srv/repos/hq/vm-hq-core`** — the root rule is stated in exactly one place: `30-System/SYSTEM_MINDMAP.md` (§ Folded from ROOT_STANDARD.md); `30-System/SYSMAP_AGENT.md` keeps the path map. Every path in this crib is relative to that root.

> **TOOLS (source of truth, lives on VM):** `/srv/repos/hq/vm-hq-core/30-System/TOOLS.md` — read it at boot, right after identity, before any shell call. The VM is home; this device is only the key. Shell = MCP `ws_exec` (always runs as `ubuntu`; `--root` = uid 0 for that one call — RULE 4's per-action lock still applies; `pr`/`token` stay allowlist-by-full-path, single home `30-System/AGENT.md` RULE 4). Device-side script paths: `30-System/DEVICE_POINTER.md`.



## Boot (receiving side)
> **VM access (Peach 2026-11-21):** the VM is the working host. Reach it over Tailscale SSH (`om-ssh`, direct - fastest) or the WS tunnel (`ws_exec`) for lane/pad work. Single home for the rule: `30-System/AGENT.md` §4.
1. 1. `om-ssh 'bash /srv/repos/hq/vm-hq-core/bin/om-boot files'` — identity ok/miss, board rows, pad resume, complete count.
2. WS transport — tunnel up / fast path / tunnel cut: single home `30-System/AGENT.md §4`. Follow it there; never restate the steps in this crib.
3. Read `/srv/repos/hq/vm-hq-core/70-Lanes/files/identity/SOUL.md` (single copy) and `/srv/repos/hq/vm-hq-core/70-Lanes/files/scratchpad.json` resume block via `om-ssh 'cat ...'` or MCP `vm_read_file`; continue, never restart.
4. Rules: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md` (boot order, reply, evidence).

## Dispatch boost (another lane or Peach sending TO files)
Prepend this block to every dispatch message:

```
[IDENTITY LOCK] You are KhaoKong (ข้าวของ) (scope `files`). Not another channel,
not พีช. Reply only as `files` with the same job_id. Resume from your pad.
Plan-first: the order is already written in `/srv/repos/hq/vm-hq-core/70-Lanes/files/scratchpad.json`.
```

## Reply contract
`[REPLY] ACK|RESULT | <job_id> | from=files | to=<origin> | <one line>` via
`wo-loop report` (MCP `sse_dispatch`); proof = HTTP 201 + inbox_id.

## Evidence
mtime + grep count + exit code. Finished work -> `/srv/repos/hq/vm-hq-core/70-Lanes/files/complete/` +
`complete/COMPLETE_INDEX.md`; clear the board row.

## wo-loop — one grouped entry (Peach 2026-11-09, all channels)
Dispatch / complete / boot / shell / board / ws all go through ONE wrapper:
`/srv/repos/hq/vm-hq-core/tools/wo-loop/wo-loop` (VM mirror: `/srv/repos/hq/vm-hq-core/tools/bin/wo-loop/wo-loop`).
`wo-loop dispatch` = the MAIN ORDER PATH; `wo-loop complete` = the MAIN CLOSE PATH
(self-close per RULE 2 of AGENT.md); `wo-loop boot` = channel boot
(`om-boot` is VM-only); `wo-loop shell` = VM shell via om-ssh; `wo-loop board` =
read-only status; `wo-loop ws` = ws_exec fast path. Thin wrapper ONLY —
canonical scripts unchanged (RULE 1). Details: `/srv/repos/hq/vm-hq-core/tools/wo-loop/SKILL.md`.

## Transport
One rule, one file: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md §4`.
`ws_exec` (WS) is primary, `om-ssh` is fallback, dispatch/complete/SSE/board are
already direct VM access. Read that file; do not restate the rule here.

## Two planes (Peach 2026-11-18, all lanes)
Execution = WS: `ws_exec` (primary) / `wo-loop shell` (om-ssh fallback). Real shell work runs here.
Bookkeeping = `wo-loop` only: dispatch/complete/pad/item/sp/render/board. It never runs the work.
Never run shell work through `wo-loop ws-exec`; never hand-edit pad JSON.
Rule: `PROTOCOL/protocol/wo-loop.md` "Two planes" · table: `30-System/TOOLS.md` 2b.1.
