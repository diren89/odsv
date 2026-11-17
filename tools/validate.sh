#!/usr/bin/env bash
# ODSV – alles erzeugen und prüfen. Aufruf: bash tools/validate.sh [--full]   (--full: zusätzlich Playwright-Audit mit Screenshots)
# Optional eigene Seiten mitprüfen: bash tools/validate.sh -- pfad/zu/seite.html …
set -euo pipefail
cd "$(dirname "$0")/.."
FULL=0; EXTRA=()
while [[ $# -gt 0 ]]; do case "$1" in --full) FULL=1;; --) shift; EXTRA=("$@"); break;; esac; shift; done
step(){ printf '\n▶ %s\n' "$1"; }
step "Tokens erzeugen und prüfen";      python3 tools/build_tokens.py >/dev/null && python3 tools/check_tokens.py | tail -2
step "Signets erzeugen und prüfen";      python3 tools/build_signets.py && node tools/check_signets.js && node tools/render_signets.js
step "Web-Build (tokens.css, Sprite)";  node tools/build-web.js >/dev/null && echo ok
step "Katalog erzeugen";                python3 tools/build_catalog.py
step "CSS: nur Tokens";                 node tools/check-css.js | tail -4
step "Website erzeugen";               python3 tools/build_site.py
step "HTML-Regeln (lint)";              node tools/lint-html.js web/index.html web/examples/website.html web/examples/dashboard.html templates/website.html templates/dashboard.html "${EXTRA[@]}"
if [[ $FULL == 1 ]]; then step "Playwright-Audit";  node tools/audit.js | awk -F'|' '{print $1,$2,$3,$4,$5}'; fi
printf '\n✔ ODSV-Prüfung bestanden\n'
