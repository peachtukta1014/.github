---
name: docs-diagram
description: "Draw diagrams (flowchart, sequence, ER, architecture, charts) to PDF/SVG/PNG offline via Typst + CeTZ."
allowed-tools: Read Write Edit Bash
tags: [3. Documents, vm, KEEP+PATCH, ours]
---

# docs-diagram — real diagram files, rendered offline

There is **no Chromium** in this setup, so Mermaid cannot be rendered to a file (mmdc / mermaid.ink /
Kroki are all out). The path that works is **Typst + CeTZ** (vector, offline, embeddable), with Mermaid
kept as the design-time lingua franca.

**Execution host: the VM.** All commands here run on `vm-chincha-hq` (Tailscale SSH `om-ssh`, or the WS
tunnel `ws_exec`). The device holds no tooling.

## Layout
```
docs-diagram/
  SKILL.md                    ← this file
  scripts/render_diagram.py   ← the renderer (resolves the package path per host, builds in a temp dir)
  assets/diagram-template.typ ← ready-to-edit flowchart template
  assets/report-embed.typ     ← how to embed an SVG in a report with caption/figure
  references/*.md             ← the knowledge library: 38 Mermaid types (from WH-2099/mermaid-skill)
  references/MERMAID_UPSTREAM_SKILL.md ← the upstream SKILL.md (workflow + type table)
```

## Workflow
1. **Pick the type** — open `references/<type>.md` (flowchart.md, sequenceDiagram.md,
   entityRelationshipDiagram.md, c4.md, architecture.md …) and decide what the reader must see.
2. **Draft in Mermaid first** (`.mmd` or a fenced block) to agree the structure with the user — cheap and fast to revise.
3. **Render for real as CeTZ** — copy `assets/diagram-template.typ` and edit the nodes/edges.
4. **Compile**
   ```
   python3 <skill-dir>/scripts/render_diagram.py <file.typ> --format pdf,svg,png --outdir <dir> --strict
   ```
5. **Embed in a report** — `image("<diagram>.svg")` inside a figure with a caption (see `assets/report-embed.typ`).
6. **Check by eye** — `pdftoppm -png -r 90 <file>.pdf <prefix>` and look at the PNGs: no boxes or text crossing lines.

## Rules measured on the host
- `typst` (0.15.1 on the VM) **does** fetch `@preview` packages from Universe; a vendored copy also exists at
  `$HQ_ROOT/tools/typst-packages/` (cetz 0.2.2, oxifmt 0.2.1) and `render_diagram.py` picks
  whichever host path exists. Nothing needs the device.
- The VM can read files under `/srv/...` normally — always render through `render_diagram.py` (it handles the
  package path and the scratch dir).
- Fonts: `("Noto Sans Thai", "Noto Sans")` for body text; `("Libertinus Serif", "Noto Serif Thai")` for print
  documents. `fonts-noto-cjk` is installed on the VM.
- `mmdc` / `chromium` / `d2` / `draw.io` / `plantuml` / `dot` are absent; graphviz can be added with
  `apt-get install graphviz` when a DOT graph is genuinely wanted.
- CeTZ 0.2.2 on Typst 0.15 is fine (the old `style is deprecated` warning is harmless).

## Minimum template
```typ
#import "@preview/cetz:0.2.2": canvas, draw
#canvas({
  import draw: *
  rect((0, 0), (3, 1), radius: 4pt, stroke: 0.8pt + blue.darken(20%), fill: blue.lighten(88%))
  content((1.5, 0.5), text(size: 9pt)[Minis app])
  line((1.5, 0), (1.5, -0.8), mark: (end: ">"))
})
```

## Known limits
- No auto-layout: CeTZ places coordinates by hand. For very large graphs use graphviz.
- A 50+ node diagram is not practical by hand — split it into several images or reach for Graphviz (`dot -Tsvg`).
- No automatic diagram diff: compare the rendered PNGs by eye.
