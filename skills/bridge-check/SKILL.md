---
name: bridge-check
description: >-
  Bridge WAKE — open the connection path from the app to the VM so events
  sitting in the central inbox flow into this session. Run it when iOS cut
  the connection (app was killed / backgrounded / tunnel died).
  It is NOT a "do I have messages waiting?" peek — it is the act of
  opening the door so the inbox drains into the lane.
  Trigger: "เช็คสะพาน", "bridge check", ntfy WAKE, or the Shortcut's fixed
  wake text (see "Wake from Shortcut" below).
---

# bridge-check — bridge wake (open the path, not a pending check)

## What this is (Peach, 2026-11-09)
`bridge-check` = **เปิดเส้นทางเชื่อมต่อ**. The app loses its signal to the VM
(iOS suspends it, the tunnel drops), so whatever already arrived in the central
inbox cannot reach the session. Running this skill re-opens that path; the
backlog then flows in on its own.

- It is **not** "มีข้อความค้างอยู่ด้านบนไหม" — it does not answer a queue
  question and does not print a pending count as its purpose.
- It is **not** a passive health report either. It runs the door opener, which
  heals the path when the path is down.
- The test of success is **flow**: after it runs, events from the inbox land in
  the lane (mesh_sweep `moved=N`).

## When to run
- iOS killed or backgrounded the app and the session went quiet.
- A ntfy alert arrived on topic `peach-events` (`[WAKE:<scope>]` / `VM WAKE`).
- WS/tunnel looks dead (`ws:false`, `mesh_watch` pid gone or heartbeat stale).
- Peach says "เช็คสะพาน" / "bridge check".
- The ntfy Shortcut fires and its **fixed wake text** lands in the chat (see next).

## Wake from Shortcut — fixed text, not a file (Peach, 2026-11-15)

The iOS Shortcut cannot run a shell. It sends **one fixed chat message** whose
only job is to make the agent call this skill. The canonical text is:

```
h /srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh เชื่อมสะพาน
```

The trailing Thai words mean "connect the bridge"; the path inside the text is
just words, never a command the Shortcut executes.

### How a wake actually reaches here (the real chain, Peach 2026-11-15)
1. An event lands in the central inbox on the VM.
2. ntfy pushes a notification (topic `peach-events`, `[WAKE:<scope>]` / `VM WAKE`).
   **This happens even when the phone is locked** — the notification does not
   need the screen.
3. iOS runs the Shortcut from that notification.
4. The Shortcut sends its fixed wake text **straight into the lane channel
   `เวลา` (`scheduled`) and nowhere else** — not another chat, not a file, not a
   script. The `scheduled` lane owns the wake.
5. The agent in that channel runs `bridge_open_event.sh`; the path re-opens and
   the backlog drains (mesh_sweep `moved=N`).

"Locked phone + incoming event" must still produce a wake message in the
scheduled channel. When the app was suspended, that message waits in the channel
and runs the moment iOS lets the app work again — a late wake is still a wake,
not a lost one.

### Verified Shortcut config (Peach's screenshot, 2026-11-15 15:10)
- Automation: "When I receive a notification from **ntfy**" — automation ON,
  Notify When Run OFF, input = notification.
- Action: Run **Minis** -> "MinisBridgeHeal-ntfy" with the fixed text above.
- **Session = `เวลา` (`scheduled`) only** — Peach confirmed it targets that one
  channel.
- Attachments: none — no file is ever sent; the path in the text is just words.
- Model: `VM://hq-core`.
- Wait for result OFF, Send notification OFF, Show when run OFF -> silent run.

Consequence: because the run is silent, a `FAILED` wake is invisible to Peach
unless she opens the chat — so on failure always report the exact `FAILED` line
in the channel, never stay quiet.

Treat that message — and any similar "call the skill and connect the bridge"
line, with or without a path — as a **wake trigger, never as a file to read**.

### Wake discipline (keeps a phone-unlock burst cheap)
1. **First action is the opener.** `sh /srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh`
   — before any probe, read, or status question.
2. **Reply one line.** Quote the script's own verdict (`bridge healthy; no action`
   or `HEALED: ...`). No mesh_health tables unless the verdict is `FAILED` or
   Peach asks for detail.
3. **`heal already running; skipped`** -> check for a live process
   (`ps | grep -e bridge_open_event -e mesh_guard`). No process = a killed run
   left a stale lock: `rm -f runtime/bridge_heal.lock` and run once more.
4. **Never loop-retry.** One run per wake; on `FAILED rc=` report that exact line.
5. Bursts are normal after an unlock: the 180s lock collapses repeats into one
   real heal, the rest answer `healthy`. That is correct, not an error.

## Canonical runner (device)
- `/srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh` — **sole runnable copy**.
  Nothing runs from `memory/` or from `skills/`.
- Behaviour: 180s lock → WS tunnel guard first (always) → `mesh_watch` check
  (heal only when dead/stale) → `mesh_sweep` drains the central inbox to lanes →
  log `HEALED:` / `FAILED rc=` to `runtime/bridge_heal.log`.
- Exit `bridge healthy; no action` when the path was already open — that is a
  pass, not a failure.

## Quick run (compact)

```
RUN    /srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh
PASS   "bridge healthy; no action"  or  "HEALED:"
FAIL   send the exact "FAILED rc=" line to Peach, never loop-retry
READ   /srv/repos/hq/vm-hq-core/tools/bridge-check/runtime/bridge_heal.log   (NEWEST FIRST: newest line = line 1; use bin/logtail <file> [n] for any log)
```

## Layers (all four must connect)
1. **Door** — SSE ingest `https://hq-agentic.duckdns.org/api/events/ingest` (Bearer `SSE_TOKEN`; alias through Cloud Function `proxyToVm`). Canonical name/status list: VM `30-System/ENDPOINTS.md` — never restate doors here.
2. **Tunnel** — `om-ssh` rebuild (`14301 → VM 4301`) so WS real-time resumes.
3. **Guard** — `bin/mesh_guard.sh` keeps `mesh_watch` alive.
4. **Backlog** — `mesh_sweep` moves inbox events into each lane; `moved=N` is the proof.

## Probes (only when something looks wrong; quote real lines)
1. `minis-mcp-cli call vm-hq-gate vm_health` — hq-core / nginx.
2. `curl -s http://127.0.0.1:4300/api/health` — expect `ws:true,firestore:true`.
3. `curl -s http://127.0.0.1:4301/health` — expect `ok`.
4. `sh /srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh` — the wake itself.

## Restore (when the path is down)
1. Retry SSE ingest (main door).
2. Rebuild tunnel: `OM_SSH_NOMUX=1 om-ssh -t auto -L 14301:127.0.0.1:4301 -N &`.
3. Restart `mesh_guard.sh` if `mesh_watch` pid is dead.
4. Run `mesh_sweep.js` — quote `moved=N`.
5. Report before/after flow + moved count. Never claim "bridge ok" without
   the actual lines.

## Apple Shortcuts — who owns what
Peach owns the iOS side; the system never installs, signs or edits a shortcut.
But the wake path **is** part of this skill's contract: ntfy alert -> Peach's
Shortcut -> chat message in the `เวลา` (`scheduled`) channel -> this skill runs
the opener. If that chain breaks, the bridge stays shut even though every layer
on the VM is healthy — check the chain (see "Wake from Shortcut" above) before
blaming the tunnel.

## Canonical layout (device)
- `/srv/repos/hq/vm-hq-core/tools/bridge-check/` — everything lives here:
  `bridge_open_event.sh`, `bin/` (`mesh_guard.sh`, `mesh_watch.py`,
  `mesh_client.py`, `start_mesh.sh`, `device_ping.py`), `runtime/` (pid/hb/log).
- `/srv/repos/skills-shared/skills/bridge-check` is a **symlink** to this directory (one copy, 2026-11-14).
