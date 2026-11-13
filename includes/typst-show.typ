// Continuous reading layout: no recto/verso blank pages or print-binding margins.
#let accent = rgb("216b9c")
#set page(paper: "a5", margin: (x: 15mm, top: 16mm, bottom: 17mm), numbering: "1")
#set text(font: "DejaVu Serif", size: 10pt, lang: "en")
#set document(title: "Understanding Modern LLMs", author: "dragos-fotache")
#set par(justify: false, leading: 0.7em, spacing: 0.8em)
#set heading(numbering: "1.1", hanging-indent: 0pt)
#show heading: set text(font: "DejaVu Sans", fill: accent, weight: "bold")
#show heading.where(level: 1): it => {
  if it.body != [Appendices] {
    pagebreak(weak: true)
    it
  }
}
#show link: set text(fill: accent)
// Long worked solutions must flow across A5 pages instead of overflowing them.
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: true,
    fill: background_color,
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"),
    width: 100%,
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%,
      below: 0pt,
      block(
        fill: background_color,
        width: 100%,
        inset: 8pt)[#if icon != none [#text(icon_color, weight: 900)[#icon] ]#title]) +
      if(body != []){
        block(
          inset: 1pt,
          width: 100%,
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}
#let part(title) = block(above: 1.5em, below: 1em)[
  #text(font: "DejaVu Sans", size: 12pt, fill: accent, weight: "bold", title)
]
#let chapter(title, image: none, l: none) = {
  heading(level: 1, title)
  if l != none { label(l) }
}
#let appendices(title, hide-parent: false, body) = {
  state("appendix-state", none).update(true)
  counter(heading).update(0)
  set heading(numbering: "A.1")
  body
}
#align(center)[
  #v(14mm)
  #text(font: "DejaVu Sans", size: 23pt, fill: accent, weight: "bold")[Understanding Modern LLMs]
  #v(4mm)
  #text(size: 13pt)[From derivatives to transformers]
  #v(7mm)
  #text(size: 10pt)[A growing coursebook with derivations, exercises, and reviewed working]
  #v(9mm)
  #link("https://dragos-fotache.github.io/llm-coursebook/")[Read the interactive edition online]
]
#pagebreak()
#outline(depth: 2)
