---
name: reflex
description: >-
  The ONE entry for locating things: where a document lives, which machine holds it
  (Minis device vs VM), which tool leads where, and whether an address is still valid.
  Use at boot, before searching for a file, before choosing a tool, or when a pointer
  might have gone stale. Do NOT grep the tree to find something - ask reflex first.
  Trigger: "where is X", "which tool for Y", "หาไฟล์", "reflex", a stale/broken pointer,
  or any moment a lane is about to search the filesystem.
---

# reflex — where things live, and whether that is still true

**ใช้ทำอะไร:** ที่เดียวสำหรับหาว่าอะไรอยู่ที่ไหน — เอกสารอยู่ไฟล์ไหน เครื่องไหนถือครอง (มือถือ Minis หรือ VM) เครื่องมือตัวไหนพาไปไหน และที่อยู่(pointer)นั้นยังใช้ได้อยู่ไหม เรียกก่อนบูท ก่อนหาไฟล์ ก่อนเลือกเครื่องมือ หรือเมื่อสงสัยว่า pointer ตายแล้ว

**Index only.** Detail lives in `references/`; load ONE file, not all of them.

## The one trunk
All VM paths: **`/srv/repos/hq/vm-hq-core`** (the real tree).
`/opt/vault/vm-hq-core` is a compatibility symlink — it works, but never print it.

## Four questions every entry answers
`leads where` · `what for` · `destination` · `how to call` — one line each, no prose.

## Categories (pick by intent, then open the one reference)

| # | Intent | Open | Canonical home |
|---|---|---|---|
| 1 | find a document / resolve a doc id | `references/addresses.md` | `registry/docids.json` -> `docmap.json` |
| 2 | which machine holds what | `references/device-vs-vm.md` | `30-System/DEVICE_POINTER.md` |
| 3 | which tool leads where | `references/tools.md` | `30-System/TOOL_CATALOGUE.md` (12 categories) |
| 4 | is this pointer still true | `references/known-drift.md` | this skill, + `bin/doc_drift.py` |

## Scripts (thin — they call the canonical tools, they do not reimplement them)

```
sh scripts/where <topic-or-id>     # where does X live -> one path + its owner
sh scripts/tool <intent>           # which tool for Y -> category + how to call
sh scripts/check [id ...]          # is this address still valid -> ok | MOVED | BROKEN
```

## Rules
- **Ask reflex before searching.** If reflex answers, no `rg`/`find` is needed.
- **Never copy** a script or a table into this skill; point at the canonical file (RULE 11).
- A stale pointer is a **defect to fix**, not a reason to create a second copy of the target.
- `find` is broken on this VM - use `rg --files`.
