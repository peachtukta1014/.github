# .github — shared assets (CI is OFF)

**Status: GitHub Actions is turned off for this account (Peach 2026-11). Nothing here runs.**

The public content of this repo is the **skills** folder, published from the HQ VM trunk
(`bin/publish_public.sh` → `skills/`). That is the only part that is live and it is what the
phone imports.

## Archived (kept for reference, not active)

`archive/ci/` holds what used to be shared CI:

- `templates/sync-project-tree.yml`, `templates/pr-status.yml`, `templates/deploy-status-job.yml`
- `notify-ingest/action.yml` — the composite action that POSTed one wo/1 EVENT to the HQ ingest door
- `install-ci-workflows` — the installer that dropped those workflows into each repo
- `gen_skills_index.py`, `doc_id_lint.py` — stale copies; the live versions live in the VM trunk

To revive any of it: copy the file back out of `archive/ci/`, and re-check the paths against the
VM trunk first (`system/AGENT.md`, `bin/publish_public.sh`) — the old `notify-ingest@v2` path in
the snippets below no longer resolves.

## Old usage (archived, for reference)

```yaml
- uses: peachtukta1014/.github/archive/ci/notify-ingest@main
  with:
    endpoint: ${{ vars.EVENT_URL }}
    token: ${{ secrets.VM_SSE_TOKEN }}
    lane: code
    repo: ${{ github.repository }}
```
