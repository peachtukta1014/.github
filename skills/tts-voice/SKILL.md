---
name: tts-voice
description: "Speak text aloud in Thai or English: pick the right voice path first (Gemini 3.8 via the VM proxy, Google Cloud free tier, or keyless edge-tts), then call the registered tool. Use for any text-to-speech request."
tags: [7. Devices + UI, both, ready, team]
---

# TTS voice

Three voice paths exist. **Pick by cost and feature, not by habit** — the wrong default
burns paid credit for audio the free tier produces identically.

## Which path (decide in this order)

| Need | Path | Cost |
|---|---|---|
| Plain speech, any length, need rate/volume control | **edge-tts** (`tools.tts.edge_say`) | free, keyless, unlimited |
| Thai, good quality, long-form reading | **Google Cloud TTS** through the VM proxy | free 1M chars/month, then paid |
| Expressive/style narration, 30 curated voices | **Gemini 3.8 TTS** through the VM proxy | paid (OpenRouter) |

Default to **edge-tts** unless Peach asks for a specific voice or style. Say which path you used
and what it cost.

## Commands

```bash
# what exists: 2091 rows (30 studio voices + 2059 library), 29 locales
python3 tools/tts/find_voice.py --list
python3 tools/tts/find_voice.py --check Sulafat        # is a studio voice allowed?

# keyless, free, has --rate / --volume (the only path that does)
python3 tools/tts/edge_say.py --text "สวัสดีครับ" --voice th-TH-PremwadeeNeural --out /tmp/a.mp3
python3 tools/tts/edge_say.py --text "hello" --voice en-US-AriaNeural --rate +10%

# Google Cloud (free tier), Thai
curl -s -X POST https://vm-chincha-hq.tail9cf6ce.ts.net/v1/audio/speech \
  -H "Authorization: Bearer $TTS_PROXY_AUTH_TOKEN" -H 'Content-Type: application/json' \
  -d '{"model":"th-TH-Neural2-C","input":"สวัสดีครับ","voice":"th-TH-Neural2-C"}' -o /tmp/b.mp3

# Gemini 3.8 via the same proxy (paid)
  -d '{"model":"google/gemini-3.8-flash-tts","input":"...","voice":"Sulafat"}'
```

Thai voices that actually exist: `th-TH-PremwadeeNeural` (F), `th-TH-NiwatNeural` (M) for
edge-tts; `th-TH-Neural2-C` for Google Cloud. The Gemini studio whitelist is what
`--check` validates.

## Limits that are real (verified 2026-11-27)

- The **library half** of `voice_library.tsv` has **no Thai locale** (29 locales, none `th`) —
  Thai only comes from the studio list or edge-tts / Google Cloud.
- The upstream prompter pack's extra fields — `turns[]`, `style`, `speaker_voice_configs`,
  `backchannel` — **do not map** onto our `{model, input, voice}` API. Sending them is ignored,
  not an error. Details: `tools/tts/README.md`.
- The proxy is bound to `127.0.0.1:8765`; from the device it is reachable only over the tailnet
  at `https://vm-chincha-hq.tail9cf6ce.ts.net/v1`. There is no public route.
- `TTS_PROXY_AUTH_TOKEN` is a secret: reference it, never print it, never paste it into a file.

## Where the code lives

`tools/tts/` is a **registered tool group** (not a copy of the upstream skill): `find_voice.py`,
`edge_say.py`, `tools/tts/tools/tts/references/voice_library.tsv`, and `README.md` with the full limits list. This
skill is the routing layer — when to use which path; the tools are the implementation. Do not
duplicate the scripts here.

Upstream origin of the pack: `tts-prompter` (Peach's upload, 2026-11-27) — registered as tools,
because most of it could not be expressed in our API.

## Reporting

If Peach ordered a report of the run, use `bin/peach_report.py --lane <lane> --kind order
--ordered ...` (Thai body — a Peach-ordered report). Otherwise the pad is enough.

## What came in the uploaded pack (`tts-prompter.zip`, Peach 2026-11-27)

Nothing was dropped. The files live in the trunk's tool group; this skill routes to them:

| File in the zip | Where it is now | State |
|---|---|---|
| `scripts/find_voice.py` | `tools/tts/find_voice.py` (tool `tools.tts.find_voice`) | runs; `--check` validates the studio whitelist |
| `references/voice_library.tsv` | `tools/tts/references/voice_library.tsv` | 2091 rows, 30 studio + 2059 library, 29 locales (no `th`) |
| `references/voice_catalog.md` | `tools/tts/references/voice_catalog.md` | kept |
| `references/language_catalog.md` | `tools/tts/references/language_catalog.md` | kept |
| `SKILL.md` (21.8 KB) | `references/upstream-tts-prompter-SKILL.md` (this skill) | kept verbatim, **reference only** — it documents `turns[]`/`style`/`speaker_voice_configs`/`backchannel`, which our `{model,input,voice}` API cannot express |
| `edge_say.py` (ours, same day) | `tools/tts/edge_say.py` (tool `tools.tts.edge_say`) | the free keyless path; the only one with `--rate`/`--volume` |

Why a tool group plus this skill, not a skill that ships the scripts: RULE 14 — one home per
thing. Executable code belongs in `tools/`, callable by every channel as a registered tool; the
skill carries the *when/how*, not a second copy.

**Two copies, two jobs.** This skill ships the pack so it imports cleanly on the phone and works
offline. The *live runtime* is  (registered as ), and it is the copy the
VM actually runs. If the voice library or a script changes: update  first, then copy
the file here — a divergence between the two is a defect, not a style choice.
