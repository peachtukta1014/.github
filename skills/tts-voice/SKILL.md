---
name: tts-voice
description: "Speak text aloud in Thai or English: pick the right voice path first (Gemini 3.8 via the VM proxy, Google Cloud free tier, or keyless edge-tts), then call the registered tool. Use for any text-to-speech request."
tags: [7. Devices + UI, both, ready, team]
---

# TTS voice

Three voice paths exist. **Pick by cost and feature, not by habit** — the wrong default
burns paid credit for audio the free tier produces identically.

## Which path (decide in this order)

| Need | Path | Cost | Measured 2026-11-27 |
|---|---|---|---|
| Thai speech, any length | **Google Cloud TTS** `th-TH-Neural2-C` via the VM proxy | free 1M chars/month | **works** — HTTP 200, 21,120 B, 2.64 s |
| Expressive/style narration, 30 curated voices | **Gemini 3.8 TTS** via the same proxy | paid (OpenRouter) | **works** — HTTP 200, 19,316 B |
| Need `--rate` / `--volume` | **edge-tts** (`tools.tts.edge_say`) | free, keyless | **partial** — short Thai works (11,232 B / 1.87 s); a longer Thai sentence returns **0 bytes, rc=1**. Do not use it for long text until that is fixed |

**Default to Google Cloud `th-TH-Neural2-C`.** It is free to 1M chars/month and it is the only
path that passed on long Thai text today. State which path you used and what it cost.
The proxy needs `Authorization: Bearer $TTS_PROXY_AUTH_TOKEN` even on 127.0.0.1 (a bare POST
returns 401) — reference the variable, never print it.

**edge-tts long-text defect is open** (Peach 2026-11-27): `edge-tts --write-media` with a full
sentence fails inside `edge_tts/util.py` on Python 3.14 and writes a 0-byte file. Capture the
traceback, fix or pin, then update this row.


## Getting the audio to play inside Open Minis (proven 2026-11-27)

The app plays audio itself — you do not need a provider round trip to hear a file the VM made:

1. Generate on the VM: `curl ... -o /tmp/a.mp3` (or `edge_say.py --out`).
2. Bring it to the phone: `om-ssh "cat /tmp/a.mp3" > /var/minis/attachments/a.mp3`
3. Put it in the chat as a Markdown audio link: `![voice](minis://attachments/a.mp3)` —
   add `?auto_play=true` when Peach asked to hear it immediately.

That is the whole delivery path. Proven with a 21,120-byte, 2.64-second Thai file that played in
the chat.

Two separate wiring questions, do not mix them up:

| Want | How |
|---|---|
| Hear a file we already made | attachment link above — no provider needed |
| The app's own speech feature should call OUR endpoint | Providers → Custom: Base URL `https://vm-chincha-hq.tail9cf6ce.ts.net`, model id `google/gemini-3.8-flash-tts` or `th-TH-Neural2-C`, plus the token. That is provider `6486BDD0…` ("OR key (TTS)") |

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

Why the pack is also in `tools/tts/`: executable code belongs where every channel can call it as
a registered tool (RULE 14). This skill is the portable package — it ships the same files so an
import on the phone works with no VM round trip.

**Two copies, two jobs.** This skill ships the pack so it imports cleanly on the phone and works
offline. The *live runtime* is `tools/tts/` (registered as `tools.tts.*`), and that is the copy the
VM actually executes. If the voice library or a script changes: update `tools/tts/` first, then
copy the file here — a divergence between the two is a defect, not a style choice.
