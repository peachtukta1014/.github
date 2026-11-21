# device-vs-vm — which machine holds what

**The device (iSH + Minis on the phone) is the key and the door only.** Code, vault, identity,
secrets, logs and services live on the VM. If device and VM disagree, **the VM wins**.

## One trunk spelling
| | Path |
|---|---|
| **canonical (print this)** | `/srv/repos/hq/vm-hq-core` |
| compatibility symlink (works, never print) | `/opt/vault/vm-hq-core` -> the above |

Both resolve, so nothing breaks — but a doc that prints the symlink form makes a reader believe
there are two trees. Verified 2026-11-21: the `boot` skill printed one form, the `wo-boost`
locator printed the other.

## What lives where
| Thing | Device | VM |
|---|---|---|
| skills | `/var/minis/skills/` | — |
| device tool scripts | `/var/minis/shared/tools/bin/` | — |
| rules, identity, pads, board, room, ledger | — | `/srv/repos/hq/vm-hq-core/` |
| secrets | never | `/etc/chincha/env/*` (root 0600 / root:ubuntu 0640) |
| offline lane cards | `/var/minis/shared/lanes/<lane>.md` | — |

## Reaching the VM
```
ws_exec  (tunnel 14301->4301)   PRIMARY - all shell work
om-ssh   (auto-probe route)     DIRECT - large writes, long runs, tunnel dead
```
`om-ssh` auto-probes and picks `ssh-hq-tailscale` (tailnet `100.126.23.56`) first, IAP as fallback.

**A device script must never `cd` into a VM path** — it does not exist here. Route the command
through `ws_exec`. (This skill's first draft made exactly that mistake; `scripts/where` fixed it.)
