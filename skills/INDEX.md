# Skills registry — provenance, homes and tags
_Generated 2026-11-21 23:37 +07 by `bin/gen_skills_index.py` from `skills/SOURCES.json`. Do not hand-edit rows: edit SOURCES.json and re-run._
## The homes (one copy each)
| Home | Path | What it is |
|---|---|---|
| authoring | `peachtukta1014/.github` -> `skills/` | the public repo lanes import from |
| working copy | `/srv/repos/hq/vm-hq-core/skills/` | the clone lanes read and edit; this INDEX lives here |
| install target | `/var/minis/skills/` (device) | what the app loads — installed, never hand-edited |
## Publishing (manual, Peach 2026-11-21)
The 15-minute `skills-publish.timer` is **off**. Push by hand when the library changes:
```
bash /srv/repos/hq/vm-hq-core/bin/publish-skills.sh
```
## Tag legend
`source` = where it came from (**team** ours · **minis** built-in · **OpenMinis** official · a hub name) · `readiness` = **ready** (works as-is) or **adapt** (edit before use) · `where` = **device** (iSH on the phone) / **vm** / **both** / **prompt-only** · `runtime` = what it needs.
**Provenance rule:** a row is exact only when SOURCES.json says `verified: true`. Rows marked *(unverified)* came from a shared hub / the internet and their repo is not pinned yet — adapt the body and scripts for us before relying on them (Peach 2026-11-21).

## Categories (from SOURCES.json)
| # | Category | Skills |
|---|---|---|
| 1 | Team + system | `bridge-check`, `core-ops`, `system-protocol-design`, `wo-loop` |
| 2 | Dev discipline | `dev-agent-md-refactor`, `dev-debugging-recovery`, `dev-git-workflow`, `dev-parallel-agents`, `dev-verification-gate` |
| 3 | Documents | `docs-diagram`, `docs-pdf-converter`, `docs-readmes`, `docs-typst-report` |
| 4 | Research | `research-gem-seeker`, `research-reader` |
| 5 | Ops + infra | `cloud-gcp-waf`, `ops-disk-scan` |
| 6 | Data | `data-context-extractor`, `dev-sql-optimization`, `vector-index-tuning` |
| 7 | Devices + UI | `hw-todoocard`, `ui-generative-minis` |
| 8 | Prompt + AI | `ai-prompt-engineer` |
| 9 | Authoring | `skill-creator` |


## Our team skills (5)
| skill | ไทย | tags | installed | what it does |
|---|---|---|---|---|
| `bridge-check` | เปิดสะพานถึง VM | team · ready · vm · net | yes | Our own. Bridge WAKE — open/heal the device-to-VM path. |
| `core-ops` | งานวิศวกรรม chinchaflow | team · ready · vm · python node net | yes | Our own. One engineering workflow for the chinchaflow repo. |
| `docs-diagram` | วาดไดอะแกรมเป็นไฟล์จริง | team · ready · vm · python typst | yes | Composed here from hub reference material (see shared/skills-hub-sources/INDEX_TH.md). Renders offline with Ty |
| `system-protocol-design` | ออกแบบโปรโตคอลเอเจนต์ | team · ready · vm · prompt-only | yes | Our own. Design or repair a multi-agent protocol. Peach 2026-11-21: keep, do not delete. |
| `wo-loop` | บูทเลน + ใบงาน | team · ready · vm · python gh-cli | no | Our own. Boot a lane then run the work loop; absorbed the two former team skills. |

## Minis built-in (0)
| skill | ไทย | tags | installed | what it does |
|---|---|---|---|---|

## Imported — by source (18)
| skill | upstream | source repo | ไทย | tags | installed | verdict |
|---|---|---|---|---|---|---|
| `ai-prompt-engineer` | prompt-engineer | Jeffallan/claude-skills | ออกแบบพรอมต์ LLM | claude-skills · adapt · vm · net | yes | KEEP+PATCH |
| `docs-pdf-converter` | pdf-converter | OpenMinis/MinisSkills | เอกสาร → PDF | MinisSkills · ready · vm · python typst | yes | KEEP |
| `hw-todoocard` | todoocard | OpenMinis/MinisSkills | จอ e-paper TodooCard | MinisSkills · ready · vm · python | yes | KEEP |
| `ops-disk-scan` | disk-scan | OpenMinis/MinisSkills | ดิสก์กินที่ไหน | MinisSkills · ready · vm · python zip git | yes | KEEP |
| `research-reader` | web-content-extractor | OpenMinis/MinisSkills | อ่านเนื้อหาเว็บ | MinisSkills · ready · vm · net | yes | KEEP |
| `ui-generative-minis` | generative-ui-minis | OpenMinis/MinisSkills | ข้อความ → HTML | MinisSkills · ready · vm · python | yes | KEEP |
| `cloud-gcp-waf` | google-cloud-waf-cost-optimization | hub (unverified) **(unverified)** | ค่าใช้จ่าย GCP | hub · adapt · vm · net | yes | KEEP+PATCH |
| `data-context-extractor` | data-context-extractor | hub (unverified) **(unverified)** | สร้างสกิลข้อมูล | hub · ready · vm · zip | yes | KEEP |
| `dev-agent-md-refactor` | agent-md-refactor | hub (unverified) **(unverified)** | จัด AGENTS.md | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-debugging-recovery` | debugging-and-error-recovery | hub (unverified) **(unverified)** | หาสาเหตุบั๊ก | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-git-workflow` | git-workflow-and-versioning | hub (unverified) **(unverified)** | วินัย git / PR | hub · adapt · vm · node git | yes | KEEP+PATCH |
| `dev-sql-optimization` | sql-optimization-patterns | hub (unverified) **(unverified)** | จูน SQL | hub · ready · vm · prompt-only | yes | KEEP |
| `docs-readmes` | crafting-effective-readmes | hub (unverified) **(unverified)** | เขียน README | hub · ready · vm · prompt-only | yes | KEEP |
| `docs-typst-report` | typst-pdf-maker | hub (unverified) **(unverified)** | รายงาน PDF (Typst) | hub · adapt · vm · python typst | yes | KEEP+PATCH |
| `research-gem-seeker` | github-gem-seeker | hub (unverified) **(unverified)** | หา OSS จาก GitHub | hub · adapt · vm · python node net | yes | KEEP+PATCH |
| `vector-index-tuning` | vector-index-tuning | hub (unverified) **(unverified)** | จูน vector index | hub · ready · vm · prompt-only | yes | KEEP |
| `dev-parallel-agents` | dispatching-parallel-agents | obra/superpowers | แบ่งงานขนาน | superpowers · adapt · vm · prompt-only | yes | KEEP+PATCH |
| `dev-verification-gate` | verification-before-completion | obra/superpowers | ยืนยันก่อนปิดงาน | superpowers · ready · vm · prompt-only | yes | KEEP |

## Counts
- library **23** · ours **5** · built-in **0** · imported **18** · installed on device **22**
- provenance verified: **13** / 23 — the rest are hub/internet imports whose repo is not pinned yet
- 2026-11-18 audit (code lane): KEEP 6 · KEEP+PATCH 11 · ARCHIVE 9 · DELETE 18 (`docs/reports/skills-audit-20261118.md`)

## Gates
```
python3 /srv/repos/hq/vm-hq-core/bin/gen_skills_index.py
```
