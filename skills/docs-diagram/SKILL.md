---
name: docs-diagram
description: วาดไดอะแกรม (flowchart, sequence, ER, สถาปัตยกรรม, กราฟ) เป็นไฟล์จริง PDF/SVG/PNG แบบออฟไลน์ ด้วย Typst+CeTZ และฝังลงรายงาน Typst ได้ทันที ใช้คลัง syntax Mermaid 38 ชนิดเป็นคลังความรู้ตอนออกแบบ. Use when the user asks for a diagram, flowchart, architecture picture, or a PDF that must contain one, and no browser/Chromium is available.
allowed-tools: Read Write Edit Bash
---

# docs-diagram — ไดอะแกรมจริงในไฟล์ PDF ออฟไลน์

เครื่องนี้ **ไม่มี Chromium** → Mermaid render เป็นไฟล์ไม่ได้ (mmdc/mermaid.ink/Kroki ใช้ไม่ได้)
ทางที่ใช้ได้จริงคือ **Typst + CeTZ** (เวกเตอร์, ออฟไลน์, ฝังลงรายงานได้เลย) และเก็บ Mermaid ไว้เป็นภาษากลางตอนออกแบบ

## โครงสร้าง
```
docs-diagram/
  SKILL.md                    ← ไฟล์นี้
  scripts/render_diagram.py   ← ตัวเรนเดอร์ (คัดลอก build ไป /root เพราะ typst อ่าน /var/minis ไม่ได้)
  assets/diagram-template.typ ← เทมเพลต flowchart พร้อมใช้
  assets/report-embed.typ     ← วิธีฝัง SVG ลงรายงาน + caption/figure
  references/*.md             ← คลัง knowledge: Mermaid 38 ชนิด (จาก WH-2099/mermaid-skill)
  references/MERMAID_UPSTREAM_SKILL.md ← SKILL.md ต้นฉบับ upstream (workflow + ตารางชนิด)
```

## เวิร์กโฟลว์
1. **เลือกชนิด** — เปิด `references/<type>.md` (flowchart.md, sequenceDiagram.md, entityRelationshipDiagram.md, c4.md, architecture.md …) ดูว่าผู้อ่านต้องเห็นอะไร
2. **ร่างเป็น Mermaid ก่อน** (`.mmd` หรือ fenced block) เพื่อตกลงโครงกับผู้ใช้ — ใช้เป็นภาษากลาง ราคาถูกและแก้ไว
3. **เรนเดอร์จริงเป็น CeTZ** — คัดลอก `assets/diagram-template.typ` แล้วแก้ node/edge
4. **คอมไพล์**
   ```
   python3 /var/minis/skills/docs-diagram/scripts/render_diagram.py <file.typ> --format pdf,svg,png --outdir <dir> --strict
   ```
5. **ฝังลงรายงาน** — `image("<diagram>.svg")` ใน figure พร้อม caption (ดู `assets/report-embed.typ`)
6. **ตรวจด้วยตา** — `pdftoppm -png -r 90 <file>.pdf <prefix>` แล้วเปิดภาพดู ต้องไม่มีกล่องสี่เหลี่ยม/ตัวอักษรทับเส้น

## กฎที่ต้องรู้ (วัดจริงในเครื่องนี้)
- `typst` ดึง package จาก Universe **ไม่ได้** (`Network Error ... os error 92`) → ทุก `@preview` ต้อง vendor ไว้ที่ `/var/minis/shared/tools/typst-packages/` (มี `cetz 0.2.2`, `oxifmt 0.2.0`)
- typst อ่านไฟล์ใต้ `/var/minis` **ไม่ได้** → สคริปต์จะ copy ไป `/root` ก่อนเสมอ ห้ามเรียก `typst` ตรง ๆ บน path ใต้ `/var/minis`
- ฟอนต์: `("Noto Sans Thai", "Noto Sans")` สำหรับเนื้อหา, `("Libertinus Serif", "Noto Serif Thai")` สำหรับเอกสารพิมพ์
- `mmdc` / `chromium` / `d2` / `draw.io` / `plantuml` / `dot` **ไม่มี** (graphviz ลงได้ด้วย `apk add graphviz` ถ้าต้องการกราฟ DOT)
- CeTZ 0.2.2 บน typst 0.12 เตือน `style is deprecated` — เป็น warning ปกติ ไม่กระทบผล

## เทมเพลตขั้นต่ำ
```typ
#import "@preview/cetz:0.2.2": canvas, draw
#canvas({
  import draw: *
  rect((0, 0), (3, 1), radius: 4pt, stroke: 0.8pt + blue.darken(20%), fill: blue.lighten(88%))
  content((1.5, 0.5), text(size: 9pt)[Minis app])
  line((1.5, 0), (1.5, -0.8), mark: (end: ">"))
})
```

## ข้อจำกัดที่รู้ตัว
- ไม่มี auto-layout: CeTZ วางพิกัดเอง (ต้องคำนวณ) — งานกราฟใหญ่มากให้ใช้ graphviz
- ผังซับซ้อน 50+ node ทำมือไม่ไหว → แนะนำ Graphviz (`dot -Tsvg`) หรือแยกเป็นหลายภาพ
- ไม่มี diagram-diff อัตโนมัติ: เทียบด้วยตาจาก PNG ที่เรนเดอร์
