# Transport boundaries

Resolve transport by capability from `registry/transports.json` and the registered MCP surface:

- `wo.lifecycle`, `vm.command.small`, and `vm.command.structured`: WS primary.
- `vm.command.large`, `vm.file.bulk`, `vm.command.raw`, and `vm.interactive`: Tailscale direct SSH primary.
- `vm-hq-gate`: primary typed VM gateway.
- `minis-tools`: device/WS adapter and transitional entrypoint.
- IAP: compatibility-only; never present it as the current primary route.

`wo-loop` owns lifecycle/bookkeeping semantics. `bridge-check` owns health, recovery, and push-wake only. The VM owns durable execution and state; device files are adapters/projections.

Never invent endpoints, hostnames, tokens, SSH targets, or implementation paths. If live registration or deployment paths are not verified, keep the command logical and report `runtime verification pending`.
