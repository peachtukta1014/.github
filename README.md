# .github — shared CI assets

-  — composite action: POST one wo/1 EVENT to the HQ ingest door.
  Used by the standard  workflow in all 8 repos.

Usage:
```yaml
- uses: peachtukta1014/.github/notify-ingest@v1
  with:
    endpoint: ${{ vars.EVENT_URL }}
    token: ${{ secrets.VM_SSE_TOKEN }}
    lane: code
    repo: ${{ github.repository }}
```
