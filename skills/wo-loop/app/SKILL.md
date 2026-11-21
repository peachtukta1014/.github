---
name: wo-loop-app
description: >-
  BOOT + identity lock for every channel. Trigger this whenever Peach says any of:
  "บูท", "บู๊ท", "บูทแป้ง", "บูทปั้นแป้ง", "ปั้นแป้ง", "บูทโค้ด", "boot code",
  "บูทจี้", "บูทกุ้งทอง", "บูทชาเย็น", "บูทหมึกสาย", "บูทเวลา", "บูทข้าวของ",
  "บูทข้าวเรียม", "บูทเกมมิ่ง", "บูทเกี๊ยว" — i.e. a boot word + a channel name
  (Thai or English), with or without "om-boot". Also use when dispatching work TO
  a scope (identity boost block) or when a channel boots after a chat clear.
---

# wo-loop — boot & identity lock (index)

## Thai triggers (Peach's commands)
- `บูท` — boot this lane · `บูทแชนแนล <lane>` — boot that channel
- `บูทงาน` / `สั่งงานบูทงาน` — open/operate a work order
- `ต่อสะพาน` / `เชื่อมสะพาน` / `เช็คสะพาน` — bridge WAKE (open the path)
Full table: `30-System/AGENT.md` (§Trigger lexicon). Never confuse
`บูท` (boot a lane) with `บูทงาน` (open a work order).
> **TOOLS (source of truth, lives on VM):** `/srv/repos/hq/vm-hq-core/30-System/TOOLS.md` — read it at boot, right after identity, before any shell call. The VM is home; this device is only the key. Shell = MCP `ws_exec` (always runs as `ubuntu`; `--root` = uid 0 for that one call — RULE 4's per-action lock still applies; `pr`/`token` stay allowlist-by-full-path, single home `30-System/AGENT.md` RULE 4). Device-side script paths: `30-System/DEVICE_POINTER.md`.


Peach commands by plain speech — no terminal. A message like **"บูทแป้ง"** in any
chat means: boot that lane, load its identity, resume its pad.

## 1. Trigger → scope (Thai / English)

| What Peach types | scope | boot command (VM) |
|---|---|---|
| บูทจี้ · จี้ · jii | `jii` | `om-boot jii` |
| บูทกุ้งทอง · กุ้งทอง · seafood | `seafood` | `om-boot seafood` |
| บูทชาเย็น · ชาเย็น · tea | `tea` | `om-boot tea` |
| บูทหมึกสาย · หมึกสาย · webhook | `webhook` | `om-boot webhook` |
| บูทเวลา · เวลา · scheduled | `scheduled` | `om-boot scheduled` |
| บูทข้าวของ · ข้าวของ · files | `files` | `om-boot files` |
| บูทข้าวเรียม · ข้าวเรียม · research | `research` | `om-boot research` |
| **บูทแป้ง · บูทปั้นแป้ง · ปั้นแป้ง · บูทโค้ด · code** | `code` | `om-boot code` |
| บูทเกมมิ่ง · เกมมิ่ง · gaming | `gaming` | `om-boot gaming` |
| บูทเกี๊ยว · เกี๊ยว · hokkien | `hokkien` | `om-boot hokkien` |

No channel named → ask one short question, or boot the lane this chat belongs to.

## 2. Boot (receiving side) — 4 steps, STATUS mode only

> **ROOT = `/srv/repos/hq/vm-hq-core`.** `/opt/vault` alone is NOT the root — it only
> holds `_archive/ backups/ vm-hq-core/`. Every `70-Lanes/…` and `30-System/…` path
> below is relative to that root.

1. `bash /srv/repos/hq/vm-hq-core/bin/om-boot <scope>` (full path — not on PATH over non-interactive SSH).
2. Read `/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/identity/SOUL.md`.
3. Read `/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/scratchpad.json` resume block; continue, never restart.
4. Rules: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md`.
Then answer in the lane's own voice, in Thai, with the evidence from step 1.

## 3. Dispatch boost (sending TO a scope)
Prepend to every dispatch message:

```
[IDENTITY LOCK] You are <Name> (scope `<scope>`). Not another channel,
not Peach. Reply only as `<scope>` with the same job_id. Resume from your pad.
Plan-first: the order is already written in `/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/scratchpad.json`.
```

## 4. Reply contract
`[REPLY] ACK|RESULT | <job_id> | from=<scope> | to=<origin> | <one line>` via
`wo-loop report` (MCP `sse_dispatch`); proof = HTTP 201 + inbox_id.

## 5. Evidence & close
mtime + grep count + exit code. Done → `/srv/repos/hq/vm-hq-core/70-Lanes/<scope>/complete/` +
`COMPLETE_INDEX.md`, clear the board row.

Per-scope full files (VM): `/srv/repos/hq/vm-hq-core/skills/wo-loop/<scope>/SKILL.md`.

## Transport
One rule, one file: `/srv/repos/hq/vm-hq-core/30-System/AGENT.md §4`.
`ws_exec` (WS) is primary, `om-ssh` is fallback, dispatch/complete/SSE/board are
already direct VM access. Read that file; do not restate the rule here.

## Two planes (Peach 2026-11-18, all lanes)
Execution = WS: `ws_exec` (primary) / `wo-loop shell` (om-ssh fallback). Real shell work runs here.
Bookkeeping = `wo-loop` only: dispatch/complete/pad/item/sp/render/board. It never runs the work.
Never run shell work through `wo-loop ws-exec`; never hand-edit pad JSON.
Rule: `PROTOCOL/protocol/wo-loop.md` "Two planes" · table: `30-System/TOOLS.md` 2b.1.
