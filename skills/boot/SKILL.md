---
name: boot
description: Boot one lane (identity + SCOPE + pad + board). Use when Peach says "/boot <lane>" or a lane needs to start work. Runs one VM command; do not search the filesystem.
---

# boot

```
WHERE  VM /opt/vault/vm-hq-core/bin/om-boot
RUN    /var/minis/shared/tools/bin/ws_exec.py --command "bash /opt/vault/vm-hq-core/bin/om-boot <scope>"
       (ws_exec opens the tunnel itself; if ssh fails it calls ws_tunnel_guard, then om-ssh — no manual step)
READ   /opt/vault/vm-hq-core/70-Lanes/<scope>/SCOPE.md · PROTOCOL/00_INDEX.md
DON'T  no ls/find/md5 before boot · no om-sync during boot
```

Lane names: ปั้นแป้ง=code · ข้าวของ=files · เกมมิ่ง=gaming · เกี๊ยว=hokkien · จี้=jii · ข้าวเรียม=research · เวลา=scheduled · กุ้งทอง=seafood · ชาเย็น=tea · หมึกสาย=webhook

Unknown scope? `/var/minis/shared/tools/bin/lane-id` resolves this chat session → lane
(bindings: `memory/config/session_bind.json`; offline card: `shared/lanes/<lane>.md`).

After boot report: identity loaded · pad tasks · board rows · what must be done now.
Scripts are symlinks to the single real copy — never duplicate them (RULE 11).

## Which lane am I (lane-id)
Full steps live in `references/lane-identity.md` (same folder). Short form: read `/var/minis/memory/config/session_bind.json` -> `lane-id --fetch` -> live identity from `70-Lanes/<lane>/identity/` -> offline card `/var/minis/shared/lanes/<lane>.md` when the tunnel is down.

## The key to the VM (device-side script map)
Full map in `references/vm-key.md` (same folder): which local script lives where, which door to use (ws_exec / ws_dispatch / ws_complete / gate_call), and what never lives on the device. The VM stays canonical.
