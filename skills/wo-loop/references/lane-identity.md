---
name: lane-identity
description: Load who this chat session is — which lane (channel) it belongs to, that lane's role, VM identity paths and pad. Use at the start of any session, whenever the user asks "who are you / which lane", or when a message arrives from another lane and you must reply as the right owner.
---

# lane-identity — remember the role, read the truth from the VM

The device holds no identity of its own. Each chat session is bound to one lane in
`$HQ_ROOT/lanes/<lane>/identity/config/session_bind.json`; the real identity lives on the VM.

## Steps (in order)

1. Detect the lane:
   ```
   lane-id
   ```
   → prints `LANE = <scope> (<ไทย>)`, the offline card, and the VM paths.
2. Load the live identity (always prefer VM over the card):
   ```
   lane-id --fetch
   ```
   This prints `lanes/<lane>/identity/GLOBAL.md` from the VM.
3. If VM/tunnel is down, fall back to the offline card `$HQ_ROOT/lanes/<lane>.md`
   and say so. Do not invent tasks, paths or a new role.
4. Start work only after the lane's board/pad is read:
   ```
   ws_exec --command "bash $HQ_ROOT/bin/om-boot <lane>"
   ```

## Rules

- Answer as **that lane only**. Work ordered by another lane is accepted and closed
  by the owning lane, with `wo-loop complete` → HTTP 201 + inbox_id.
- Never restate protocol rules; point at the VM file (`system/…`).
- Unknown/ambiguous lane → ask which channel this is; never guess between lanes.
- The device is an entry gate: no canonical copy, no second diary, keep storage near-empty.
