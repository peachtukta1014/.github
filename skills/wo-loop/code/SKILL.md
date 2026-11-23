---
name: wo-loop-code
description: >-
  code identity lock + boot entry + dispatch boost text (scope fixed inside).
  Use when dispatching TO code, or when code boots after a chat clear.
---

# code — boot + dispatch lock (PunPaeng (ปั้นแป้ง))

## Thai triggers (Peach's commands)
- `บูท` — boot this lane · `บูทแชนแนล <lane>` — boot that channel
- `บูทงาน` / `สั่งงานบูทงาน` — open/operate a work order
- `ต่อสะพาน` / `เชื่อมสะพาน` / `เช็คสะพาน` — bridge WAKE (open the path)
Full table: `30-System/AGENT.md` (§Trigger lexicon). Never confuse
`บูท` (boot a lane) with `บูทงาน` (open a work order).

> **ROOT** = `/srv/repos/hq/vm-hq-core` — the root rule itself has one home: `30-System/SYSTEM_MINDMAP.md` (sec Folded from ROOT_STANDARD.md), which SSOT_INDEX topic 6 names as canonical. Not restated here.
> Every `70-Lanes/...` and `30-System/...` path is relative to that root.

> **TOOLS (source of truth, lives on VM):** `/srv/repos/hq/vm-hq-core/30-System/TOOLS.md` — read it at boot, right after identity, before any shell call. The VM is home; this device is only the key. Shell = MCP `ws_exec` (always runs as `ubuntu`; `--root` = uid 0 for that one call — RULE 4's per-action lock still applies; `pr`/`token` stay allowlist-by-full-path, single home `30-System/AGENT.md` RULE 4). Device-side script paths: `30-System/DEVICE_POINTER.md`.



## Boot (receiving side)

The VM is the execution and durable-state authority. Resolve the logical capability through `registry/transports.json`; do not assume a device path, a gateway, or a fixed primary/fallback route.

1. Run `wo-loop boot code` after resolving this session with `lane-id`.
2. Read only the identity, scope, protocol, pad, and board paths returned by boot.
3. Continue from the VM-owned pad; never restart or hand-edit pad JSON.
4. Read `30-System/AGENT.md` and `30-System/TOOLS.md` for current rules and capability routing.
## Dispatch boost (another lane or Peach sending TO code)
Prepend this block to every dispatch message:

```
[IDENTITY LOCK] You are PunPaeng (ปั้นแป้ง) (scope `code`). Not another channel,
not พีช. Reply only as `code` with the same job_id. Resume from your pad.
Plan-first: the order is already written in `/srv/repos/hq/vm-hq-core/70-Lanes/code/scratchpad.json`.
```

## Reply contract
`[REPLY] ACK|RESULT | <job_id> | from=code | to=<origin> | <one line>` via
`wo-loop report` (MCP `sse_dispatch`); proof = HTTP 201 + inbox_id.

## Evidence
mtime + grep count + exit code. Finished work -> `/srv/repos/hq/vm-hq-core/70-Lanes/code/complete/` +
`complete/COMPLETE_INDEX.md`; clear the board row.

## wo-loop — one logical lifecycle entry

Use `wo-loop` for boot, dispatch, complete, pad, item, sp, board, report, and PR preparation. The registered adapter may transport the request, but VM pads, boards, repositories, services, and durable work-order state remain VM-owned. Do not call implementation files directly or duplicate them.
## Transport

Resolve transport by capability, not by a fixed fallback claim:

- WS is primary for lifecycle, dispatch/complete automation, and small/structured commands.
- Tailscale direct SSH is primary for bulk, large, raw, and interactive operations.
- IAP is compatibility-only.
- `vm-hq-gate` is the primary typed VM gateway; `minis-tools` is a device/WS adapter and transitional entrypoint.

If live registration, path, or SHA is not verified, keep the command logical and state `runtime verification pending`.
## Two planes

Execution uses the capability-resolved VM route and bounded commands. Bookkeeping uses `wo-loop` only: dispatch, complete, pad, item, sp, render, board, and report. `wo-loop` is not a generic shell substitute. `bridge-check` is limited to health, recovery, and push-wake; it never owns work-order state.

Before ending a turn that changed work, update the VM-owned pad and report fresh evidence. Never claim completion without evidence.
