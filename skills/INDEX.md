# Skills registry — the library, its prefixes and its homes
_Generated 2026-11-21 16:44 +07 by `skills-shared/bin/gen_skills_index.py` (files lane). Do not hand-edit rows: re-run the generator._
## The homes (one copy each, no second source)
| Home | Path | What it is |
|---|---|---|
| authoring | `peachtukta1014/.github` -> `skills/` | the public repo where a skill is written and reviewed (PR) |
| working copy on the VM | `/srv/repos/skills-shared/skills/` | the clone lanes read and edit; this INDEX lives here |
| install target | `/var/minis/skills/` (device) | what the app loads — installed, never hand-edited |
The vault mirror `/srv/repos/hq/vm-hq-core/skills/` was **removed on 2026-11-21** (proven byte-duplicate of the working copy; archive `_archive/skills-mirror-20261121/`). Device home `/var/minis/shared/skills` never existed.
## The prefix rule
**A prefix is a category, not a rename.** No prefix = a **team/system** skill (boot, bridge-check, core-ops, wo-boost, skill-creator, data-context-extractor, system-protocol-design, vector-index-tuning) — it is used by every lane and keeps its bare name. A prefix = a **supplementary** skill in a subject area (`dev-`, `docs-`, `research-`, `ops-`, `hw-`, `ui-`, `ai-`, `cloud-`). Names are stable identifiers (AGENT.md RULE 1): a move between the two groups is decided by Peach, never by the generator.
## Team / system skills (7)
| skill | installed | what it does |
|---|---|---|
| `boot` | yes | lane boot (identity + scope + pad + board) |
| `bridge-check` | yes | open/heal the device-to-VM path (bridge WAKE) |
| `core-ops` | yes | one engineering workflow for the chinchaflow repo (debug/audit/CI/release) |
| `data-context-extractor` | yes | grow a company-specific data-analysis skill from analyst knowledge |
| `system-protocol-design` | yes | design or repair a multi-agent protocol |
| `vector-index-tuning` | yes | tune a vector index (HNSW, quantisation) |
| `wo-boost` | yes | work-order skill: dispatch / ACK / close, locator first |

## Supplementary skills (17)
| category | skill | installed | what it does |
|---|---|---|---|
| AI / prompt | `ai-prompt-engineer` | yes | Writes, refactors, and evaluates prompts for LLMs — generating optimized prompt templates, structured output schemas, evaluation rubrics, and test sui |
| Cloud (GCP) | `cloud-gcp-waf` | yes | Evaluates Google Cloud workloads for cost efficiency and FinOps alignment using the Google Cloud Well-Architected Framework Cost Optimization pillar.  |
| Dev discipline | `dev-agent-md-refactor` | yes | Refactor bloated AGENTS.md, CLAUDE.md, or similar agent instruction files to follow progressive disclosure principles. Splits monolithic files into or |
| Dev discipline | `dev-debugging-recovery` | yes | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't match expectations, |
| Dev discipline | `dev-git-workflow` | yes | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting uncommitted work in |
| Dev discipline | `dev-parallel-agents` | yes | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| Dev discipline | `dev-sql-optimization` | yes | Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use  |
| Dev discipline | `dev-verification-gate` | yes | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming |
| Docs & documents | `docs-diagram` | yes | วาดไดอะแกรม (flowchart, sequence, ER, สถาปัตยกรรม, กราฟ) เป็นไฟล์จริง PDF/SVG/PNG แบบออฟไลน์ ด้วย Typst+CeTZ และฝังลงรายงาน Typst ได้ทันที ใช้คลัง syn |
| Docs & documents | `docs-pdf-converter` | yes | Convert documents to PDF via a typst-based pipeline. Supports Markdown, HTML, plain text, images, and any pandoc-supported format. Use this skill when |
| Docs & documents | `docs-readmes` | yes | Use when writing or improving README files. Not all READMEs are the same — provides templates and guidance matched to your audience and project type. |
| Docs & documents | `docs-typst-report` | yes | "Generate professional, high-quality PDF documents with Typst. Use for reports, academic papers, resumes, structured documents, mathematical typesetti |
| UI & hardware | `hw-todoocard` | yes | TodooCard（土豆片 / NEWSTONE）六色电子纸技能族。用户提到土豆片、TodooCard、电子纸推送， 或要在卡上显示内容时使用。当前子技能 today-eats（今天吃点啥：附近随机外卖并推送）。 后续可扩展天气卡、任意图推送等子技能。 |
| Ops / VM & system | `ops-disk-scan` | yes | Report what is actually taking up space in a directory tree — the biggest subdirectories and the biggest individual files, largest first. Use this ski |
| Research & web | `research-gem-seeker` | yes | Search GitHub for battle-tested solutions instead of reinventing the wheel. Use when the user's problem is universal enough that open source developer |
| Research & web | `research-reader` | yes | Clean and extract the main body content from a webpage URL. Use this skill whenever the user asks to extract, scrape, or read the main article, text,  |
| UI & hardware | `ui-generative-minis` | yes | In the current Minis environment, automatically convert text descriptions into a single-file HTML generator similar to Claude Artifact, with unified s |

## Counts
- library: **24** skills · installed on the device: **24**
- in the library but not installed: none
- installed but missing from the library: `skill-creator`
- archived (pruned 2026-11-21, on the VM): `_archive/skills-pruned-20261121/` — `agentic-eval`, `internet-skill-finder`, `reflex`

## Gates
```
python3 /srv/repos/skills-shared/bin/gen_skills_index.py     # rebuild this file
python3 /srv/repos/skills-shared/bin/doc_id_lint.py         # doc ids: no BROKEN and no MOVED stub
```
