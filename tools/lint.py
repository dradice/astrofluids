#!/usr/bin/env python3
"""Check the book's sources for the conventions in STYLE.md.

Errors (exit status 1):
  * a display equation outside a solution has no {#eq-...} label
  * an equation inside a solution has a label (would shift numbering)
  * duplicate labels anywhere in the book
  * references to labels that do not exist
  * a figure/image without fig-alt
  * a solutions-profile block without a .solution div inside
Warnings:
  * fig-alt still contains "TODO"
  * a label that does not start with the chapter's key (tools/chapters.py)

Usage: python3 tools/lint.py [files...]   (default: the whole book)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import chapters  # noqa: E402

KEYS = {slug: key for _, cs in chapters.PARTS for slug, key, *_ in cs}
KEYS.update({slug: key for slug, key, *_ in chapters.APPENDICES})

LABEL = re.compile(r"\{#((?:eq|fig|exr|cnj|sec|tbl)-[A-Za-z0-9_-]+)")
REF = re.compile(r"(?<![\w@])-?@((?:eq|fig|exr|cnj|sec|tbl)-[A-Za-z0-9_-]*[A-Za-z0-9])")
SOL_OPEN = re.compile(r'^(:{3,})\s*\{\.content-visible\s+when-profile="solutions"\}\s*$')


def strip_code(text):
    """Blank out fenced code blocks (keep line count)."""
    return re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), text)


def solution_mask(lines):
    """True for lines inside a solutions-profile block."""
    mask, depth_fence = [False] * len(lines), None
    for i, line in enumerate(lines):
        if depth_fence is None:
            m = SOL_OPEN.match(line.strip())
            if m:
                depth_fence = 1
                mask[i] = True
                continue
        else:
            mask[i] = True
            s = line.strip()
            if re.match(r"^:{3,}\s*\{", s) or re.match(r"^:{3,}\s*\w", s):
                depth_fence += 1
            elif re.match(r"^:{3,}\s*$", s):
                depth_fence -= 1
                if depth_fence == 0:
                    depth_fence = None
    return mask


def lint(files):
    errors, warnings = [], []
    labels = {}
    refs = []
    for f in files:
        rel = f.relative_to(ROOT) if f.is_relative_to(ROOT) else f
        text = strip_code(f.read_text(encoding="utf-8"))
        lines = text.split("\n")
        in_sol = solution_mask(lines)
        key = KEYS.get(f.stem)

        # solutions blocks must contain a .solution div
        for i, line in enumerate(lines):
            if SOL_OPEN.match(line.strip()):
                nxt = next((l for l in lines[i + 1:] if l.strip()), "")
                if ".solution" not in nxt:
                    errors.append(f"{rel}:{i+1}: solutions block without '::: {{.solution}}'")

        # display equations
        for m in re.finditer(r"\$\$(.*?)\$\$([^\n]*)", text, re.S):
            line_no = text.count("\n", 0, m.start()) + 1
            after = m.group(2)
            sol = in_sol[line_no - 1]
            has_label = re.match(r"\s*\{#eq-", after)
            if sol and has_label:
                errors.append(f"{rel}:{line_no}: labelled equation inside a solution")
            if not sol and not has_label:
                errors.append(f"{rel}:{line_no}: display equation without {{#eq-...}} label")

        # footnotes used in solutions must be defined inside the solution
        # (otherwise their text is published with the end-of-page notes)
        note_def = {}
        for i, line in enumerate(lines):
            d = re.match(r"^\s*\[\^([^\]]+)\]:", line)
            if d:
                note_def[d.group(1)] = in_sol[i]
        for i, line in enumerate(lines):
            if in_sol[i]:
                for fid in re.findall(r"\[\^([^\]]+)\](?!:)", line):
                    if note_def.get(fid) is False:
                        errors.append(f"{rel}:{i+1}: footnote [^{fid}] used in a solution "
                                      "but defined outside it (would leak)")

        # labels and references
        for i, line in enumerate(lines):
            for lab in LABEL.findall(line):
                if lab in labels:
                    errors.append(f"{rel}:{i+1}: duplicate label {lab} "
                                  f"(also {labels[lab]})")
                labels[lab] = f"{rel}:{i+1}"
                if key and not lab.startswith(("sec-", )) and \
                        not re.match(rf"^[a-z]+-{re.escape(key)}(-|$)", lab):
                    warnings.append(f"{rel}:{i+1}: label {lab} does not use key '{key}'")
            for r in REF.findall(line):
                refs.append((r, f"{rel}:{i+1}"))

        # figures
        for m in re.finditer(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", text):
            line_no = text.count("\n", 0, m.start()) + 1
            attrs = m.group(1) or ""
            if "fig-alt=" not in attrs:
                errors.append(f"{rel}:{line_no}: image without fig-alt")
            elif "TODO" in attrs:
                warnings.append(f"{rel}:{line_no}: fig-alt still TODO")

    for r, where in refs:
        if r not in labels:
            errors.append(f"{where}: reference to unknown label {r}")
    return errors, warnings


def main():
    if len(sys.argv) > 1:
        files = [Path(a).resolve() for a in sys.argv[1:]]
    else:
        files = sorted(ROOT.glob("*.qmd")) + sorted((ROOT / "chapters").glob("*.qmd")) \
            + sorted((ROOT / "appendices").glob("*.qmd"))
    errors, warnings = lint(files)
    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("error: " + e)
    print(f"lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
