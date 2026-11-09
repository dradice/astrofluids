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
  // Size the inline equation by its actual ink (fractions etc.), not by the line
  // height; otherwise the box border cuts through tall content.
  set text(top-edge: "bounds", bottom-edge: "bounds")
  show math.equation.where(block: true): eq => box(inset: (x: 2pt, y: 3pt), math.equation(
    block: false, numbering: none, math.display(eq.body)))
  it
}

// 3. Exercises.
// orange-book centres all figures (`show figure: set align(center)`), which overrides
// theorion's left alignment of exercise frames (they are figures of kind "exercise").
#show figure.where(kind: "exercise"): set align(start)

// 4. Figure size.
// The SVG figures are drawn for the web, with labels at about 20 px so that they match
// the body text there; at their natural size in the PDF (1 px = 0.75 pt) the labels are
// ~15 pt against 10 pt body text, and most figures fill the whole text width. Scale SVGs
// to 65% of their natural size, and cap every image at 70% of the text width (raster
// images have no meaningful natural size).
#show image: it => layout(size => {
  let m = measure(it)
  let is-svg = type(it.source) == str and lower(it.source).ends-with(".svg")
  let target = if is-svg { m.width * 0.65 } else { m.width }
  target = calc.min(target, size.width * 0.7)
  if m.width > 0pt and target < m.width {
    scale(target / m.width * 100%, reflow: true, it)
  } else {
    it
  }
})

// 5. References to chapters.
// orange-book numbers chapters as "9." (with a period, for the chapter headings), so
// references print "Chapter 9." in the middle of a sentence. Drop the trailing period.
#show ref: it => {
  let el = it.element
  if el == none or el.func() != heading or el.level != 1 or el.numbering == none {
    return it
  }
  context {
    let nums = counter(heading).at(el.location())
    let n = if type(el.numbering) == str { numbering(el.numbering, ..nums) } else { (el.numbering)(..nums) }
    if type(n) == str { n = n.trim(".", at: end) }
    let sup = if it.supplement == auto { el.supplement } else { it.supplement }
    link(el.location(), [#sup~#n])
  }
}
