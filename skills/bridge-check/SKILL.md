---
name: bridge-check
description: "Bridge WAKE — reopen the app-to-VM connection so queued events flow again. Use when iOS suspends the app, a tunnel dies, or a wake alert arrives."
---

# bridge-check — health, recovery, and push-wake

`bridge-check` opens or heals the app-to-VM path so already queued events can flow into the correct lane. It is a connectivity mechanism, not a pending-count query and not a work-order state store.

## Scope

It may:

- check or reopen the configured app-to-VM door;
- restore the configured WS/tunnel guard;
- restart or heal the mesh watcher when the authorized runtime says it is stale;
- sweep already queued events into lanes;
- report a fresh `healthy`, `HEALED`, or exact `FAILED rc=` verdict.

It must not:

- create, dispatch, complete, or own a work order;
- write a lane pad or board row as its own state machine;
- invent a host, URL, token, SSH target, or implementation path;
- be used as a generic shell or MCP tool catalogue.

## When to run

Run once when:

- iOS killed or backgrounded the app and the session went quiet;
- a configured wake alert arrives;
- the configured WS/tunnel heartbeat is stale or unavailable;
- Peach says `เช็คสะพาน`, `ต่อสะพาน`, or `เชื่อมสะพาน`.

A wake message is a trigger to call this skill, not a file to read. The scheduled lane owns the wake conversation when the configured Shortcut routes it there.

## Wake discipline

1. Resolve the registered bridge-health/recovery capability before invoking anything.
2. Run the authorized bridge opener once. Do not hard-code a device or VM path from this document while runtime verification is pending.
3. Reply with the opener's own verdict: `bridge healthy; no action`, `HEALED: ...`, or the exact `FAILED rc=...` line.
4. If the result says `heal already running; skipped`, inspect only the authorized process/lock evidence defined by the runtime deployment.
5. Never loop-retry. A failed wake is reported, not hidden.
6. Do not claim the bridge is healthy without fresh output from the opener or registered health capability.

## Transport boundary

The route is capability-selected, not a fixed primary/fallback pair:

- WS is primary for lifecycle and small/structured bridge coordination.
- Tailscale direct SSH is primary for large/raw/interactive recovery operations when selected by the registry.
- IAP is compatibility-only.
- `vm-hq-gate` is the typed VM gateway; `minis-tools` may expose a device/WS adapter.
- The VM owns durable event, lane, board, and work-order state. The device exposes transport/UI adapters only.

The machine-readable route policy is `registry/transports.json`. Live registration and implementation paths remain runtime facts; if they are not verified, say so.

## Evidence contract

A successful run reports one of:

```text
bridge healthy; no action
HEALED: <opener-provided detail>
FAILED rc=<n>: <opener-provided detail>
```

When healing drains queued events, include the opener-provided `moved=N` evidence. Do not manufacture health tables or counts.

## Shortcut boundary

Peach owns the iOS Shortcut. This skill does not install, sign, edit, or mutate it. A configured notification-to-chat wake message should invoke this skill in the configured lane; the path text in that message is not executed by the Shortcut itself.

## References

Load only when needed:

- `references/README_TH.md` — user-facing bridge explanation and current deployment notes.
- `registry/transports.json` — capability-to-route policy.
- `system/CONNECTION_POINTS.md` — endpoint facts and authority boundary.
