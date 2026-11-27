---
name: wo-loop
description: "Run the work-order loop across HQ VM lanes: boot, dispatch, board, pad, close, report, and PR."
---

# wo-loop

Use one logical work-order entry for lane boot, dispatch, pad, board, report, closeout, and PR preparation. The VM owns execution, pads, boards, repositories, services, and durable work-order state. Open Minis is only the conversational UI/MCP client.

## 1. Boot — start here

```text
Resolve: lane-id -> ASCII lane ID
Run:    lane-boot <scope>
Read:   only the paths reported by boot
Do not: inspect broad paths or read pad/identity files before boot
```

Lane names: ปั้นแป้ง=code · ข้าวของ=files · จี้=jii · ข้าวเรียม=research · เวลา=scheduled · กุ้งทอง=seafood · ชาเย็น=tea · หมึกสาย=webhook

Unknown scope: use `lane-id`; never infer from a misspelled voice command.

After boot, report identity loaded, pad tasks, board rows, and what must be done now. Scripts have one canonical home; adapters and public copies are projections.

## 2. Capability routing

Resolve the operation through `registry/transports.json` and the registered MCP surface. Do not name a device implementation path as if it were the VM authority.

- `wo.lifecycle`, `vm.command.small`, and `vm.command.structured`: WS primary.
- `vm.command.large`, `vm.file.bulk`, `vm.command.raw`, and `vm.interactive`: Tailscale direct SSH primary.
- IAP: compatibility-only; never present it as the current primary route.
- `vm-hq-gate`: primary typed VM gateway.
- `minis-tools`: device/WS adapter and transitional entrypoint; not durable-state owner.

If registration, path, or SHA is not live-verified, label it `runtime verification pending` and keep the command logical.

## 3. VM-side logical commands

```text
lane-boot <scope>
wo-loop dispatch --to <lane> --from <me> --job WO-... --title "..." [--checklist "a|b"]
wo-loop sp status --scope <lane>
wo-loop pad --lane <lane> --log "..." [--status "..."] [--next-action "..."]
wo-loop item --lane <lane> --n <N> --status done --evidence "..."
wo-loop complete --to <orderer> --from <lane> --job <JOB> --summary "..." [--evidence "..."]
wo-loop board [--scope <lane>]
wo-loop report --lane <lane> --title "..."
wo-loop pr <branch> <title> [body-file]
```

`exec` is only for a bounded VM command selected by the capability resolver. `wo-loop` is not a generic shell catalogue.

## 4. Bridge boundary

Run `bridge-check` only for connection health, recovery, or push-wake. It must never create, own, or close work-order state. A failed bridge opener is reported exactly once; do not loop-retry.

## 5. Rules

- Ask before assuming: voice input may be misspelled.
- Job IDs use `WO-<lane>-<slug>-<YYYYMMDD>-NN`.
- One asset = one owner; shared skills have no lane owner.
- Read `specs/00_INDEX.md` and callers before touching shared scripts.
- No ACK/RESULT means the job is not done.
- Update the VM-owned pad before ending any turn that changed work.
- Report to Peach in Thai: what, measurable result, risk, and what she must decide.
- Never hand-edit pad JSON.

## 6. CI

Open the PR and stop. Do not poll CI from this skill. The CI/event workflow reports success or failure.

## Locator

```json
{
  "skill_file": "registry/skills.json -> skills/wo-loop/SKILL.md",
  "per_scope_detail": "skills/wo-loop/<scope>/SKILL.md",
  "vm_wo_loop": "runtime-verified VM entry; currently declared by the VM authority model",
  "vm_pad": "boot-reported VM path",
  "vm_board": "boot-reported VM path",
  "protocol_map": "specs/00_INDEX.md",
  "dispatch": "logical wo-loop dispatch",
  "complete": "logical wo-loop complete",
  "message": "logical wo-loop report",
  "ws_exec": "resolved WS capability, when selected by registry"
}
```
