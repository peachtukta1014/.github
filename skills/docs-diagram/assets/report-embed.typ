#set page(paper: "a4", margin: 2cm)
#set text(font: ("Noto Sans Thai", "Libertinus Serif"), size: 11pt)
#set heading(numbering: "1.")

= สถาปัตยกรรม (Diagram in PDF)

แผนภาพด้านล่างวาดด้วย CeTZ แล้วฝังเป็น SVG ในรายงาน:

#figure(
  image("diagram.svg", width: 70%),
  caption: [เส้นทาง event: Minis app → bridge → VM hq-core],
)

ตารางเทียบ:
#table(columns: 2, [ชั้น], [บทบาท], [Minis app], [ต้นทาง], [bridge], [ส่งต่อ], [VM], [canonical])
