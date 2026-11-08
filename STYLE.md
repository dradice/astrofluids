# Writing conventions

## Chapters

- One file per chapter, `chapters/<slug>.qmd`. Slugs have no numbers and are never renamed (they are the page URLs). The order lives only in `_quarto.yml`.
- The chapter list, with each chapter's **label key**, lives in `tools/chapters.py`. Every label in a chapter starts with that key.
- Each chapter starts with `# Title {#sec-<key>}`. Structure:
  1. Body sections. Optional material goes in `::: {.callout-note collapse="true"}` boxes titled "Going further".
  2. `## In-class worksheet {#sec-<key>-worksheet}`
  3. `## Exercises {#sec-<key>-exercises}`
  4. `## Further reading {#sec-<key>-reading}`: textbook sections first [@clarke2007].
- **Exercise numbers depend on chapter order.** During the semester, chapters may only be appended, never inserted or reordered.

## Math

- Inline `$...$`. Display:

  ```markdown
  $$
  \partial_t \rho + \nabla\cdot(\rho \vb{v}) = 0
  $$ {#eq-continua-continuity}
  ```

- **Every display equation gets a label** (`#eq-<key>-<name>`) so that it is numbered. Use descriptive names. Sequential names like `eq-sound-12` are acceptable for equations no one references yet.
- Multi-line derivations use `\begin{aligned}...\end{aligned}` inside `$$`, with one label for the whole block.
- **Equations inside solutions get no label.** Otherwise equation numbers would differ between the public and the solutions builds.
- Macros are provided by `filters/macros.lua`. Do not define `\newcommand` in chapters.
  - `\vb{v}`, `\vb{\xi}`: vectors in bold. Latin letters are upright (`\mathbf`); Greek letters use `\boldsymbol` (bold italic), as in the LaTeX `physics` package.
  - `\dd`, `\ii`, `\ee`: upright d, i, e.

  To add a macro, edit the tables at the top of the filter.
- Use `\boxed{...}` for key results.

## Exercises and solutions

```markdown
::: {#exr-hydro-lane-emden}
## Lane–Emden equation
Statement...
:::

::: {.content-visible when-profile="solutions"}
::: {.solution}
Solution... (no equation labels in here)
:::
:::
```

- The `.solution` class is what `tools/check-no-solutions.sh` looks for. Always use it.
- Exercises adapted from textbooks are rewritten in our own words and credited, e.g. "Adapted from @clarke2007, Problem 8." Never copy textbook wording.
- Assumptions use `::: {#cnj-<key>-<name>}` with a `## Title` (rendered as "Assumption N.k").

## Figures

```markdown
![Caption sentence.](../figures/<slug>/name.svg){#fig-<key>-name fig-alt="What the figure shows and why it matters."}
```

- Every figure has a caption and `fig-alt`. The alt text describes the content; it is never LaTeX source. Decorative images use `fig-alt=""`.
- Refer to figures as `@fig-...`, never "the figure above".
- Editable sources (Inkscape SVG, Python scripts) go in `figures-src/<slug>/`.
- Never rely on colour alone: also use line styles or labels. Graphical elements need at least 3:1 contrast.
- Images from other sources need a compatible license and a credit line in the caption.

## Citations

`[@key]`, with entries in `references.bib`. Include a DOI or ADS bibcode when there is one.
