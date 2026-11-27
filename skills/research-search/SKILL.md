---
name: research-search
description: "Search the live web from the VM and get clean LLM-ready results, or fetch known URLs as markdown. Keyless by default."
tags: [4. Research, vm, KEEP, OpenMinis/MinisSkills, exa]
---

# Research Search (Exa MCP, run on the VM)

Web **search** for every lane, executed on the VM itself — no phone, no browser,
no Minis app in the middle (RULE 16). Ported from the device-side skill
`exa-search` (OpenMinis/MinisSkills, upstream `exa-search`); the device skill
needs the Minis browser/MCP, this one is a plain HTTPS call so the VM can run it.

## When to use
- You need current information and do not have the URL yet (news, releases, docs, people, companies)
- You have URLs and want clean markdown (use `fetch`; `research-reader` does this too)
- Pair with `research-gem-seeker` (find code) and `research-reader` (read one page)

## Run it (on the VM)
```bash
bin/skill-run research-search scripts/search.py search "self-hosted team memory with an API" --num 5
bin/skill-run research-search scripts/search.py fetch https://example.com/article
bin/skill-run research-search scripts/search.py tools      # what the endpoint exposes
```

## How it works
`POST https://mcp.exa.ai/mcp` — MCP streamable HTTP, JSON-RPC
(`initialize` -> `notifications/initialized` -> `tools/call`). The endpoint
exposes `web_search_exa` and `web_fetch_exa`. A `User-Agent` header is required
(the endpoint answers **403** to bare `Python-urllib/...`).

Query style: describe the ideal page, not keywords — "blog post comparing X and Y
performance", not "X vs Y".

## Key
Keyless works (Exa MCP basic tier). For higher limits set `EXA_API_KEY` in the lane
environment (the VM keeps the value in its vault — `system/SECRETS.md`, never published);
the script sends it and never prints it.
Check without printing: `[ -n "$EXA_API_KEY" ] && echo set || echo unset`.

## Requirements
`python3` (stdlib only) + outbound HTTPS. Runs in `vm` scope only.
