---
name: vm-key
description: >-
  Device-side entry skill (the key). Use whenever a channel needs to reach the
  VM: run shell commands, open the WS tunnel, choose privilege level, or load
  the canonical TOOLS. This skill is the on-device map of which local script
  lives where; the VM stays the source of truth.
path: /srv/repos/hq/vm-hq-core/skills/vm-key/SKILL.md
---

# vm-key — the key to the VM (device side only)

**Rule:** the VM is the home. This device holds only the key: transport scripts,
protocol clients, and skills. No identity, no code, no secrets live here.
Canonical tool map: `/srv/repos/hq/vm-hq-core/30-System/TOOLS.md` (read it at boot).

## 1. One command to work on the VM

```
minis-tools ▶ ws_exec {"command": "<shell command>"}
```
- Runs as `ubuntu` on the VM, speed ~1.3 s (one ssh tunnel 14301->4301, then ws-bridge `/exec`).
- **Full privilege** (apt, systemctl, package installs, root-owned files):
  `ws_exec {"command": "...", "root": true}` — audited to `/var/log/ws-exec.log` with `user=root`.
- Fallback if the tunnel will not open: `minis-tools ▶ vm_exec` (om-ssh, ~10 s).

## 2. Where the device pieces live

| Purpose | Path (on this device) |
|---|---|
| Fast shell client | `ws_exec.py` |
| SSH / IAP transport | `om-ssh`, `om_iap.py` |
| Order work | `ws_dispatch.py` |
| Close work | `ws_complete.py` |
| Message only | `sse_dispatch.py` |
| Chat ping | `sse_ping.py` |
| Board | `board_check.py` |
| One-entry CLI | `wo-loop` |
| Bridge heal | `/srv/repos/hq/vm-hq-core/tools/bridge-check/bridge_open_event.sh` |
| MCP server (device) | `/srv/repos/hq/vm-hq-core/tools/mcp/minis_tools_mcp.py` |
| MCP server (VM) | `vm-hq-gate` -> `/srv/repos/hq/vm-hq-core/mcp/gate/mcp_gate.py` |
| Chapter skills | `/srv/repos/hq/vm-hq-core/skills/wo-loop/<scope>/SKILL.md` |
| Device inventory | `30-System/CONNECTION_POINTS.md` on the VM (device keymap was retired 2026-11-15) |

**Skill rule:** every skill has exactly ONE real copy at
`/srv/repos/hq/vm-hq-core/skills/<name>/` and `/srv/repos/hq/vm-hq-core/skills/<name>` is a symlink to it.
Two diverging copies = a bug.

## 3. Choose the door

| Job | Door |
|---|---|
| run anything on the VM | `ws_exec` |
| order another channel | `ws_dispatch` |
| close a job | `ws_complete` |
| read the board | `board_check` |
| shop / Firestore / mesh | `vm-hq-gate ▶ gate_directory` -> `gate_call(category='chincha')` |
| repo / PR | `gate_call(category='github')` |
| VM status / logs / service | `gate_call(category='vm-operations')` |

## 4. Never on the device

`70-Lanes/<scope>/identity/*`, `/home/ubuntu/chinchaflow`, secrets, reports, logs,
Firestore data, service state. Load identity from the VM, never from the phone.
