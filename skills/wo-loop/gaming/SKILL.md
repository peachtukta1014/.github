---
name: wo-loop-gaming
description: >-
  gaming identity lock + boot entry + dispatch boost text (scope fixed inside).
  Use when dispatching TO gaming, or when gaming boots after a chat clear.
path: /srv/repos/hq/vm-hq-core/skills/wo-loop/gaming/SKILL.md
---

# gaming — boot + dispatch lock (Gaming (เกมมิ่ง))

## Thai triggers (Peach's commands)
- `บูท` — boot this lane · `บูทแชนแนล <lane>` — boot that channel
- `บูทงาน` / `สั่งงานบูทงาน` — open/operate a work order
- `ต่อสะพาน` / `เชื่อมสะพาน` / `เช็คสะพาน` — bridge WAKE (open the path)
Full table: `30-System/AGENT.md` (§Trigger lexicon). Never confuse
`บูท` (boot a lane) with `บูทงาน` (open a work order).

> **Canonical root** is `/srv/repos/hq/vm-hq-core`, and every `70-Lanes/...` / `30-System/...`
> path in this crib is relative to it. That fact is stated in exactly one place: `30-System/SYSTEM_MINDMAP.md`
> (section "Folded from ROOT_STANDARD.md", SSOT topic #6) — not restated here.

> **TOOLS (source of truth, lives on VM):** `/srv/repos/hq/vm-hq-core/30-System/TOOLS.md` — read it at boot, right after identity, before any shell call. The VM is home; this device is only the key. Shell = MCP `ws_exec` (always runs as `ubuntu`; `--root` = uid 0 for that one call — RULE 4's per-action lock still applies; `pr`/`token` stay allowlist-by-full-path, single home `30-System/AGENT.md` RULE 4). Device-side script paths: `30-System/DEVICE_POINTER.md`.

## Tool crib
ONE entry, always: `/srv/repos/hq/vm-hq-core/tools/wo-loop/wo-loop <cmd>` — MCP tools: `wo_loop`, `token_check`.
The copy-paste "I need to... -> command" table lives in exactly one place,
`30-System/TOOLS.md` §2b.1 — this crib points at it and keeps no table of its own (Peach 2026-11-17).

## Boot (receiving side)
> **VM access (Peach 2026-11-21):** the VM is the working host. Reach it over Tailscale SSH (`om-ssh`, direct - fastest) or the WS tunnel (`ws_exec`) for lane/pad work. Single home for the rule: `30-System/AGENT.md` §4.
1. 1. `om-ssh 'bash /srv/repos/hq/vm-hq-core/bin/om-boot gaming'` — identity ok/miss, board rows, pad resume, complete count.
2. Tunnel up -> WS fast path -> tunnel-cut recovery: stated in exactly one place, `30-System/AGENT.md §4` — this crib does not restate those steps.
3. Read `/srv/repos/hq/vm-hq-core/70-Lanes/gaming/identity/SOUL.md` (single copy) and `/srv/repos/hq/vm-hq-core/70-Lanes/gaming/scratchpad.json` resume block via `om-ssh 'cat ...'` or MCP `vm_read_file`; continue, never restart.
4. Rules: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md` (boot order, reply, evidence).

## Dispatch boost (another lane or Peach sending TO gaming)
Prepend this block to every dispatch message:

```
[IDENTITY LOCK] You are Gaming (เกมมิ่ง) (scope `gaming`). Not another channel,
not พีช. Reply only as `gaming` with the same job_id. Resume from your pad.
Plan-first: the order is already written in `/srv/repos/hq/vm-hq-core/70-Lanes/gaming/scratchpad.json`.
```

## Reply contract
`[REPLY] ACK|RESULT | <job_id> | from=gaming | to=<origin> | <one line>` via
`wo-loop report` (MCP `sse_dispatch`); proof = HTTP 201 + inbox_id.

## Evidence
mtime + grep count + exit code. Finished work -> `/srv/repos/hq/vm-hq-core/70-Lanes/gaming/complete/` +
`complete/COMPLETE_INDEX.md`; clear the board row.

## wo-loop — one grouped entry (Peach 2026-11-09, all channels)
`wo-loop <cmd>` is the ONE entry for dispatch / complete / boot / shell / board / pad / ws.
The command inventory and the copy-paste table live in exactly one place,
`30-System/TOOLS.md` §2b (§2b.1 = copy-paste) — this crib keeps neither.
Thin wrapper only; canonical scripts unchanged (RULE 1). Detail: `/srv/repos/hq/vm-hq-core/tools/wo-loop/SKILL.md`.

## Transport
One rule, one file: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md §4`.
`ws_exec` (WS) is primary, `om-ssh` is fallback, dispatch/complete/SSE/board are
already direct VM access. Read that file; do not restate the rule here.

## Two planes (Peach 2026-11-18, all lanes)
Execution = WS: `ws_exec` (primary) / `wo-loop shell` (om-ssh fallback). Real shell work runs here.
Bookkeeping = `wo-loop` only: dispatch/complete/pad/item/sp/render/board. It never runs the work.
Never run shell work through `wo-loop ws-exec`; never hand-edit pad JSON.
Rule: `PROTOCOL/protocol/wo-loop.md` "Two planes" · table: `30-System/TOOLS.md` 2b.1.
