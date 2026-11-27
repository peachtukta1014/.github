#import "@preview/cetz:0.3.4": canvas, draw

#set page(width: 12cm, height: 8cm, margin: 6mm)
#set text(font: ("Noto Sans Thai", "Noto Sans"))

#canvas({
  import draw: *
  let cnode(x, y, body, fill: blue) = {
    rect((x - 1.5, y - 0.4), (x + 1.5, y + 0.4), radius: 4pt,
         stroke: 0.8pt + fill.darken(20%), fill: fill.lighten(88%))
    content((x, y), align(center, text(size: 9pt, body)))
  }
  cnode(0, 0, [Minis app])
  cnode(0, -1.3, [bridge / tunnel])
  cnode(0, -2.6, [VM hq-core])
  line((0, -0.4), (0, -0.9), mark: (end: ">"))
  line((0, -1.7), (0, -2.2), mark: (end: ">"))
  content((1.9, -1.3), align(left, text(size: 8pt, fill: gray)[ws_exec]))
})
