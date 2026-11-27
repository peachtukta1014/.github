---
name: firecrawl-research
version: 1.0.0
description: "Research the live web through the Firecrawl MCP that is already connected: search, scrape a page to markdown, map or crawl a site, or run a multi-step research agent. Use when a research task needs real pages (prices, specs, docs, tables, PDFs) and the free path is not enough."
tags: [4. Research, both, ours, mcp]
---

# firecrawl-research — the second research door (MCP, metered)

**Why this skill exists (Peach 2026-11-27).** The team already has a Firecrawl MCP
connected, and it is *metered* — so it must be the deliberate second choice, not the
default. The free/general path is `research-search`; this skill documents exactly what the
MCP exposes and when spending a credit is the right call.

## When to use it

| situation | use |
|---|---|
| quick fact check, read one page as text | `research-search` (free) |
| page is JS-heavy, paywalled-ish, or Firecrawl already has it indexed | **this skill** |
| need a **structured** result (fields, table, JSON) from a page or PDF | **this skill** — `firecrawl_scrape` with a schema/prompt |
| need a section of a site (many pages, same shape) | **this skill** — `firecrawl_map` then `firecrawl_crawl` |
| need an open-ended multi-page answer with sources | **this skill** — `firecrawl_agent` (most expensive: watch credits) |
| just browsing a site interactively | the built-in browser, not this |

## The tools (as the connected MCP exposes them)

Discover the live list before relying on it: `minis-mcp-cli tools firecrawl`.

| tool | what it does | cost |
|---|---|---|
| `firecrawl_scrape` | one URL -> markdown / html / links / screenshot / summary / **structured `json` via `queryOptions`** / PDF pages. `url` may omit the scheme; `objective` (one sentence) is required | 1 page credit |
| `firecrawl_search` | web search, returns sources to scrape next | search credit |
| `firecrawl_map` | list a site's URLs (find the right page before crawling) | cheap |
| `firecrawl_crawl` | collect a set of pages under a site/path | per page |
| `firecrawl_agent` + `firecrawl_agent_status` | multi-step research job with sources; poll its status | most expensive |
| `firecrawl_extract` | structured extraction across known pages | per page |
| `firecrawl_usage` | read the team's credit usage — **check this before a big run** | free |
| `alexandria_library_search` / `_read` | typed data providers (same fields across many pages) | per call |

Notes that change results:
- `maxAge: 0` forces a live fetch; a larger value accepts a cached copy (cheaper, may be stale).
- `onlyMainContent: true` strips navigation — use it when you want clean text.
- `parsers: ["pdf"]` (+ `pdfOptions.maxPages`) handles PDFs.
- `storeInCache` / `zeroDataRetention` decide whether the result is kept.

## How to call it

- From an agent session: `minis-mcp-cli call firecrawl firecrawl_scrape '{"url":"…","objective":"…"}'`.
- From the VM: the MCP lives on the device side, so a VM-side need goes through the
  **device-queue** (`bin/device_queue.py` on the VM) or is handed to a device session —
  do not invent a VM-only path.
- Big jobs: `firecrawl_usage` first, then the smallest tool that answers the question.

## Iron rules

1. **Free first.** If `research-search` can answer it, do not spend a credit.
2. **Name the objective.** `firecrawl_scrape` needs a one-sentence `objective`; keep it about the goal, never secrets or the owner's exact words.
3. **One page, one call.** Prefer several small scrapes over one crawl unless the task really spans a site.
4. **Record what it cost.** When a run is heavy, note the credits (`firecrawl_usage`) in the work order evidence.
5. **Cite the source URL** in the answer; a scraped page is a source, not the truth.

## Related skills

`research-search` (general, free) · `research-reader` (URL -> markdown, free) ·
the folded web-research family (web-search / exa-search / tavily-search / web-content-extractor)
