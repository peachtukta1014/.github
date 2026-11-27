# .github — shared assets

**CI is OFF for this account (Peach 2026-11). Nothing here runs.**

The only live content is **`skills/`**, published from the HQ VM trunk by
`bin/publish_public.sh`. That folder is what the phone imports when Peach presses
"update skills from URL".

Everything that used to be shared CI (workflow templates, the `notify-ingest` composite action,
the installer and the stale generator copies) has been deleted, not archived — the VM trunk holds
the live versions, and GitHub history keeps the rest if it is ever needed.

The phone reaches the VM directly over Tailscale; there is no Cloud Function bridge any more
(`proxyToVm` was deleted 2026-11-24).
