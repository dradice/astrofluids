#!/usr/bin/env bash
# Fail if solution content made it into a public build.
#
# Solutions are written as
#   ::: {.content-visible when-profile="solutions"}
#   ::: {.solution}
#   ...
#   :::
#   :::
# The public build must contain no element with class "solution".
# Usage: tools/check-no-solutions.sh [_book]
set -euo pipefail
dir="${1:-_book}"
if [ ! -d "$dir" ]; then
  echo "check-no-solutions: directory '$dir' not found" >&2
  exit 2
fi
if grep -rlE 'class="[^"]*\bsolution\b' --include='*.html' "$dir"; then
  echo "ERROR: solution content found in the public build (files above)." >&2
  exit 1
fi
echo "check-no-solutions: OK (no solution content in $dir)"
