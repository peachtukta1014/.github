---
name: core-ops
version: 2.0.0
description: "Unified chinchaflow engineering workflow: debug, audit, incident, CI/CD, MCP PR ops, release/deploy. Trigger on 'fix bug / ตรวจโค้ด / audit / ระบบล่ม / CI / merge PR / ปล่อยของ'."
tags: [1. Team + system, vm, ours, ours]
---

> Canonical: `$HQ_ROOT/skills/core-ops/SKILL.md` does not exist for this skill — device is canonical (`$HQ_ROOT/skills/core-ops/`).


# core-ops — unified chinchaflow engineering (debug · audit · incident · cicd · mcp · release · chain)

**Registered for the whole team.** Every lane may call this directly - no order, no owner's permission (Peach 2026-11-22). It is registered, so any agent reaches it; the lane's own scope decides what it *works on*, never what tooling it may *use*.

> ONE place for every engineering workflow in chinchaflow. The old
> `core-ops debug/audit/incident/cicd/mcp/release/chain` skills are merged here.
> Always: read the actual file before editing · smallest diff · never refactor
> working code · CI is the gate (green → auto-merge, red → fix) · never
> force-push main / never change secrets. **Iron rule from PR #638:** read the
> full function signature + grep every reference + run the smoke test before PR.

## Repo rules (all sections)
- Clone: `$HQ_ROOT/repos/chinchaflow` (pull first) · private repo —
  every GitHub curl needs `Authorization: Bearer $GH_TOKEN` (env only).
- Work branch: `open-minis_<agent>_<task>` (e.g. `open-minis_webhook_line-name-size`; underscore or dash allowed) → PR → pr-verify CI
  green → auto-merge (squash). One PR, one intent.
- High-risk (price/stock/order/bill/schema/delete-feature) → restate in Thai +
  wait for Peach's "OK" BEFORE editing.
- Repo rules (all sections) — current truth (2026-09-13): agent-control docs are NOT in the repo anymore (moved to Open Minis). In-repo truth = the code + rules files themselves (`firestore.rules`, `storage.rules`) + `system/SYSMAP_AGENT.md` (the path map).

---

## A. DEBUG — when Peach says "fix the bug / it's broken / error here"

The system's real-world debug flow (built from Peach's own scars, PR #638).

1. **Listen → check the shared board and active task** — translate symptom into expected vs actual behavior; high-risk confirm with Peach first.
2. **Search the shared Lessons KB first** — `python3 $HQ_ROOT/chincha/kb/kb.py search --keywords "<kw>"`. Never start from zero.
3. **Trace the data flow** — pull repo → open dep-map
   (`kb/dep-map-<system>.json` file→file) → topic→files table → follow the bad
   value upstream to the FIRST divergence.
4. **One hypothesis, one sentence** — "X wrong because Y, therefore Z". Can't
   fill the sentence → back to step 3. Change exactly 1 spot that tests it.
5. **3-layer check BEFORE PR** (the #638 lesson):
   - L1 syntax: `node --check <file>`
   - L2 references: `grep -rn '<new-name>' apps/<app>/src/` — names must match
     what's actually defined (never reference a `data` object inside a
     destructured-params function!)
   - L3 local smoke: `node /srv/repos/chinchaflow/apps/seafood-pos/scripts/smoke-test.mjs` (shrimp) /
     `node /srv/repos/chinchaflow/apps/chincha-tea/scripts/smoke-test.mjs` (tea). Heavy/cross-app → E2B
     (no cloud sandbox helper is shipped — the `e2b_smoke.py` route was removed 2026-10-26; run smoke tests locally or on the VM)
6. **Open PR → verify CI STARTED → done** (Mode A, Peach approved):
   - Auto-merge fires for **any branch** once the `CI` workflow is fully green
     (2026-11-14: the 2026-09-12 agent-branch gate was retired — every PR is
     CI-checked, so every green PR merges). Guards that still keep a PR open:
     draft, `hold`/`do-not-merge` label, HEAD sha changed, merge conflict, and
     any pending/failed check in `statusCheckRollup`.
   - After opening: do ONE check that the CI runs have actually STARTED (not
     finished — if they never start, re-trigger with an empty commit), then
     close the ledger row and finish. Completion arrives via bridge; react to
     red only after it is reported (never watch/wait for it).
7. **Close cleanly** — update the shared Lessons KB with a verified reusable lesson if appropriate; finish the v4 Scratchpad as completed and retained; update the Central Work Board and Work Ledger result row. Use `kb.py` and `sp.py`.

Never: edit without "why this line" · multiple changes per round · weaken a
failing test · merge on red CI · touch workflow files (.github/) without care.

---

## B. AUDIT — read-only code review ("ตรวจโค้ด/ดูบั๊ก/เช็คโค้ด/audit")

**Iron: no code changes / no PRs / no Issues** — report only, wait for Peach.

1. **Scope it** — which system (shrimp/tea/webhook/cron)? which area
   (money/stock/slip/voice/3-lang)? Unsure → restate before auditing.
2. **Use current in-repo truth** — `system/SYSMAP_AGENT.md` +
   rules files (`firestore.rules`, `storage.rules`) — don't scan the repo
   blindly. Audit reports live in `$HQ_ROOT/audit/`.
3. **Extend with dep-map** — `kb/dep-map-{webhook-core,seafood-pos,chincha-tea}.json`
   forward/reverse to find who a file touches.
4. **Audit** — search/grep first, ranged reads (full-file only <150 lines);
   check Security (OWASP frame → real code), Data integrity (money float,
   Firestore bypass, race), Error handling, Performance (N+1, unbounded),
   Maintainability (dup/constants/dead exports).
5. **Report** — verdict first (🟢 healthy / 🟡 needs_attention / 🔴 urgent) →
   summary → findings `file:line → issue → suggested fix` → no code changes.

Never: report what you didn't read this round · wander outside scope · generic
advice without a real file+line. Cross-app gotchas: tea must never import
`firebase/firestore`/`onSnapshot` (use firestoreRest.js) · shrimp oversell
guard must subtract offline-queue reservation (cartStock.js) · webhook
`teaDailySummary.js` has 2 copies — always compare both (drift watch).

---

## C. INCIDENT — production recovery runbook ("ระบบล่ม/bot เงียบ/ล็อกอินไม่ได้")

Project `chincha-eeed6`, functions region `asia-southeast1`. Diagnose first —
**never broad-deploy functions to recover** (2026-08-01: manual
`--only functions --force` with a subset wiped all 16 functions → recover via
CI workflow, full set).

1. **Triage 60s** — what does Peach see? which system? money/stock/customer
   involved → high-stakes, consider escalation.
2. **Playbooks** (real cases):
   - **A. Functions missing / LINE bot silent** → re-run Deploy Cloud Functions
     workflow (`deploy-functions.yml`) → verify both `lineWebhook` +
     `lineWebhookTea` return 200. Delete one function by name:
     `firebase functions:delete <name> --region asia-southeast1 --project chincha-eeed6`.
   - **B. Login 403 (shrimp_users)** → revert the offending commit (PR #629
     lesson) — don't patch auth live.
   - **C. Webhook non-200 after deploy** → read function logs → bad deploy →
     re-run full workflow; code bug → fix PR.
3. **Verify customer-facing path** — `lineWebhook` + `lineWebhookTea` must be
   HTTP 200 before calling it done.
4. **Escalate NOW (Thai, stop)** — 🔴 secret/token leaked · 🔴 customer/sales
   data at risk · 🔴 abnormal AI/Firebase cost.

---

## D. CICD — deploy + CI status + merge

> **DELIVERY (the rule):** PR/CI/deploy results arrive AUTOMATICALLY — the
> CI aggregator (`services/hq-core/src/ci_agg.js`) emits AT MOST ONE doc per
> outcome: one for "PR ready + merged", one immediate for any red check, one
> for deploy ok/FAILED.
> Auto-merge fires for ANY branch once workflow `CI` (the verify workflow is
> named `CI`; `PR Verify` no longer exists) is fully green.
> After opening a PR: check ONCE that CI has started running, close the ledger
> row, move on — NEVER wait/poll/watch CI to completion (not even "to close
> the loop"). Act only when a notification arrives.

The tools below are ON-DEMAND ONLY — use them when Peach asks for a status
check or when a notification says something went red and needs reading.
Never run them as a watch loop.

**Use the whole gate, not one partition.** `vm-hq-gate` is the team's single entrance and it has seven channels - `chincha` (shop channels) · `wo-channels` (dispatch, external: minis-tools) · `vm-shell` · `vm-operations` · `github` · `gcloud-platform` · `host-diagnostics`. This skill reaches for whichever one the step needs: `chincha` for the shop apps (PRs, CI, Firestore), `github` for org-level operations, `vm-shell`/`vm-operations` for host and service work, `gcloud-platform` for cloud resources, `host-diagnostics` for Peach's PC. Skill bodies are NOT a gate channel - they live in this trunk under `skills/` and are read through `vm-shell`. Registration is team-wide (Peach 2026-11-22): the tooling is never limited to the repo you are working in.

1. **Status check (on demand)** — `minis-mcp-cli call vm-hq-gate gate_call --input '{"category":"chincha","tool":"list_open_prs","arguments":{}}'`,
   `get_pr_status --input '{"prNumber": N}'` (always live, zero local tooling).
2. **Fallback via API** — curl PRs/runs/jobs with `$GH_TOKEN` (never echo token).
   Local toolset `/srv/work/chincha-status/` (`poll_gh.Use MCP.
3. **Merge** — normally do NOT merge by hand: auto-merge workflow handles green
   PRs (minis/*, hq/*, vm/*). Gate merge - special cases only (`gate_call(category='chincha', tool='merge_pr')`)
   only for special cases Peach orders, and only when CI is verified green.
4. **On red** — when the bridge reports a failure: read the run log, fix, PR
   again. That's reactive work after notification, never waiting.

---

## E. MCP — chincha workflow operator (minis-mcp-cli)

Server runs on the **VM** (24/7) via SSH stdio — local repo copy `mcp/server.cjs`
is NOT used anymore (2026-09-11: iSH npm cache broken; migrated to VM where
`/srv/secrets/vault/auth/firebase-sa.json` admin SA lives). Registered as **chincha**
(call server id `chincha`, never `Chincha`). Config:
`minis-mcp-cli add --name chincha --command ssh --args "jii-vm bash /opt/jii/start-mcp-chincha.sh"`.
8 tools:

| Tool | Use |
|---|---|
| `list_open_prs` | Open PRs (number, title, branch, CI, mergeable) |
| `get_pr_status` | CI check status per PR |
| `merge_pr` | Merge (squash) — only when CI green |
| `get_github_issue` | Issue details |
| `query_firestore` | Generic Firestore read (scope-validated) |
| `mesh_send` | Send a message via Central Mesh (Firestore mesh_messages) lane<->lane |
| `mesh_inbox` | Read mesh inbox (filter by scope/status) |
| `mesh_stats` | Central Mesh summary (counts by status) |

```bash
minis-mcp-cli call vm-hq-gate gate_call --input '{"category":"chincha","tool":"list_open_prs","arguments":{}}' --pretty
minis-mcp-cli call vm-hq-gate gate_call --input '{"category":"chincha","tool":"get_pr_status","arguments":{"prNumber":650}}' --pretty
minis-mcp-cli call vm-hq-gate gate_call --input '{"category":"chincha","tool":"merge_pr","arguments":{"prNumber":650}}' --pretty   # only green CI
minis-mcp-cli call vm-hq-gate gate_call --input '{"category":"chincha","tool":"query_firestore","arguments":{"path":"sales/abc123","scope":"seafood"}}' --pretty
```
Needs `GH_TOKEN` on the VM (`/etc/chincha/env/*.env` → symlink into the vault; SSH runs as ubuntu with GH_TOKEN set).
Firestore auth = VM SA at `/srv/secrets/vault/auth/firebase-sa.json` (the `/etc/jii/` shim was removed 2026-11-12;
every consumer reads the vault file directly via env (`FIREBASE_SERVICE_ACCOUNT_FILE`, `SA_PATH` = `/srv/secrets/vault/auth/*-sa.json`); `/etc/chincha/secrets/` holds no links at all).
Also: `minis-mcp-cli tools <server>` to discover live tools (chincha + github).

---

## F. RELEASE — safe deploy orchestration ("ปล่อยของ/อัป production")

Deploys are **workflow-driven** (merge → workflow → verify), never hand-run.

| Workflow | Deploys | Verify |
|---|---|---|
| `deploy-functions.yml` | All LINE Cloud Functions | webhooks return 200 |
| `deploy-hosting.yml` | Hosting shrimp + tea | build/deploy per target |
| `deploy-rules.yml` | Firestore + Storage rules | — |
| `deploy-scheduled-functions.yml` | Tea summary cron | deploy by name only |

**The ONE rule that caused a real outage:** never
`firebase deploy --only functions --force` by hand with a subset (wiped all 16
functions 2026-08-01). Remove one function by name (`functions:delete`). Pick
the narrowest workflow; watch `chincha-cicd`/MCP status; verify webhooks 200
after functions deploy; report Thai.

---

## G. CHAIN — project changes via MINIS_CHANGELOG ("มี PR ใหม่/อ่าน chain")

1. `cat $HQ_ROOT/chincha/MINIS_CHANGELOG/<YYYY-MM>/<YYYY-MM-DD>.md` — read today's
   manual team PR chain (newest PR at top). Folder rules: `MINIS_CHANGELOG/README.md`.
   Not auto-synced — agents write it by hand each time any PR is opened/merged on chinchaflow
   (full repo history stays in `docs/AGENT_CHANGELOG_TH.md`).
2. Deep dive only when needed — the full repo history lives in the repo (not mirrored to the app);
   for older PR detail use `git -C $HQ_ROOT/repos/chinchaflow` (central clone).
3. Sync KB to reality (main-pilot duty) — update `kb/<system>.json`. Repo rule
   docs (AGENTS.md etc.) are Peach's auto-sync — read, don't edit.
4. Report to Peach: what's new (PR/CI) · what updated (KB) · anything for her
   to decide · "พร้อมแล้ว — งานไหนต่อ?"

## Report to Peach (ALL sections)
Thai, short, mobile-friendly. Verdict/result first → what changed (file paths)
→ checks passed → anything Peach must decide → done.