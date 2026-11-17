# ODSV – Hinweise für Claude Code

Dieses Repository ist das ODSV-Design-System (Websites, Dashboards, Präsentationen). ODSV steht für OneDay Super Visuals.

@AGENTS.md

## Arbeitsweise in diesem Repo

**Quellen (hier ändern):**

| Was | Datei |
|---|---|
| Werte | `tokens/tokens.json` (mit `$description`) |
| Komponenten-Stil | `web/odsv.css` (nur `var(--odsv-…)`) |
| Verhalten | `web/odsv.js`, Diagramme `web/odsv-charts.js` |
| Komponenten-Beschreibung | `catalog/src/components.meta.py` |
| Diagrammformen für Agents | `catalog/src/charts.meta.py` |
| Beispiele (werden zu `examples[]` im Katalog) | `<template class="docs-src">` in `web/index.html`; Demodaten der Diagramme in `web/docs.js` (`renderCharts`) |
| JS-API-Doku | `catalog/js-api.md` – **von Hand gepflegt**, die einzige nicht erzeugte Datei in `catalog/` (außer `catalog/src/`) |
| Signets | `tools/build_signets.py` |
| Folien | `pptx/odsv_pptx.py`, `tokens/pptx.json` |
| Website | `tools/build_site.py`, `tools/site/site.css`, `tools/site/site.js` |

**Erzeugt (nie von Hand ändern):** `catalog/*.json`, `catalog/COMPONENTS.md`, `web/tokens.css`, `tokens/tokens.css`, `web/signets/*.svg`, `pptx/signets/*.png`, `site/` (nicht eingecheckt).

**Nach jeder Änderung:** `bash tools/validate.sh` (mit `--full` zusätzlich Playwright-Audit mit Screenshots). Der Lauf erzeugt Tokens, Signets, Sprite, Katalog und Website und prüft Tokens, CSS, Doku und HTML. Er scheitert, wenn eine CSS-Wurzel, eine `ODSVCharts`-Funktion oder eine Lint-Regel undokumentiert ist.

**Einmalig einrichten:** `pip install python-pptx lxml beautifulsoup4` und `npm i playwright`; für Folien-Renderings LibreOffice (`soffice`) und `pdftoppm` (Poppler).
- Auf macOS ohne mitgelieferte Browser: `CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` setzen; `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm i playwright` reicht dann.
- Soll im Repo kein `package.json` entstehen: Playwright in einen Ordner außerhalb installieren und `NODE_PATH=<ordner>/node_modules` setzen. Python-Pakete gehen ebenso in eine venv außerhalb des Repos.
- `validate.sh` rendert die Folien-PNGs der Signets neu. Unterscheiden sie sich nur bytegenau (anderer Rechner, andere Chrome-Version), mit `git checkout -- pptx/signets/` zurücksetzen.

**Sprache der Inhalte:** Deutsch. Außer in `web/examples/` keine produktspezifischen Begriffe, nur fachlich neutrale. Beispielzahlen als „Quelle: Beispieldaten“ kennzeichnen.

**Version:** Bei neuer Komponente, neuem Token oder Layout MINOR anheben (SPEC 14): `tokens.json → $extensions.odsv.version`, `pptx.json → version`, Kopfzeilen in `README.md`, `AGENTS.md`, `SPEC.md`, `llms.txt`, `web/odsv.js` (`ODSV.version`), `web/index.html`; Eintrag in SPEC 14.

**Veröffentlichen:** Push auf `main` baut die Website über `.github/workflows/pages.yml` neu.
