# Skills registry — provenance, homes and tags
_Generated 2026-11-27 18:02 +07 by `bin/gen_skills_index.py` from `skills/SOURCES.json`. Do not hand-edit rows: edit SOURCES.json and re-run._
## The homes (one copy each)
| Home | Path | What it is |
|---|---|---|
| canonical source | `hq-infra/skills/` | trunk skills edited and reviewed here |
| install target | `/var/minis/skills/` (device) | what the app loads — imported, never authoritative |
## Publishing
`hq-infra/.github/workflows/publish-skills.yml` is the sole publisher. It publishes the canonical workflow dispatch). Open Minis imports skills from the public URL.
## Tag legend
`source` = where it came from (**team** ours · **minis** built-in · **OpenMinis** official · a hub name) · `readiness` = **ready** (works as-is) or **adapt** (edit before use) · `where` = **device** (iSH on the phone) / **vm** / **both** / **prompt-only** · `runtime` = what it needs.
**Provenance rule:** a row is exact only when SOURCES.json says `verified: true`. Rows marked *(unverified)* came from a shared hub / the internet and their repo is not pinned yet — adapt the body and scripts for us before relying on them (Peach 2026-11-21).

## Categories (from SOURCES.json)
| # | Category | Skills |
|---|---|---|
| 1 | Team + system | `bridge-check`, `lane-boot`, `mcp-cli`, `skill-registry-maintenance`, `system-protocol-design`, `team-composition-analysis`, `wo-loop` |
| 2 | Dev discipline | `dev-agent-md-refactor`, `dev-debugging-recovery`, `dev-git-workflow`, `dev-parallel-agents`, `dev-verification-gate`, `final-release-review`, `git-commit`, `jest-skill`, `lesson-learned`, `pnpm-upgrade`, `refactor`, `tdd`, `writing-plans` |
| 3 | Documents | `code-documenter`, `docs-diagram`, `docs-pdf-converter`, `docs-readmes`, `docs-typst-report`, `excalidraw-diagram`, `plantuml-ascii` |
| 4 | Research | `internet-skill-finder`, `research-gem-seeker`, `research-reader`, `research-search` |
| 5 | Ops + infra | `cloud-gcp-waf`, `ops-disk-scan`, `sentry-sdk-setup` |
| 6 | Data | `data-context-extractor`, `dbt-transformation-patterns`, `dev-sql-optimization`, `huggingface-datasets`, `ml-pipeline`, `shap`, `similarity-search-patterns`, `spark-optimization`, `stable-baselines3`, `vector-index-tuning` |
| 7 | Devices + UI | `hw-todoocard`, `ui-generative-minis`, `webapp-template` |
| 8 | Prompt + AI | `agentic-eval`, `ai-prompt-engineer`, `langchain-architecture` |
| 9 | Authoring | `skill-creator`, `writing-skills` |
| 99 | Uncategorised | `evidence-chain-builder`, `firecrawl-research`, `production-agent-public`, `webapp-testing` |


## Our team skills (6)
| skill | ไทย | tags | installed | what it does |
|---|---|---|---|---|
| `bridge-check` | เปิดสะพานถึง VM | team · ready · vm · prompt-only | yes | Our own. Bridge WAKE — open/heal the device-to-VM path. |
| `docs-diagram` | วาดไดอะแกรมเป็นไฟล์จริง | team · ready · vm · python typst | yes | Composed here from hub reference material (see shared/skills-hub-sources/INDEX_TH.md). Renders offline with Ty |
| `lane-boot` | บูสต์เลนผ่าน VM | team · ready · vm · prompt-only | yes | Lean English lane boost entry for Open Minis and the HQ VM; covers all eight lanes. |
| `skill-registry-maintenance` | ทะเบียนสกิล | team · ready · vm · python git | yes | Reusable workflow for stable-ID skill registry maintenance, resolver changes, and evidence-led validation. |
| `system-protocol-design` | ออกแบบโปรโตคอลเอเจนต์ | team · ready · vm · prompt-only | yes | Our own. Design or repair a multi-agent protocol. Peach 2026-11-21: keep, do not delete. |
| `wo-loop` | บูทเลน + ใบงาน | team · ready · vm · prompt-only | yes | Our own. Boot a lane then run the work loop; absorbed the two former team skills. |

## Minis built-in (0)
| skill | ไทย | tags | installed | what it does |
|---|---|---|---|---|

## Imported — by source (49)
| skill | upstream | source repo | ไทย | tags | installed | verdict |
|---|---|---|---|---|---|---|
| `ai-prompt-engineer` | prompt-engineer | Jeffallan/claude-skills | ออกแบบพรอมต์ LLM | claude-skills · adapt · vm · net | yes | KEEP+PATCH |
| `code-documenter` | code-documenter | Jeffallan/claude-skills **(unverified)** |  | claude-skills · adapt · vm · python node net | no | KEEP+PATCH |
| `ml-pipeline` | ml-pipeline | Jeffallan/claude-skills **(unverified)** |  | claude-skills · adapt · vm · net git | no | KEEP+PATCH |
| `refactor` | refactor | Jeffallan/claude-skills **(unverified)** |  | claude-skills · adapt · vm · prompt-only | no | KEEP+PATCH |
| `docs-pdf-converter` | pdf-converter | OpenMinis/MinisSkills | เอกสาร → PDF | MinisSkills · ready · vm · python typst | yes | KEEP |
| `evidence-chain-builder` | evidence-chain-builder | OpenMinis/MinisSkills |  | MinisSkills · ready · vm · python | no | KEEP |
| `hw-todoocard` | todoocard | OpenMinis/MinisSkills | จอ e-paper TodooCard | MinisSkills · ready · vm · python | yes | KEEP |
| `ops-disk-scan` | disk-scan | OpenMinis/MinisSkills | ดิสก์กินที่ไหน | MinisSkills · ready · vm · python zip git | yes | KEEP |
| `production-agent-public` | production-agent-public | OpenMinis/MinisSkills |  | MinisSkills · ready · vm · python net | no | KEEP |
| `research-reader` | web-content-extractor | OpenMinis/MinisSkills | อ่านเนื้อหาเว็บ | MinisSkills · ready · vm · net | yes | KEEP |
| `research-search` | exa-search | OpenMinis/MinisSkills | ค้นเว็บจาก VM | MinisSkills · adapt · vm · python net | no | KEEP |
| `ui-generative-minis` | generative-ui-minis | OpenMinis/MinisSkills | ข้อความ → HTML | MinisSkills · ready · vm · python | yes | KEEP |
| `webapp-testing` | webapp-testing | anthropics/skills |  | skills · adapt · vm · python node net | no | KEEP+PATCH |
| `agentic-eval` | agentic-eval | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `cloud-gcp-waf` | google-cloud-waf-cost-optimization | hub (unverified) **(unverified)** | ค่าใช้จ่าย GCP | hub · adapt · vm · net | yes | KEEP+PATCH |
| `data-context-extractor` | data-context-extractor | hub (unverified) **(unverified)** | สร้างสกิลข้อมูล | hub · ready · vm · zip | yes | KEEP |
| `dbt-transformation-patterns` | dbt-transformation-patterns | hub (unverified) **(unverified)** |  | hub · adapt · vm · git | no | KEEP+PATCH |
| `dev-agent-md-refactor` | agent-md-refactor | hub (unverified) **(unverified)** | จัด AGENTS.md | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-debugging-recovery` | debugging-and-error-recovery | hub (unverified) **(unverified)** | หาสาเหตุบั๊ก | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-git-workflow` | git-workflow-and-versioning | hub (unverified) **(unverified)** | วินัย git / PR | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-sql-optimization` | sql-optimization-patterns | hub (unverified) **(unverified)** | จูน SQL | hub · ready · vm · prompt-only | yes | KEEP |
| `docs-readmes` | crafting-effective-readmes | hub (unverified) **(unverified)** | เขียน README | hub · ready · vm · prompt-only | yes | KEEP |
| `docs-typst-report` | typst-pdf-maker | hub (unverified) **(unverified)** | รายงาน PDF (Typst) | hub · adapt · vm · python typst | yes | KEEP+PATCH |
| `excalidraw-diagram` | excalidraw-diagram | hub (unverified) **(unverified)** |  | hub · adapt · vm · net | no | KEEP+PATCH |
| `final-release-review` | final-release-review | hub (unverified) **(unverified)** |  | hub · adapt · vm · net git gh-cli | no | KEEP+PATCH |
| `git-commit` | git-commit | hub (unverified) **(unverified)** |  | hub · adapt · vm · net git | no | KEEP+PATCH |
| `huggingface-datasets` | huggingface-datasets | hub (unverified) **(unverified)** |  | hub · adapt · vm · node net | no | KEEP+PATCH |
| `internet-skill-finder` | internet-skill-finder | hub (unverified) **(unverified)** |  | hub · adapt · vm · python gh-cli | no | KEEP+PATCH |
| `jest-skill` | jest-skill | hub (unverified) **(unverified)** |  | hub · adapt · vm · node | no | KEEP+PATCH |
| `langchain-architecture` | langchain-architecture | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `lesson-learned` | lesson-learned | hub (unverified) **(unverified)** |  | hub · adapt · vm · git | no | KEEP+PATCH |
| `mcp-cli` | mcp-cli | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `plantuml-ascii` | plantuml-ascii | hub (unverified) **(unverified)** |  | hub · adapt · vm · java net git | no | KEEP+PATCH |
| `pnpm-upgrade` | pnpm-upgrade | hub (unverified) **(unverified)** |  | hub · adapt · vm · node net git | no | KEEP+PATCH |
| `research-gem-seeker` | github-gem-seeker | hub (unverified) **(unverified)** | หา OSS จาก GitHub | hub · adapt · vm · python node net | yes | KEEP+PATCH |
| `sentry-sdk-setup` | sentry-sdk-setup | hub (unverified) **(unverified)** |  | hub · adapt · vm · java net | no | KEEP+PATCH |
| `shap` | shap | hub (unverified) **(unverified)** |  | hub · adapt · vm · python net | no | KEEP+PATCH |
| `similarity-search-patterns` | similarity-search-patterns | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `spark-optimization` | spark-optimization | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `stable-baselines3` | stable-baselines3 | hub (unverified) **(unverified)** |  | hub · adapt · vm · python net | no | KEEP+PATCH |
| `team-composition-analysis` | team-composition-analysis | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `vector-index-tuning` | vector-index-tuning | hub (unverified) **(unverified)** | จูน vector index | hub · ready · vm · prompt-only | yes | KEEP |
| `webapp-template` | spark-app-template | hub (unverified) **(unverified)** |  | hub · adapt · vm · prompt-only | no | KEEP+PATCH |
| `dev-parallel-agents` | dispatching-parallel-agents | obra/superpowers | แบ่งงานขนาน | superpowers · adapt · vm · prompt-only | yes | KEEP+PATCH |
| `dev-verification-gate` | verification-before-completion | obra/superpowers | ยืนยันก่อนปิดงาน | superpowers · ready · vm · prompt-only | yes | KEEP |
| `tdd` | tdd | obra/superpowers **(unverified)** |  | superpowers · adapt · vm · prompt-only | no | KEEP+PATCH |
| `writing-plans` | writing-plans | obra/superpowers **(unverified)** |  | superpowers · adapt · vm · git | no | KEEP+PATCH |
| `writing-skills` | writing-skills | obra/superpowers **(unverified)** |  | superpowers · adapt · vm · net git | no | KEEP+PATCH |
| `firecrawl-research` | — | ours (written on the VM, Peach 2026-11-27) |  | ours (written on the VM, Peach 2026-11-27) · ready · both · prompt-only | no | KEEP |

## Counts
- library **55** · ours **6** · built-in **0** · imported **49** · installed on device **24**
- provenance verified: **19** / 55 — the rest are hub/internet imports whose repo is not pinned yet
- 2026-11-18 audit (code lane): KEEP 6 · KEEP+PATCH 11 · ARCHIVE 9 · DELETE 18 (`docs/reports/skills-audit-20261118.md`)

## Gates
```
python3 $HQ_ROOT/bin/gen_skills_index.py
```
