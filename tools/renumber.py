#!/usr/bin/env python3
"""Tidy equation labels in one or more chapters, updating references book-wide.

  python3 tools/renumber.py chapters/sound-waves.qmd [more files]

For each file (whose key comes from tools/chapters.py):
  * labels that belong to another chapter's key (e.g. after moving a section
    from chapter "sound" to chapter "strat") are re-keyed:
        eq-sound-oscillation-book -> eq-strat-oscillation-book
    (also fig-, exr-, cnj- labels);
  * sequential labels eq-<key>-<n> are renumbered so that n is again the
    position of the equation among the chapter's numbered equations.
Every reference (@label) and label definition in the whole book is updated.
Run `just lint` afterwards.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import chapters  # noqa: E402
from lint import solution_mask, strip_code  # noqa: E402

KEYS = {slug: key for _, cs in chapters.PARTS for slug, key, *_ in cs}
KEYS.update({slug: key for slug, key, *_ in chapters.APPENDICES})
ALL_KEYS = sorted(set(KEYS.values()), key=len, reverse=True)


def book_files():
    return sorted(ROOT.glob("*.qmd")) + sorted((ROOT / "chapters").glob("*.qmd")) \
        + sorted((ROOT / "appendices").glob("*.qmd"))


def plan(path):
    key = KEYS[path.stem]
    text = path.read_text(encoding="utf-8")
    code_free = strip_code(text)
    lines = code_free.split("\n")
    in_sol = solution_mask(lines)
    mapping = {}

    # 1. re-key labels from other chapters
    for lab in re.findall(r"\{#((?:eq|fig|exr|cnj|tbl)-[A-Za-z0-9_-]+)", code_free):
        kind, rest = lab.split("-", 1)
        if rest.startswith(key + "-"):
            continue
        for other in ALL_KEYS:
            if rest.startswith(other + "-"):
                mapping[lab] = f"{kind}-{key}-{rest[len(other) + 1:]}"
                break

    # 2. renumber sequential equation labels by position
    n = 0
    for m in re.finditer(r"\$\$(?:(?!\$\$).)*?\$\$[ \t]*\{#(eq-[A-Za-z0-9_-]+)\}", code_free, re.S):
        line_no = code_free.count("\n", 0, m.start())
        if in_sol[line_no]:
            continue
        n += 1
        lab = mapping.get(m.group(1), m.group(1))
        if re.fullmatch(rf"eq-{re.escape(key)}-\d+", lab):
            mapping[m.group(1)] = f"eq-{key}-{n}"
    return {a: b for a, b in mapping.items() if a != b}


def apply(mapping):
    if not mapping:
        return 0
    pat = re.compile(r"(?<=[#@])(" + "|".join(map(re.escape, sorted(mapping, key=len, reverse=True)))
                     + r")(?![A-Za-z0-9_-])")
    changed = 0
    for f in book_files():
        text = f.read_text(encoding="utf-8")
        new = pat.sub(lambda m: mapping[m.group(1)], text)
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def main():
    files = [Path(a).resolve() for a in sys.argv[1:]]
    if not files:
        sys.exit(__doc__)
    mapping = {}
    for f in files:
        mapping.update(plan(f))
    for a, b in mapping.items():
        print(f"{a} -> {b}")
    print(f"renumber: {len(mapping)} label(s) changed in {apply(mapping)} file(s)")


if __name__ == "__main__":
    main()
