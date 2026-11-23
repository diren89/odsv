# ODSV – Design-System v1.2.0

Dunkel, gesperrte Versalien, ein gelber Akzent. Für Websites, Dashboards und Präsentationen.

**AI-Agents beginnen mit [`AGENTS.md`](AGENTS.md)**, Menschen mit der Referenzseite `web/index.html` und [`SPEC.md`](SPEC.md).

| Ordner/Datei | Inhalt |
|---|---|
| `AGENTS.md`, `llms.txt` | Einstieg für AI-Agents: Entscheidungsbaum, Muss-Regeln, Ablauf, Inhaltsgrenzen, Definition of Done |
| `SPEC.md` | Vollständige Spezifikation (Prinzipien, Farbe, Typo, Raster, Komponenten, Dashboards, Diagramme, Folien, Bewegung, Barrierefreiheit, Agenten-Schnittstelle) |
| `GAPS.md` | Lückenanalysen und Prüfberichte |
| `tokens/` | `tokens.json` (Quelle, DTCG, alle Tokens beschrieben), `tokens.css`, `pptx.json` |
| `catalog/` | erzeugt: Komponenten (`components.json`, `COMPONENTS.md`), Diagrammformen (`charts.json`), Klassen, Icons, Tokens flach, Folienlayouts; von Hand: `js-api.md`; Quellen in `catalog/src/` |
| `web/` | `odsv.css`, `odsv.js`, `odsv-charts.js`, `icons.svg` (Icons + 18 Signets), `signets/` (SVG-Dateien), Referenzseite, Beispiele |
| `templates/` | Startvorlagen: `website.html`, `dashboard.html`, `deck_example.py` |
| `pptx/` | `ODSV-Vorlage.potx` (16 Layouts), Beispielpräsentation, `odsv_pptx.py` (Helfer), `signets/` (Folienbilder) |
| `tools/` | Erzeuger und Prüfungen, `validate.sh` führt alles aus |
| `tools/build_site.py`, `tools/site/` | Website im Stil eines Komponenten-Explorers (Storys mit Theme, Breite und Code, Tokens, Icons, Signets, Richtlinien); erzeugt `site/` |

Änderungen immer in den Quellen (Liste in [`CLAUDE.md`](CLAUDE.md): u. a. `tokens/tokens.json`, `web/odsv.css`, `web/odsv-charts.js`, `catalog/src/*.meta.py`), danach `bash tools/validate.sh`.

## Website

`python3 tools/build_site.py` erzeugt `site/`: reines HTML, CSS und JS, läuft direkt per Doppelklick auf `site/index.html` oder auf jedem statischen Host. Zum lokalen Ansehen über HTTP: `python3 -m http.server -d site`.
Veröffentlichen über GitHub Pages: `.github/workflows/pages.yml` baut und veröffentlicht bei jedem Push auf `main` (einmalig unter Settings → Pages die Quelle „GitHub Actions“ wählen). `site/` wird nicht eingecheckt.
