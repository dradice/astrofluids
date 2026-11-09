// Fixes for the Typst/PDF output (Quarto 1.12, orange-book template).
// Included with `include-before-body`, i.e. after Quarto's definitions and after
// `#show: book.with(...)`, so these rules and definitions take precedence.

// 1. Breakable callouts.
// Quarto defines `callout` with `breakable: false`, so a callout that does not fit in
// the space left on a page moves to the next page, and one longer than a page runs off
// the bottom and is clipped. This redefinition (same signature, same look) lets the
// box continue on the next page.
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: true,
    fill: background_color,
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"),
    width: 100%,
    radius: 2pt,
    {
      // Title bar; `sticky` keeps it on the same page as the start of the body.
      block(
        inset: 1pt,
        width: 100%,
        below: 0pt,
        sticky: true,
        block(
          fill: background_color,
          width: 100%,
          inset: 8pt)[#if icon != none [#text(icon_color, weight: 900)[#icon] ]#title])
      if body != [] {
        block(
          inset: 1pt,
          width: 100%,
          above: 0pt,
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    }
  )
}

// 2. Boxed equations (`\boxed{...}`).
// Pandoc writes `\boxed{X}` as `#box(stroke: black, inset: 3pt, [$ X $])`, i.e. a
// *display* equation inside the box. Typst numbers it, so the equation number is
// printed twice and every later equation number is off by one with respect to the
// HTML; a box after other material is also pushed onto its own line. Render the inner
// equation inline (in display style) and unnumbered instead.
#show box: it => {
  // `numbering: none` must be set (not only overridden below) so that the inner
  // equation does not step the equation counter.
  set math.equation(numbering: none)
  show math.equation.where(block: true): eq => math.equation(
    block: false, numbering: none, math.display(eq.body))
  it
}

// 3. Exercises.
// orange-book centres all figures (`show figure: set align(center)`), which overrides
// theorion's left alignment of exercise frames (they are figures of kind "exercise").
#show figure.where(kind: "exercise"): set align(start)
