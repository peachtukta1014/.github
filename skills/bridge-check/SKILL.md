---
name: bridge-check
description: "Probe the VM bridge and, when it is down, run the ONE opener. Use when the app was suspended, a tunnel died, queued events stopped flowing, or Peach says เช็คสะพาน / ต่อสะพาน / เชื่อมสะพาน."
---

# bridge-check

Two halves, one skill. **Probe** answers "is the path alive?"; **opener** reopens it. Neither
writes a pad, a room or a work order — the bridge carries messages, it does not hold state.

## What is alive today (2026-11-27)

| half | where it runs | how you call it | what you get |
|---|---|---|---|
| probe | VM | MCP tool `bridge_check` (server `minis-tools`) or `tools/bin/bridge-check` | JSON `{"bridge":"ok"}` plus `hq_core`, `services`, `mesh_heartbeat`, `lanes` |
| opener | device | MCP tool `bridge_open_event` (device tool, registry `registry/device_tools.json`) | its own verdict line: `healthy; no action`, `HEALED: …`, or `FAILED rc=…` |
| opener, from the VM | VM | `bin/device_run.py --tool bridge_open_event` | the same verdict (P14: a tool is named, never a device path) |

`bridge_check` acking is **not** proof that events flow: the probe can be green while the session
is asleep. The opener is what makes a sleeping session wake.

## When to run

Run **once** when any of these is true:

- the app was backgrounded or killed and the chat went quiet;
- a wake alert arrived in the inbox;
- the WS tunnel or the SSE path stopped delivering events;
- Peach asks to check / reopen the bridge.

Do not run it on a timer, and do not run it twice to be sure.

## The four steps

1. **Probe.** Call `bridge_check`. Read all four sub-checks, not just `bridge`.
   - `lanes.missing_pad` non-empty → a lane has no pad: that is a data problem, not a bridge problem; report it, do not fix it here.
   - `services` with anything not `active` → name the service and stop; a dead service is not healed by an opener.
2. **Decide.** Everything green → report `bridge healthy; no action` and stop. Nothing else to do.
3. **Open.** Something is down → call the opener **once** (`bridge_open_event`, or `bin/device_run.py --tool bridge_open_event` from the VM). Use its verdict verbatim.
4. **Report.** One line with the verdict and the probe you ran after it. If the opener failed, give the exact `FAILED rc=…` and the probe field that is still red — never a guess.

## Verdicts you may report

- `bridge healthy; no action` — probe green, nothing was done.
- `HEALED: <what the opener said>` — the opener ran and the path is up.
- `FAILED: <exact opener line>` — the opener ran and did not heal it. Do not retry in the same turn.
- `UNKNOWN: probe unavailable` — the probe itself could not run (VM unreachable). Stop and say so.

## Never

- Never retry in a loop or start a keep-alive daemon: the opener is one shot by design.
- Never claim healthy without fresh probe output from this turn.
- Never write a pad, a room entry or a work order as part of a bridge check.
- Never invent a host, URL, token or device path — the registry is the only place those live
  (`registry/transports.json`, `registry/device_tools.json`).

## What to leave behind

Nothing durable: a wake is an operation, not a fact. If the path kept dying, that is a lesson for
the room (`bin/room post team --from <lane> --kind note "…"`) — not a pad entry and not a new file.
