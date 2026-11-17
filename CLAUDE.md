# ODSV – Hinweise für Claude Code

Dieses Repository ist das ODSV-Design-System (Websites, Dashboards, Präsentationen).

@AGENTS.md

## Arbeitsweise in diesem Repo

- Quellen ändern, nie erzeugte Dateien: `tokens/tokens.json`, `web/odsv.css`, `web/odsv.js`, `catalog/src/*`, `tools/build_signets.py`, `pptx/odsv_pptx.py`.
- Nicht von Hand bearbeiten (wird erzeugt): `catalog/*.json`, `catalog/*.md`, `web/tokens.css`, `tokens/tokens.css`, `web/signets/*.svg`, `pptx/signets/*.png`.
- Nach jeder Änderung: `bash tools/validate.sh` (mit `--full` zusätzlich Playwright-Audit mit Screenshots).
- Einmalig einrichten: `npm i playwright` und `pip install python-pptx lxml beautifulsoup4`; für Folien-Renderings LibreOffice (`soffice`) und `pdftoppm` (Poppler). Chrome-Pfad bei Bedarf über `CHROME_PATH`.
- Sprache der Inhalte: Deutsch. Außer in `web/examples/` keine produktspezifischen Begriffe, nur fachlich neutrale.
