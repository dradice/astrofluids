#!/usr/bin/env python3
"""Convert a 2025 TeXmacs file (notes, worksheet, or homework) to Quarto.

Pipeline: TeXmacs (headless, on the host) -> LaTeX -> clean-up -> pandoc ->
Markdown post-processing. The result is a first draft that still needs a
read-through against the 2025 PDF.

  python3 tools/tm2qmd.py ../2025/notes/15-mri.tm --key mri --slug mri \
      -o chapters/mri.qmd

What it does:
  * every display equation gets a label (numbered); TeXmacs labels are kept
    (eq:mri.condition -> eq-mri-condition), others become eq-<key>-<n>,
    where n counts all numbered displays in the file;
  * equations inside solutions get no label (see STYLE.md);
  * eqnarray -> alignedat (keeps the eqnarray column layout), one label per
    block; \\decorated -> \\boxed; \\mathbf -> \\vb; \\mathd -> \\dd; ...;
  * Eq. \\eqref{x} -> @eq-...;
  * figures: TeXmacs drawings (exported as PDF) are converted to SVG
    placeholders in figures/<slug>/ with fig-alt="TODO";
  * question -> ::: {#exr-...}, homework "Solution." -> solutions-profile div,
    example -> callout, axiom -> Assumption (::: {#cnj-...});
  * "(*)" sections -> "Going further" callouts (not collapsible: Quarto's
    collapsible callouts are not keyboard accessible);
  * worksheet group-member tables and homework boilerplate are dropped.

Options:
  --kind notes|worksheet|homework  (default: guessed from the path)
  --no-title    omit the "# Title {#sec-key}" line (for fragments)
  --tex FILE    use an existing LaTeX export instead of running TeXmacs
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "tm2qmd"

# --------------------------------------------------------------------------
# helpers


def find_group(s, i):
    """Given s[i] == '{', return index just past the matching '}'."""
    assert s[i] == "{", s[i : i + 20]
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError("unbalanced braces near: " + s[i : i + 60])


def replace_macro(s, name, fn, nargs=1):
    r"""Replace \name{a1}...{an} using fn(*args) -> str (balanced braces)."""
    pat = re.compile(r"\\" + name + r"(?![A-Za-z])\s*")
    out, pos = [], 0
    while True:
        m = pat.search(s, pos)
        if not m:
            break
        j = m.end()
        args = []
        ok = True
        for _ in range(nargs):
            while j < len(s) and s[j] in " \t\n":
                j += 1
            if j >= len(s) or s[j] != "{":
                ok = False
                break
            k = find_group(s, j)
            args.append(s[j + 1 : k - 1])
            j = k
        if not ok:
            out.append(s[pos : m.end()])
            pos = m.end()
            continue
        out.append(s[pos : m.start()])
        out.append(fn(*args))
        pos = j
    out.append(s[pos:])
    return "".join(out)


def label_name(raw, key, prefix):
    """eq:mri.condition -> eq-mri-condition (key not duplicated)."""
    name = re.sub(r"^(eq|fig|sec|tab)[:\-.]", "", raw.strip())
    name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    if name == key or name.startswith(key + "-"):
        return f"{prefix}-{name}"
    return f"{prefix}-{key}-{name}"


# --------------------------------------------------------------------------
# LaTeX-level clean-up


SIMPLE_SUBS = [
    (r"\\tmmathbf(?![A-Za-z])", r"\\vb"),
    (r"\\mathbf(?![A-Za-z])", r"\\vb"),
    (r"\\mathd(?![A-Za-z])", r"\\dd"),
    (r"\\mathi(?![A-Za-z])", r"\\ii"),
    (r"\\decorated(?![A-Za-z])", r"\\boxed"),
    (r"\\cdummy(?![A-Za-z])", r"\\cdot"),
    (r"\\backassign(?![A-Za-z])", "=:"),
    (r"\\assign(?![A-Za-z])", ":="),
    (r"\\comma(?![A-Za-z])", ","),
    (r"\\leqslant(?![A-Za-z])", r"\\leq"),
    (r"\\geqslant(?![A-Za-z])", r"\\geq"),
    (r"\\textbar(?![A-Za-z])", "|"),
]


def clean_latex(body):
    for pat, rep in SIMPLE_SUBS:
        body = re.sub(pat, rep, body)
    body = replace_macro(body, "xequal", lambda a: r"\overset{" + a + "}{=}")
    body = replace_macro(body, "tmop", lambda a: r"\operatorname{" + a + "}")
    body = replace_macro(body, "tmem", lambda a: r"\emph{" + a + "}")
    body = replace_macro(body, "tmtextit", lambda a: r"\emph{" + a + "}")
    body = replace_macro(body, "tmstrong", lambda a: r"\textbf{" + a + "}")
    body = replace_macro(body, "tmtextbf", lambda a: r"\textbf{" + a + "}")
    body = replace_macro(body, "tmverbatim", lambda a: r"\texttt{" + a + "}")
    # title block
    body = re.sub(r"\\maketitle", "", body)
    body = replace_macro(body, "author", lambda a: "")
    # lone "\" lines (TeXmacs empty paragraphs)
    body = re.sub(r"(?m)^\s*\\\s*$", "", body)
    body = re.sub(r"\{\\noindent\}", "", body)
    # worksheet group-member table
    body = re.sub(
        r"\\begin\{center\}\s*Group Members\s*\\end\{center\}.*?\\end\{tabularx\}",
        "",
        body,
        flags=re.S,
    )
    # homework boilerplate paragraph
    body = re.sub(
        r"Solutions should be the result of your individual work\..*?(\n\s*\n)",
        r"\1",
        body,
        flags=re.S,
    )
    return body


def extract_title(body):
    m = re.search(r"\\title\{", body)
    if not m:
        return "", body
    k = find_group(body, m.end() - 1)
    raw = body[m.end() : k - 1]
    raw = replace_macro(raw, "tmmisc", lambda a: "")
    title = " ".join(raw.split())
    return title, body[: m.start()] + body[k:]


# --------------------------------------------------------------------------
# equations


EQ_ENV = re.compile(
    r"\\begin\{(equation\*?|eqnarray\*?|align\*?)\}(.*?)\\end\{\1\}|\\\[(.*?)\\\]",
    re.S,
)


def split_rows(body):
    rows = re.split(r"\\\\", body)
    return [r for r in rows if r.strip()]


def split_cells(row):
    cells, depth, cur, i = [], 0, [], 0
    while i < len(row):
        c = row[i]
        if c == "\\":
            cur.append(row[i : i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if c == "&" and depth == 0:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    cells.append("".join(cur))
    return cells


def eqnarray_to_alignedat(body):
    rows = split_rows(body)
    if len(rows) == 1:  # a single row needs no alignment (and MathJax can
        return " ".join(c.strip() for c in split_cells(rows[0]))  # line-break it)
    out = []
    for row in rows:
        cells = [c.strip() for c in split_cells(row)]
        if len(cells) == 3:
            lhs, rel, rhs = cells
            rel = "{}" + rel + "{}" if rel else ""
            out.append(f"{lhs} &{rel} && {rhs}")
        elif len(cells) == 1:
            out.append(cells[0])
        else:
            out.append(" & ".join(cells))
    return "\\begin{alignedat}{2}\n" + " \\\\\n".join(out) + "\n\\end{alignedat}"


def tidy_math(s):
    s = re.sub(r"\\nonumber", "", s)
    s = "\n".join(line.strip() for line in s.strip().splitlines())
    s = re.sub(r"\n{2,}", "\n", s)
    return s


class Equations:
    """Replace display math with \\[ ... \\] QQEQ<n>QQ markers."""

    def __init__(self, key):
        self.key = key
        self.items = []  # (label or None-for-auto, body)

    def __call__(self, m):
        env, body, bracket = m.group(1), m.group(2), m.group(3)
        if bracket is not None:
            body = bracket
            env = "displaymath"
        labels = re.findall(r"\\label\{([^}]*)\}", body)
        body = re.sub(r"\\label\{[^}]*\}", "", body)
        if env.startswith("eqnarray") or env.startswith("align"):
            body = eqnarray_to_alignedat(body)
        body = tidy_math(body)
        n = len(self.items)
        self.items.append((labels[0] if labels else None, body))
        if len(labels) > 1:
            print(f"warning: block with {len(labels)} labels; keeping {labels[0]}",
                  file=sys.stderr)
        return f"\\[ {body} \\] QQEQ{n}QQ"


# --------------------------------------------------------------------------
# figures


class Figures:
    def __init__(self, key, slug, texdir, figdir, tag=""):
        self.key, self.slug, self.texdir, self.figdir = key, slug, texdir, figdir
        self.tag = tag
        self.n = 0
        self.items = []  # (path, label)

    def convert(self, fname):
        src = self.texdir / fname
        self.figdir.mkdir(parents=True, exist_ok=True)
        stem = Path(fname).stem
        if src.suffix.lower() == ".pdf":
            dst = self.figdir / (stem + ".svg")
            subprocess.run(["pdftocairo", "-svg", str(src), str(dst)], check=True)
        elif src.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg"):
            dst = self.figdir / src.name
            shutil.copy(src, dst)
        else:
            print(f"warning: cannot convert figure {fname}", file=sys.stderr)
            dst = self.figdir / src.name
        return f"../figures/{self.slug}/{dst.name}"

    def marker(self, fname, caption):
        self.n += 1
        path = self.convert(fname)
        self.items.append((path, f"fig-{self.key}-{self.tag}{self.n}"))
        i = len(self.items) - 1
        cap = caption.strip()
        return (
            f"\n\nQQFIG{i}BEGINQQ\n\n{cap}\n\nQQFIG{i}ENDQQ\n\n"
            if cap
            else f"\n\nQQIMG{i}QQ\n\n"
        )

    def process(self, body):
        def big(cap_fig, cap_text):
            m = re.search(r"\\includegraphics(\[[^\]]*\])?\{([^}]*)\}", cap_fig)
            if not m:
                return cap_fig + cap_text
            return self.marker(m.group(2), cap_text)

        body = replace_macro(body, "bigfigurestar", big, nargs=2)
        body = replace_macro(body, "bigfigure", big, nargs=2)

        def fig_env(m):
            inner = m.group(1)
            g = re.search(r"\\includegraphics(\[[^\]]*\])?\{([^}]*)\}", inner)
            c = re.search(r"\\caption\{", inner)
            cap = ""
            if c:
                k = find_group(inner, c.end() - 1)
                cap = inner[c.end() : k - 1]
            return self.marker(g.group(2), cap) if g else inner

        body = re.sub(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", fig_env,
                      body, flags=re.S)
        # remaining bare images (e.g. centred in worksheets)
        body = re.sub(
            r"(\\begin\{center\})?\s*(\\raisebox\{[^}]*\}\{)?\\includegraphics(\[[^\]]*\])?\{([^}]*)\}\}?\s*(\\end\{center\})?",
            lambda m: self.marker(m.group(4), ""),
            body,
        )
        return body


# --------------------------------------------------------------------------
# block environments


def mark_blocks(body):
    body = re.sub(r"\\begin\{question\}(\[[^\]]*\])?", "\n\nQQEXRBEGIN\n\n", body)
    body = re.sub(r"\\end\{question\}", "\n\nQQEXREND\n\n", body)
    body = re.sub(r"\\begin\{example\*?\}(\[[^\]]*\])?", "\n\nQQEXMBEGIN\n\n", body)
    body = re.sub(r"\\end\{example\*?\}", "\n\nQQEXMEND\n\n", body)
    body = re.sub(r"\\begin\{axiom\*?\}(\[[^\]]*\])?", "\n\nQQASMBEGIN\n\n", body)
    body = re.sub(r"\\end\{axiom\*?\}", "\n\nQQASMEND\n\n", body)
    body = re.sub(r"\{\\textbf\{Solution\.?\}\}|\\textbf\{Solution\.?\}",
                  "\n\nQQSOL\n\n", body)
    return body


def mark_refs(body, key):
    def ref(m):
        raw = m.group(2)
        prefix = "fig" if raw.startswith("fig") else "sec" if raw.startswith("sec") else "eq"
        return "QQREF" + label_name(raw, key, prefix) + "QQ"

    body = re.sub(r"(Eqs?\.\s*|[Ee]quations?\s+|Figs?\.\s*|[Ff]igure\s+)?\\(?:eq)?ref\{([^}]*)\}",
                  ref, body)
    return body


# --------------------------------------------------------------------------
# Markdown post-processing


def postprocess(md, key, eqs, figs, kind):
    tag = {"worksheet": "ws", "homework": "hw"}.get(kind, "")
    # Pull out footnote definitions (pandoc puts them at the end); they are
    # re-inserted at the end of this function.
    notes = {}

    def grab(m):
        notes[m.group(1)] = " ".join(m.group(2).split())
        return ""

    md = re.sub(r"(?ms)^\[\^([^\]]+)\]:[ \t]*(.*?)(?=^\[\^|^\S|\Z)", grab, md)
    # Solutions: from QQSOL up to the next exercise (or end of document)
    def sol_block(text):
        text = re.sub(r"QQEQ\d+QQ", "", text)  # unnumbered in solutions
        return (
            '::: {.content-visible when-profile="solutions"}\n'
            "::: {.solution}\n" + text.strip() + "\n:::\n:::\n\n"
        )

    md = re.sub(r"QQSOL\s*(.*?)(?=QQEXRBEGIN|\Z)", lambda m: sol_block(m.group(1)),
                md, flags=re.S)

    # Exercises
    exr_count = [0]

    def exr(m):
        exr_count[0] += 1
        text = m.group(1).strip()
        title = ""
        t = re.match(r"\*([^*]+?)\.?\*\s*", text)
        if t:
            title = t.group(1).strip().rstrip(".")
            text = text[t.end():]
        if kind == "worksheet":  # worksheet questions are not numbered exercises
            head = f"**{title}.** " if title else ""
            return head + text + "\n"
        head = f"::: {{#exr-{key}-{exr_count[0]}}}\n"
        if title:
            head += f"## {title}\n\n"
        return head + text + "\n:::\n"

    md = re.sub(r"QQEXRBEGIN\s*(.*?)\s*QQEXREND", exr, md, flags=re.S)

    md = re.sub(r"QQEXMBEGIN\s*(.*?)\s*QQEXMEND",
                lambda m: "::: {.callout-tip icon=false}\n## Example\n\n"
                + m.group(1).strip() + "\n:::\n", md, flags=re.S)
    asm = [0]

    def assumption(m):
        asm[0] += 1
        return f"::: {{#cnj-{key}-{asm[0]}}}\n" + m.group(1).strip() + "\n:::\n"

    md = re.sub(r"QQASMBEGIN\s*(.*?)\s*QQASMEND", assumption, md, flags=re.S)

    # Equations: "$$ body $$ QQEQnQQ" -> labelled display on its own lines
    used = {}
    auto = [0]

    def label_for(n):
        raw, _ = eqs.items[n]
        auto[0] += 1
        lab = label_name(raw, key, "eq") if raw else f"eq-{key}-{tag}{auto[0]}"
        if lab in used:
            lab = f"{lab}-{auto[0]}"
        used[lab] = True
        return lab

    # One left-to-right pass over $$...$$ pairs, so pairs never get mixed up.
    # Each display goes on its own lines (still inside its paragraph); the
    # label, if any, follows the closing $$ on the same line.
    display = re.compile(r"[ \t]*\$\$((?:(?!\$\$).)*?)\$\$(?:[ \t]*QQEQ(\d+)QQ)?[ \t]*\n?",
                         re.S)
    def one_line_inline(t):
        return re.sub(r"(?<![\\$])\$([^$]+?)\$",
                      lambda x: "$" + " ".join(x.group(1).split()) + "$", t)

    out, pos, indent = [], 0, ""
    for m in display.finditer(md):
        text = md[pos:m.start()]
        if indent and text and not text.startswith(("\n", ":::")):
            text = indent + text  # rest of the paragraph after a display
        text = one_line_inline(text)
        out.append(text)
        # indentation of the current line (so displays stay inside list items)
        line = "".join(out).rsplit("\n", 1)[-1]
        lm = re.match(r"(\s*)((?:[-*+]|\d+\.)\s+)?", line)
        indent = " " * len(lm.group(0)) if lm.group(2) else lm.group(1)
        lead = "" if (not text or text.endswith("\n")) else "\n"
        if m.group(2) is not None:
            n = int(m.group(2))
            block = f"$$\n{eqs.items[n][1]}\n$$ {{#{label_for(n)}}}"
        else:
            block = f"$$\n{tidy_math(m.group(1))}\n$$"
        block = "\n".join(indent + l for l in block.split("\n"))
        out.append(f"{lead}{block}\n")
        pos = m.end()
    tail = md[pos:]
    if indent and tail and not tail.startswith(("\n", ":::")):
        tail = indent + tail
    out.append(one_line_inline(tail))
    md = "".join(out)

    # References
    md = re.sub(r"QQREF([a-z]+-[A-Za-z0-9-]+)QQ", r"@\1", md)

    # Figures
    def fig(m):
        path, lab = figs.items[int(m.group(1))]
        cap = " ".join(m.group(2).split())
        return f'![{cap}]({path}){{#{lab} fig-alt="TODO: describe this figure."}}'

    md = re.sub(r"QQFIG(\d+)BEGINQQ\s*(.*?)\s*QQFIG\1ENDQQ", fig, md, flags=re.S)
    md = re.sub(r"QQIMG(\d+)QQ",
                lambda m: f'![]({figs.items[int(m.group(1))][0]})'
                '{fig-alt="TODO: describe this figure."}', md)

    # "(*)" sections -> collapsible callouts
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        h = re.match(r"^(#+)\s+\(\\\*\)\s*(.*?)\s*(\{[^}]*\})?\s*$", lines[i])
        if h:
            level = len(h.group(1))
            j, depth = i + 1, 0
            while j < len(lines):
                # headings inside nested divs (e.g. an Example box) do not
                # end the section
                if re.match(r"^:{3,}\s*\{", lines[j]):
                    depth += 1
                elif re.match(r"^:{3,}\s*$", lines[j]):
                    depth -= 1
                h2 = re.match(r"^(#+)\s", lines[j])
                if h2 and depth == 0 and len(h2.group(1)) <= level:
                    break
                j += 1
            out.append('::: {.callout-note}')
            out.append(f"## Going further: {h.group(2)}")
            out.extend(lines[i + 1 : j])
            out.append(":::")
            out.append("")
            i = j
        else:
            out.append(lines[i])
            i += 1
    md = "\n".join(out)

    # Footnotes: put each definition back inside the solution that uses it
    # (so it is hidden with the solution), the others at the end.
    def keep_notes_inside(m):
        body = m.group(2)
        for fid in dict.fromkeys(re.findall(r"\[\^([^\]]+)\](?!:)", body)):
            if fid in notes:
                body += f"\n\n[^{fid}]: {notes.pop(fid)}"
        return m.group(1) + body + m.group(3)

    md = re.sub(r'(::: \{\.content-visible when-profile="solutions"\}\n::: \{\.solution\}\n)'
                r"(.*?)(\n:::\n:::\n)", keep_notes_inside, md, flags=re.S)
    if notes:
        md = md.rstrip() + "\n\n" + "\n\n".join(f"[^{k}]: {v}" for k, v in notes.items()) + "\n"

    # chapter-unique footnote ids (chapters are combined in the PDF)
    md = re.sub(r"\[\^([^\]]+)\]", lambda m: f"[^{key}-{m.group(1)}]", md)

    # tidy blank lines; no blank line between "$$ {#eq}" and following text
    md = re.sub(r"\n{3,}", "\n\n", md)
    leftovers = sorted(set(re.findall(r"QQ[A-Z]+\w*", md)))
    if leftovers:
        print("warning: unprocessed markers: " + ", ".join(leftovers), file=sys.stderr)
    return md.strip() + "\n"


# --------------------------------------------------------------------------


def export_tex(tm):
    CACHE.mkdir(parents=True, exist_ok=True)
    work = CACHE / tm.stem
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    shutil.copy(tm, work / tm.name)
    tex = work / (tm.stem + ".tex")
    cmd = ["distrobox-host-exec", "env", "QT_QPA_PLATFORM=offscreen", "texmacs",
           "-c", str(work / tm.name), str(tex), "-q"]
    if not shutil.which("distrobox-host-exec"):
        cmd = cmd[1:]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not tex.exists():
        sys.exit(f"TeXmacs export failed for {tm}")
    return tex


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="TeXmacs .tm file")
    ap.add_argument("--key", required=True, help="label key, e.g. mri")
    ap.add_argument("--slug", required=True, help="chapter slug, e.g. mri")
    ap.add_argument("--kind", choices=["notes", "worksheet", "homework"])
    ap.add_argument("--tex", type=Path, help="existing LaTeX export")
    ap.add_argument("--no-title", action="store_true")
    ap.add_argument("-o", "--output", type=Path, help="output .qmd (default: stdout)")
    a = ap.parse_args()

    kind = a.kind or ("homework" if "homework" in str(a.source)
                      else "worksheet" if "worksheet" in str(a.source) else "notes")
    tex = a.tex or export_tex(a.source.resolve())
    full = tex.read_text(encoding="utf-8", errors="replace")
    pre, _, rest = full.partition("\\begin{document}")
    body = rest.split("\\end{document}")[0]
    # keep only \newcommand lines of the preamble, so pandoc expands them
    macros = "\n".join(l for l in pre.splitlines()
                       if l.startswith("\\newcommand") and
                       not re.match(r"\\newcommand\{\\(mathd|mathi|tm\w+)\}", l))

    title, body = extract_title(body)
    body = clean_latex(body)
    figs = Figures(a.key, a.slug, tex.parent, ROOT / "figures" / a.slug,
                   {"worksheet": "ws", "homework": "hw"}.get(kind, ""))
    body = figs.process(body)
    body = mark_blocks(body)
    body = mark_refs(body, a.key)
    eqs = Equations(a.key)
    body = EQ_ENV.sub(eqs, body)

    doc = macros + "\n\\begin{document}\n" + body + "\n\\end{document}\n"
    res = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "markdown-raw_tex-raw_attribute",
         "--wrap=none", "--shift-heading-level-by=1", "--markdown-headings=atx"],
        input=doc, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(res.stderr)
    for line in res.stderr.splitlines():
        print("pandoc: " + line, file=sys.stderr)
    md = postprocess(res.stdout, a.key, eqs, figs, kind)
    if not a.no_title and title:
        md = f"# {title} {{#sec-{a.key}}}\n\n" + md
    if a.output:
        a.output.write_text(md, encoding="utf-8")
        print(f"wrote {a.output}: {len(eqs.items)} display equations, "
              f"{figs.n} figures", file=sys.stderr)
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
