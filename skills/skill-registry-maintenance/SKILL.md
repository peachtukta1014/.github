---
name: skill-registry-maintenance
description: Maintain a stable-ID skill registry and resolver without scattering hard-coded paths. Use when adding, moving, renaming, deprecating, or auditing repository skills and their machine-readable lookup.
license: Internal
metadata:
  version: "1.0.0"
  domain: system
  triggers: skill registry, skill resolver, stable skill id, rename skill, move skill, skill lookup, registry audit, progressive disclosure
  role: specialist
  scope: implementation
---

# Skill Registry Maintenance

Maintain skill identity separately from the current filesystem location. Treat the machine-readable registry as the lookup authority and Markdown catalogues as projections for humans.

## Core contract

- Keep `skill_id` stable across moves and renames.
- Resolve `skill_id` or an approved alias through `registry/skills.json`.
- Keep the skill body in the canonical `skills/<current-id>/SKILL.md` location unless the registry says otherwise.
- Keep provenance in `skills/SOURCES.json`; do not invent a second provenance table.
- Treat `system/SKILL_REGISTRY.md` and `skills/INDEX.md` as generated or human-facing projections, never as runtime authorities.
- Never register `skills/_inbox/` or other quarantine content as runnable.
- Never place secrets, credentials, or tokens in the registry, skill body, test fixtures, or evidence.

## Workflow

### 1. Discover existing authorities first

From the repository root, inspect the current state before editing:

```bash
git status --short --branch
find registry -maxdepth 1 -type f -print | sort
find bin -maxdepth 1 -type f -iname '*skill*' -print | sort
python3 -m json.tool skills/SOURCES.json >/dev/null
```

Check for existing registry-like files, generated catalogues, publisher workflows, and quarantine directories. Reuse an existing authority; do not create a competing registry.

### 2. Define or preserve identity

For a new skill, choose a lowercase, ASCII, hyphenated `skill_id`. For an existing skill, preserve its current ID even if its directory or display name changes. Put human-language names and former names in `aliases`, not in the stable ID.

Use one registry record per skill. A record should contain, at minimum:

```json
{
  "skill_id": "example-skill",
  "slug": "example-skill",
  "version": "1.0.0",
  "status": "active",
  "entry": "skills/example-skill/SKILL.md",
  "source": {},
  "distribution": {},
  "load": {},
  "triggers": {},
  "requires": {},
  "aliases": [],
  "owner": "internal"
}
```

Use `status: external` when a source is registered but no local body exists. External records may be discoverable as metadata but must not be treated as local runnable content.

### 3. Build or update the registry

Update `skills/SOURCES.json` first when provenance or category data changes. Then update `registry/skills.json` so every source ID has exactly one record. Keep `entry` relative to the repository root and make `load.body` point to the same resolved body.

For a move or rename:

1. Move the skill body.
2. Keep `skill_id` unchanged.
3. Change only the registry entry/path fields.
4. Preserve aliases for old display names or upstream names.
5. Verify that no quarantine path is runnable.

Do not copy the entire skill body into the registry. The registry should remain metadata-sized; load the body only after resolution.

### 4. Implement or update the resolver

The resolver must:

- accept a stable ID and exact aliases;
- load the registry rather than scanning directories as its authority;
- resolve paths relative to the repository root;
- reject path traversal and quarantine entries;
- distinguish local `active` records from `external` records;
- provide metadata, body, and resource-list modes;
- include a registry digest in machine-readable metadata for evidence.

The repository resolver is:

```bash
bin/skill-read <skill_id> --metadata
bin/skill-read <skill_id> --metadata --json
bin/skill-read <skill_id> --body
bin/skill-read <skill_id> --resources
```

Keep existing lookup commands backward-compatible when replacing directory scans with registry resolution.

### 5. Validate before claiming completion

Run all applicable checks from the repository root:

```bash
python3 -m json.tool registry/skills.json >/dev/null
python3 -m py_compile bin/skill-read
bin/skill-read <known-id> --metadata
bin/skill-read <known-id> --body >/dev/null
bin/skill-read <known-alias> --metadata --json
bin/skill-read <external-id> --body   # must fail safely when no local body exists
git diff --check
```

Also compare the ID sets in `skills/SOURCES.json` and `registry/skills.json`. Check for duplicate IDs, duplicate aliases, missing local entries, path traversal, quarantine paths, unexpected generated-file drift, and secret-like values.

Record fresh evidence: command, result, registry digest where relevant, and the changed files. Do not claim a skill is runnable merely because its metadata exists.

### 6. Commit as a narrow change

Do not migrate all lanes, rewrite boot contracts, or refactor unrelated lookup tools in the same change. Prefer one atomic commit for the registry/resolver slice and a separate change for boot or lane migration.

Before committing:

```bash
git diff --cached --name-status
git diff --cached -i -G'password|secret|api[_-]?key|token|private[_-]?key' --name-only
git status --short --branch
```

Use a descriptive conventional commit such as:

```text
feat: add stable skill registry resolver
```

Push only to an explicitly named feature branch. Do not merge or alter protected branches without explicit authorization.

## Progressive loading

Load only metadata during discovery. Load the selected `SKILL.md` body after resolution. Load scripts, references, and templates only when the selected task requires them. Never preload every skill or every lane during agent boot.

## Failure handling

- **Duplicate ID or alias:** stop and report the conflicting records.
- **Missing local entry:** mark it `external` or `blocked`; do not guess a path.
- **Quarantine entry:** reject it; quarantine content is not runnable.
- **Registry/body drift:** stop, report both paths and hashes, and repair the authority before execution.
- **Unknown request:** return a structured no-match result; do not fall back to arbitrary directory scanning.
