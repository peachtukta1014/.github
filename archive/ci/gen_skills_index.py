#!/usr/bin/env python3
"""gen_skills_index — rebuild skills/INDEX.md in the skills working clone (files lane, 2026-11-21).

Reads every skill dir in the clone, takes name + description from the SKILL.md frontmatter,
classifies by the prefix rule (a category prefix = supplementary; no prefix = team/system),
and marks whether the skill is installed on the device. Writes the file in place (root-owned).
"""
import os
import re
import subprocess
import sys
import time

CLONE = "/srv/repos/skills-shared/skills"
OUT = os.path.join(CLONE, "INDEX.md")

DEVICE = """ai-prompt-engineer boot bridge-check cloud-gcp-waf core-ops data-context-extractor
dev-agent-md-refactor dev-debugging-recovery dev-git-workflow dev-parallel-agents
dev-sql-optimization dev-verification-gate docs-diagram docs-pdf-converter docs-readmes
docs-typst-report hw-todoocard ops-disk-scan research-gem-seeker research-reader
skill-creator system-protocol-design ui-generative-minis vector-index-tuning wo-boost""".split()

CAT = {
    "ai": "AI / prompt", "cloud": "Cloud (GCP)", "dev": "Dev discipline",
    "docs": "Docs & documents", "hw": "UI & hardware", "ops": "Ops / VM & system",
    "research": "Research & web", "ui": "UI & hardware",
}
TEAM_NOTE = {
    "boot": "lane boot (identity + scope + pad + board)",
    "bridge-check": "open/heal the device-to-VM path (bridge WAKE)",
    "core-ops": "one engineering workflow for the chinchaflow repo (debug/audit/CI/release)",
    "wo-boost": "work-order skill: dispatch / ACK / close, locator first",
    "skill-creator": "author a new skill to this library's shape",
    "data-context-extractor": "grow a company-specific data-analysis skill from analyst knowledge",
    "system-protocol-design": "design or repair a multi-agent protocol",
    "vector-index-tuning": "tune a vector index (HNSW, quantisation)",
}


def front(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    name = re.search(r'^name:\s*"?([^"\n]+)"?', txt, re.M)
    desc = ""
    lines = txt.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^description:\s*(>?-?)\s*(.*)$", line)
        if not m:
            continue
        buf = [m.group(2)]
        for nxt in lines[i + 1:]:
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s", nxt) or nxt.strip() == "---":
                break
            buf.append(nxt)
        desc = " ".join(" ".join(buf).split())
        break
    return (name.group(1).strip() if name else os.path.basename(os.path.dirname(path))), desc[:150]


rows = []
for d in sorted(os.listdir(CLONE)):
    p = os.path.join(CLONE, d, "SKILL.md")
    if not os.path.isdir(os.path.join(CLONE, d)) or not os.path.isfile(p):
        continue
    name, desc = front(p)
    prefix = d.split("-")[0]
    if d in TEAM_NOTE:
        cat = "team / system"
        note = TEAM_NOTE[d]
    else:
        cat = CAT.get(prefix, "team / system")
        note = desc
    rows.append((d, cat, "yes" if d in DEVICE else "no", note))

team = [r for r in rows if r[1] == "team / system"]
sup = [r for r in rows if r[1] != "team / system"]
missing = [r[0] for r in rows if r[2] == "no"]
orphan = [d for d in DEVICE if d not in [r[0] for r in rows]]

out = []
out.append("# Skills registry — the library, its prefixes and its homes\n")
out.append("_Generated %s by `skills-shared/bin/gen_skills_index.py` (files lane). Do not hand-edit rows: re-run the generator._\n"
           % time.strftime("%Y-%m-%d %H:%M %Z"))
out.append("## The homes (one copy each, no second source)\n")
out.append("| Home | Path | What it is |\n|---|---|---|\n"
           "| authoring | `peachtukta1014/.github` -> `skills/` | the public repo where a skill is written and reviewed (PR) |\n"
           "| working copy on the VM | `/srv/repos/skills-shared/skills/` | the clone lanes read and edit; this INDEX lives here |\n"
           "| install target | `/var/minis/skills/` (device) | what the app loads — installed, never hand-edited |\n")
out.append("The vault mirror `/srv/repos/hq/vm-hq-core/skills/` was **removed on 2026-11-21** (proven byte-duplicate of the "
           "working copy; archive `_archive/skills-mirror-20261121/`). Device home `/var/minis/shared/skills` never existed.\n")
out.append("## The prefix rule\n")
out.append("**A prefix is a category, not a rename.** No prefix = a **team/system** skill (boot, bridge-check, core-ops, "
           "wo-boost, skill-creator, data-context-extractor, system-protocol-design, vector-index-tuning) — it is used by every "
           "lane and keeps its bare name. A prefix = a **supplementary** skill in a subject area (`dev-`, `docs-`, `research-`, "
           "`ops-`, `hw-`, `ui-`, `ai-`, `cloud-`). Names are stable identifiers (AGENT.md RULE 1): a move between the two groups "
           "is decided by Peach, never by the generator.\n")
out.append("## Team / system skills (%d)\n" % len(team))
out.append("| skill | installed | what it does |\n|---|---|---|\n")
for d, _, inst, note in team:
    out.append("| `%s` | %s | %s |\n" % (d, inst, note))
out.append("\n## Supplementary skills (%d)\n" % len(sup))
out.append("| category | skill | installed | what it does |\n|---|---|---|---|\n")
for d, cat, inst, note in sup:
    out.append("| %s | `%s` | %s | %s |\n" % (cat, d, inst, note))
out.append("\n## Counts\n")
out.append("- library: **%d** skills · installed on the device: **%d**\n" % (len(rows), sum(1 for r in rows if r[2] == "yes")))
out.append("- in the library but not installed: %s\n" % (", ".join("`%s`" % m for m in missing) or "none"))
out.append("- installed but missing from the library: %s\n" % (", ".join("`%s`" % o for o in orphan) or "none"))
out.append("- archived (pruned 2026-11-21, on the VM): `_archive/skills-pruned-20261121/` — `agentic-eval`, "
           "`internet-skill-finder`, `reflex`\n")
out.append("\n## Gates\n")
out.append("```\npython3 /srv/repos/skills-shared/bin/gen_skills_index.py     # rebuild this file\n"
           "python3 /srv/repos/skills-shared/bin/doc_id_lint.py         # doc ids: no BROKEN and no MOVED stub\n```\n")

body = "".join(out)
tmp = "/tmp/INDEX.md.new"
open(tmp, "w", encoding="utf-8").write(body)
subprocess.run(["sudo", "-n", "cp", tmp, OUT], check=True)
subprocess.run(["sudo", "-n", "chmod", "644", OUT], check=True)
print("wrote %s  %d bytes  (%d rows: %d team, %d supplementary, %d not installed)"
      % (OUT, len(body.encode()), len(rows), len(team), len(sup), len(missing)))
