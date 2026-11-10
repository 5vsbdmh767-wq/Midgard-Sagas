#!/bin/sh
# Run from the repo root: sh .wiki-tools/check.sh
# Every check must pass before a commit.
cd "$(dirname "$0")/.." || exit 1
echo "== Watermark scan (must be 0) =="
n=$(grep -rli -a --exclude-dir=.git --exclude-dir=.wiki-tools "aldo""nado" . | wc -l); echo "$n"
echo "== Missing links =="; python3 -I .wiki-tools/links.py . | head -5
echo "== Bad anchors (must be 0) =="; python3 -I .wiki-tools/anchors.py . | head -5
echo "== Unescaped pipes in table links =="
grep -rn --include=*.md --exclude-dir=.git --exclude-dir=.claude '^|' . | grep -P '\[\[[^\]\\]*(?<!\\)\|[^\]]*\]\]' | head
[ "$n" = 0 ] || { echo "WATERMARK FOUND: do not commit"; exit 1; }
