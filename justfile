# Common tasks for the ASTRO 442 notes. Run `just` to list them.

set shell := ["bash", "-euo", "pipefail", "-c"]

# Old TeXmacs material (outside this repo).
old := "../2025"

# List available recipes
default:
    @just --list --unsorted

# One-time setup after cloning: enable the pre-commit hook
setup:
    git config core.hooksPath tools/hooks
    @echo "pre-commit hook enabled"

# Live preview with auto-reload (optionally one file: just preview chapters/mri.qmd)
preview file="":
    quarto preview {{file}}

# Build the public site and PDF into _book/, then check that no solutions leaked
build:
    quarto render
    bash tools/check-no-solutions.sh _book

# Build only the HTML site (faster)
html:
    quarto render --to html

# Build only the PDF print version (Typst)
pdf:
    quarto render --to typst

# Instructor build with solutions into _book-solutions/ (never published)
solutions:
    quarto render --profile solutions

# Serve an already-built site at http://localhost:8000 (default: _book)
serve dir="_book":
    python3 -m http.server 8000 --bind 127.0.0.1 --directory {{dir}}

# Export a TeXmacs file to LaTeX via the host's TeXmacs (e.g. just tm2tex notes/15-mri)
tm2tex name outdir="/tmp/tm2tex":
    mkdir -p {{outdir}}
    cp "{{old}}/{{name}}.tm" "{{outdir}}/"
    distrobox-host-exec env QT_QPA_PLATFORM=offscreen texmacs \
        -c "$(realpath {{outdir}})/$(basename {{name}}).tm" \
           "$(realpath {{outdir}})/$(basename {{name}}).tex" -q
    @echo "-> {{outdir}}/$(basename {{name}}).tex (drawings exported as PDFs next to it)"

# Create stubs for chapters listed in tools/chapters.py that don't exist yet
stubs:
    python3 tools/chapters.py stubs

# Print the chapter list for _quarto.yml (paste it into the book: section)
chapters:
    python3 tools/chapters.py yaml

# Commit everything and push; GitHub Actions then rebuilds and deploys the site
publish message:
    git add -A
    git commit -m "{{message}}"
    git push

# Show the status of the latest deploys
deploys:
    gh run list --workflow Publish --limit 5

# Remove build outputs and Quarto caches
clean:
    rm -rf _book _book-solutions .quarto
