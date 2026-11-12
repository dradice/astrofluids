# Writing conventions

## Chapters

- One file per chapter, `chapters/<slug>.qmd`. Slugs have no numbers and are never renamed (they are the page URLs). The order lives only in `_quarto.yml`.
- The chapter list, with each chapter's **label key**, lives in `tools/chapters.py`. Every label in a chapter starts with that key.
- Each chapter starts with `# Title {#sec-<key>}`. Structure:
  1. Body sections. Optional material goes in `::: {.callout-note}` boxes titled "Going further: ...". Do not use `collapse="true"`: Quarto's collapsible callouts cannot be opened with the keyboard and fail axe.
  2. `## In-class worksheet {#sec-<key>-worksheet}`
  3. `## Exercises {#sec-<key>-exercises}`
  4. `## Further reading {#sec-<key>-reading}`: textbook sections first [@clarke2007].
- **Exercise numbers depend on chapter order.** During the semester, chapters may only be appended, never inserted or reordered.

## Notation (decided in the Phase 3 review; apply in each chapter as it is reviewed)

- **Mean molecular weight** $\mu$ is dimensionless: $\rho = \mu m_u n$, $p = \rho k_B T / (\mu m_u)$, with $m_u$ the atomic mass unit (Ch. 1, @eq-continua-mu).
- **Cylindrical coordinates** are $(R, \phi, z)$; $R$ is the cylindrical radius. A star's radius is then $R_*$ (or $R_\odot$ etc.).
- **Volume and area elements**: $\dd V$ and $\dd A$; the volume of a region $\Omega$ is $V_\Omega$.
- **Lagrangian label** (initial position of a fluid element): $q$ (or $\vb{q}$), never $p$.
- $\dd/\dd t$ is the rate of change following a fluid element (Ch. 1, Ch. 5).
- **Energy densities**: $u = \rho\varepsilon$ is the internal energy density; $u_{\mathrm{rad}}$ the radiation energy density when more than one source is present (Ch. 2). Photon energy: $\varepsilon_{\mathrm{ph}}$.
- **Specific volume** $v = 1/\rho$ is allowed (Ch. 2), with a sentence saying it is not the velocity.
- **Vertical direction**: $z$ points up, $\vb g = -g\hat{\vb z}$, $\partial_z p = -\rho g$ (Ch. 4 onwards). When gravity depends on $z$ (slabs, disks), use the signed component $g_z = \vb g\cdot\hat{\vb z}$, so $\partial_z p = \rho g_z$ (Ch. 4, 8, 14, 18).
- **Mean free path** $\lambda$; **scale heights** $H$; **heat flux** $\vb F_{\mathrm{heat}}$; heating rate per unit mass $\dot q$.
- **Balance laws**: $\partial_t U + \nabla\cdot\vb F = S$ (Ch. 6, @tbl-conserv-summary).
- **Energies of a system**: kinetic $K$, internal $U$, gravitational $W$ (Ch. 3, 8). Volume elements in double integrals over positions: $\dd^3 r$, $\dd^3 r'$ (the one exception to $\dd V$). Enclosed mass $M(r)$.
- **Sound speeds**: $c_s = \sqrt{(\partial p/\partial\rho)_s}$ is the adiabatic sound speed; $c_{\mathrm{iso}} = \sqrt{k_B T/(\mu m_u)} = c_s/\sqrt{\Gamma}$ the isothermal one (Ch. 9, @eq-sound-isothermal). Not $a$, which is the radiation constant. Chapters that only deal with isothermal gas (Ch. 4, 8) may write $c_s$ for it.
- **Stratified atmospheres** (Ch. 10): scale height $H = c_{\mathrm{iso}}^2/g$; acoustic cutoff $\omega_{\mathrm{ac}} = c_s/(2H)$; buoyancy (Brunt–Väisälä) frequency $N$. Polytropic constant $K$ (not $A$).
- **Turbulence** (Ch. 20): energy injection/flux/dissipation rate per unit mass $\mathcal P = v^3(\ell_0)/\ell_0$ (not $\varepsilon$, which is the specific internal energy); dissipation scale $\ell_d$; averages $\bar{\vb v}$ (with `\overline` only for products).
- **MHD** (Ch. 22): SI electromagnetism, $\nabla\times\vb B = \mu_0\vb j$ with $\vb j$ in A/m², $\sigma$ in S/m; $\eta = 1/(\mu_0\sigma)$ is the magnetic diffusivity (the resistivity is written $1/\sigma$); total energy written out as $\rho(\varepsilon + \tfrac12 v^2)$ (no symbol $e$, which is the electron charge); angular momentum density $\vb m$ in MHD chapters.
- **Magnetic tension** (Ch. 24): plasma beta $\beta = 2\mu_0 p/B^2$; magnetic pressure $B^2/2\mu_0$; $\alpha_0 = 1/\beta$ only in the Parker atmosphere. Curvature vector $\vb\kappa = (\hat{\vb b}\cdot\nabla)\hat{\vb b}$.
- **MHD waves** (Ch. 25): Alfvén velocity $\vb v_A = \vb B_0/\sqrt{\mu_0\rho_0}$, $v_A = |\vb v_A|$; Alfvén frequency $\omega_A = \vb k\cdot\vb v_A$ (used in Ch. 26). Alfvénic Mach number $\mathrm{Ma}_A = u/v_A$. The slow mode is the one with the smaller phase speed. Fourier convention $\ee^{\ii(\vb k\cdot\vb x - \omega t)}$, so $\nabla\to\ii\vb k$, $\partial_t\to-\ii\omega$.
- **Disks and the MRI** (Ch. 18, 26): cylindrical coordinates $(R, \phi, z)$, with φ for the azimuth (not θ) and subscript $R$ for radial components ($u_R$, $B_R$). Growth rates are $\lambda = -\ii\omega$, so $\lambda^2 > 0$ means instability. Epicyclic frequency $\kappa$, $\kappa^2 = 4\Omega^2 + \dd\Omega^2/\dd\ln R$. Magnetic diffusivity $\eta$, as in Ch. 22–23.
- **Notation sweep (2026-11-11, `review/notation-sweep.md`)**:
  - **Mach number** $\mathrm{Ma}$ (Alfvénic $\mathrm{Ma}_A$). $\mathcal M$ is the mass of a fluid element (Ch. 1–6); the enclosed mass is $M(r)$.
  - **Growth rates** $\lambda$, with modes $\propto e^{\lambda t}$, $\lambda = -\ii\omega$ (not $\gamma$ or $\Gamma$).
  - $\mu$ is only the (dimensionless) mean molecular weight: write $\mu m_u$ for a mass. Dynamic viscosity is $\rho\nu$, a diffusion coefficient $D$.
  - $\Gamma$ is only the adiabatic index; circulation is $\mathcal C$.
  - $k$ (or $k_n$) for wavenumbers; $\kappa$ for opacity, curvature (Ch. 24) and the epicyclic frequency (Ch. 26).
  - A prime is an Eulerian perturbation, never a derivative: write $\dd\rho/\dd r$.
  - Surface and column densities $\Sigma$ ($\sigma$ is the Stefan–Boltzmann constant).
  - Gravitational energy $W$ (Ch. 3, 7, 8).
  - $\ln$ for natural logarithms, $\log_{10}$ for decimal ones.
  - Azimuthal angle $\phi$ (`\phi`, not `\varphi`) in both cylindrical and spherical coordinates. (Ch. 8 keeps $\varphi = \dd\theta/\dd\xi$ in the Lane–Emden system.)
  - Exponential: upright, `\ee^{...}`.
- **Further reading lists and footnotes**: a bullet or a footnote must not be just `@key.`, which Pandoc reads as an example-list marker (renders as "1.", and turns later `@key` citations into numbers). Write `- @key`, or add text (`See @key.`). `just lint` checks this.
- **Plasma** (Ch. 21): free-electron density $n$ or $n_e$; plasma frequency $\omega_p$ (angular; $f_p = \omega_p/2\pi$); dielectric constant $\epsilon$ (with a warning, not $\varepsilon$); charge imbalance $\delta$; Larmor radius $r_L$; Poynting vector $\vb S$.
- **Waves**: plane waves and normal modes go as $e^{\ii(\vb k\cdot\vb x - \omega t)}$, i.e. $e^{-\ii\omega t}$; the real part is understood. Work done by an external force: $W_{\mathrm{ext}}$.
- **Units** (decided 2026-11-12): SI everywhere, with $\epsilon_0$ and $\mu_0$ in electromagnetism (no Gaussian forms; Ch. 21 has a callout on translating them). Customary units kept: $n$ in cm⁻³, $\rho$ in g cm⁻³, $\Sigma$ in g cm⁻², $\kappa$ in cm² g⁻¹, erg for large energies and luminosities, pc, AU, $M_\odot$, $R_\odot$, $L_\odot$, yr, eV, keV, km/s; convert them to SI before inserting them in a formula, and show it briefly. They are introduced in Ch. 1 (after @eq-continua-4), N and Pa in Ch. 2, erg in Ch. 3, gauss in Ch. 21 (after @eq-plasma-7; never write the gauss in g, cm, s). Field strengths in tesla with gauss in parentheses, e.g. $0.3\,\mathrm{nT}$ ($3\,\mu\mathrm{G}$). Diffusivities and viscosities in m²/s. Details in `review/si-conversion.md`.
- **Upright subscripts and units**: write `\mathrm{...}`, never `\rm` (the Typst/PDF converter cannot handle `\rm`) or `\operatorname` (`just lint` reports both).
- **Subscripts in matplotlib figures**: no mathtext; write `ω_ac` in the label and convert `_xyz` to an SVG `<tspan baseline-shift="sub">` after saving (see `figures-src/stratified-atmospheres/diagnostic-diagram.py`).
- **Numbers**: $5.2 \times 10^{43}$ (not $\cdot$). Object names in IAU style: SN 1987A, SN 1999em.

## Math

- Inline `$...$`. Display:

  ```markdown
  $$
  \partial_t \rho + \nabla\cdot(\rho \vb{v}) = 0
  $$ {#eq-continua-continuity}
  ```

- **Every display equation gets a label** (`#eq-<key>-<name>`) so that it is numbered. Use descriptive names. Sequential names like `eq-sound-12` are acceptable for equations no one references yet; after inserting or moving equations, run `just renumber chapters/<slug>.qmd` so that the numbers match positions again (it also re-keys labels moved from another chapter and updates references book-wide).
- Multi-line derivations use `\begin{aligned}...\end{aligned}` inside `$$`, with one label for the whole block.
- **Long equations.** MathJax breaks long single-line equations automatically, but it does not break rows of a derivation well. Keep every row under roughly 450 px, so that it fits the text column on a laptop (about 530 px there). If the left-hand side is long, put it on its own row and indent the following rows (`& \quad = ...`, continuation rows `& \qquad\qquad + ...`). Inside `\left( ... \right)` you cannot break a row; use `\biggl( ... \biggr)` instead.
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

- The `.solution` class is what `tools/check-no-solutions.sh` looks for. Always use it. Quarto prints the "Solution." label itself.
- Footnotes used inside a solution must be defined inside the same solution block (`just lint` checks this); otherwise their text is published with the page's footnotes.
- Footnote names include the chapter key (`[^hydro-1]`), because the PDF combines all chapters into one document.
- Exercises adapted from textbooks are rewritten in our own words and credited, e.g. "Adapted from @clarke2007, Problem 8." Never copy textbook wording.
- Assumptions use `::: {#cnj-<key>-<name>}` with a `## Title` (rendered as "Assumption N.k").

## Figures

```markdown
![Caption sentence.](../figures/<slug>/name.svg){#fig-<key>-name fig-alt="What the figure shows and why it matters."}
```

- Every figure has a caption and `fig-alt`. The alt text describes the content; it is never LaTeX source. Decorative images use `fig-alt=""`.
- Refer to figures as `@fig-...`, never "the figure above".
- Editable sources (Inkscape SVG, Python scripts) go in `figures-src/<slug>/`.
- **Size:** draw figures so that their labels display at the size of the body text (about 19 px). For an SVG, set `width`/`height` equal to the `viewBox` size and use `font-size` around 19–20. Hand-written SVGs should have a `<title>`, a `<desc>`, real `<text>` labels, and a white background (see `figures/mri/`).
- Never rely on colour alone: also use line styles or labels. Graphical elements need at least 3:1 contrast.
- Images from other sources need a compatible license and a credit line in the caption.

## Citations

`[@key]`, with entries in `references.bib`. Include a DOI or ADS bibcode when there is one.
