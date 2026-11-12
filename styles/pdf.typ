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

// 3. Exercises and assumptions.
// orange-book centres all figures (`show figure: set align(center)`), which overrides
// theorion's left alignment of exercise frames (they are figures of kind "exercise").
#show figure.where(kind: "exercise"): set align(start)
// theorion replaces each frame by its bare body (`it => it.body`), so the frame's first
// paragraph joins the surrounding text: when it follows another paragraph (e.g. the end
// of the previous exercise) it gets the first-line indent of the body text. Wrap the
// body in its own block, where the first paragraph is never indented. This rule takes
// the place of theorion's, so it also sets the left alignment.
#show figure.where(kind: "exercise"): it => block(width: 100%, breakable: true, align(start, it.body))
#show figure.where(kind: "conjecture"): it => block(width: 100%, breakable: true, align(start, it.body))

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

// 6. Part pages.
// orange-book prints the part title and, at the bottom of the same page, a small table
// of contents of the part (chapters and sections) in a narrow, unbreakable box. Our
// parts have many sections, so the box is taller than the page: it runs off the top and
// overlaps the title. Keep the title page as in the template (tinted page, part numeral
// and title), and put the part's table of contents on the following page(s), at full
// text width and breakable.
#import "@preview/orange-book:0.7.1": part-state, part-counter, part-location, part-change, appendix-state, main-color-state, part-font-size-state, outline-small-depth-state, my-outline-small, large-text, outline-heading1, outline-heading2
#let part(title) = {
  pagebreak(to: "odd")
  part-change.update(x => true)
  part-state.update(x => title)
  part-counter.step()
  [
    #context { let her = here(); part-location.update(x => her) }
    #context {
      let main-color = main-color-state.at(here())
      let part-font-size = part-font-size-state.at(here())
      set par(justify: false)
      place(block(width: 100%, height: 100%, outset: (x: 3cm, bottom: 2.5cm, top: 3cm), fill: main-color.lighten(70%)))
      place(top + right, text(fill: black, size: large-text, weight: "bold", box(width: 60%, part-state.get())))
      place(top + left, text(fill: main-color, size: part-font-size, weight: "bold", part-counter.display("I")))
    }
  ]
  pagebreak()
  context {
    let main-color = main-color-state.at(here())
    let depth = outline-small-depth-state.at(here())
    // my-outline-small wraps the outline in a box; unwrap it so that it can break.
    show box: it => if it.has("body") and it.body.func() == outline { it.body } else { it }
    block(width: 100%, breakable: true, my-outline-small(title, appendix-state, part-state, part-location, part-change, part-counter, main-color, textSize2: outline-heading1, textSize4: outline-heading2, depth: depth, width: 100%))
  }
}

// 7. Tables without a caption.
// A table with a caption is a figure, which orange-book centres. A table without a caption
// (e.g. in a worksheet) is a bare `table`, which Typst places at the left margin. Centre
// every table; the alignment of the cells is unchanged.
#show table: it => align(center, it)
