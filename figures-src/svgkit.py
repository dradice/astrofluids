"""Tiny helper for writing the hand-drawn SVG figures of the MHD chapters.

Labels are real <text>, with `_{..}`/`^{..}` (or `_x`) for sub/superscripts.
Figures are drawn at the size at which they are displayed (labels ~19-20 px).
"""
import math
import re
from pathlib import Path

FONT = "'Latin Modern Math', 'STIX Two Math', 'Cambria Math', serif"
BLUE = "#1f4fbf"
GREEN = "#0b6e0b"
RED = "#b3202a"
TEAL = "#007a7a"
GRAY = "#d9d9d9"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w, h, title, desc, ident):
        self.w, self.h, self.title, self.desc, self.ident = w, h, title, desc, ident
        self.body = []
        self.colors = {"#000": "k"}

    def raw(self, s):
        self.body.append(s)

    def _marker(self, color):
        self.colors.setdefault(color, color.strip("#"))
        return f"url(#ah-{self.colors[color]})"

    def text(self, x, y, s, anchor="start", bold=False, italic=True, size=20, fill="#000"):
        parts = re.split(r"(_\{[^}]*\}|\^\{[^}]*\}|_\S|\^\S)", s)
        out, shift = [], 0.0
        for p in parts:
            if not p:
                continue
            if p[0] in "_^":
                body = p[2:-1] if p[1] == "{" else p[1]
                d = 5 if p[0] == "_" else -8
                out.append(f'<tspan dy="{d - shift}" font-size="{size * 0.72:.1f}" '
                           f'font-style="normal">{esc(body)}</tspan>')
                shift = d
            else:
                if shift:
                    out.append(f'<tspan dy="{-shift}">{esc(p)}</tspan>')
                    shift = 0
                else:
                    out.append(esc(p))
        style = "italic" if italic and not bold else "normal"
        weight = "bold" if bold else "normal"
        self.body.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-style="{style}" font-weight="{weight}" fill="{fill}">{"".join(out)}</text>')

    def line(self, x1, y1, x2, y2, color="#000", w=1.6, head=False, tail=False, dash=None):
        a = f' marker-end="{self._marker(color)}"' if head else ""
        a += f' marker-start="{self._marker(color)}"' if tail else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke="{color}" stroke-width="{w}"{d}{a}/>')

    def path(self, d, color="#000", w=1.6, fill="none", head=False, dash=None, extra=""):
        a = f' marker-end="{self._marker(color)}"' if head else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.body.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
                         f'stroke-linejoin="round" stroke-linecap="round"{da}{a} {extra}/>')

    def poly(self, pts, color="#000", w=1.6, head=False, fill="none", closed=False):
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if closed else "")
        self.path(d, color, w, fill, head)

    def circle(self, cx, cy, r, fill="none", stroke="#000", w=1.6):
        self.body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
                         f'stroke="{stroke}" stroke-width="{w}"/>')

    def ellipse(self, cx, cy, rx, ry, rot=0, fill="none", stroke="#000", w=1.6):
        self.body.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                         f'transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})" fill="{fill}" '
                         f'stroke="{stroke}" stroke-width="{w}"/>')

    def rect(self, x, y, w, h, fill="none", stroke="#000", sw=1.6):
        self.body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
                         f'stroke="{stroke}" stroke-width="{sw}"/>')

    def out_of_plane(self, cx, cy, color="#000", r=9):
        """Circled dot: a vector pointing out of the page."""
        self.circle(cx, cy, r, stroke=color)
        self.body.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.35:.1f}" fill="{color}"/>')

    def bracket(self, x1, y1, x2, y2, w=1.5):
        """Dimension bar with end ticks."""
        self.line(x1, y1, x2, y2, w=w)
        if abs(x2 - x1) > abs(y2 - y1):
            for x, y in ((x1, y1), (x2, y2)):
                self.line(x, y - 7, x, y + 7, w=w)
        else:
            for x, y in ((x1, y1), (x2, y2)):
                self.line(x - 7, y, x + 7, y, w=w)

    def save(self, path):
        defs = "".join(
            f'<marker id="ah-{k}" viewBox="0 0 12 12" refX="10.5" refY="6" markerWidth="12" '
            f'markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
            f'<path d="M 1.5 1.5 L 10.5 6 L 1.5 10.5" fill="none" stroke="{c}" '
            f'stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/></marker>'
            for c, k in self.colors.items())
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}" role="img" '
               f'aria-labelledby="{self.ident}-t {self.ident}-d">\n'
               f'<title id="{self.ident}-t">{esc(self.title)}</title>\n'
               f'<desc id="{self.ident}-d">{esc(self.desc)}</desc>\n'
               f'<defs>{defs}</defs>\n<rect width="{self.w}" height="{self.h}" fill="#fff"/>\n'
               f'<g font-family="{FONT}">\n' + "\n".join(self.body) + "\n</g>\n</svg>\n")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(svg)


def bezier(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def offset_edges(pts, wfun):
    """Left and right edges of a ribbon around a polyline, half-width wfun(t)."""
    left, right = [], []
    n = len(pts) - 1
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        w = wfun(i / n)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left, right
