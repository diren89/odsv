# ODSV – Design-System v1.0.0

Dunkel, gesperrte Versalien, ein gelber Akzent. Für Websites, Dashboards und Präsentationen.

**AI-Agents beginnen mit [`AGENTS.md`](AGENTS.md)**, Menschen mit der Referenzseite `web/index.html` und [`SPEC.md`](SPEC.md).

| Ordner/Datei | Inhalt |
|---|---|
| `AGENTS.md`, `llms.txt` | Einstieg für AI-Agents: Entscheidungsbaum, Muss-Regeln, Ablauf, Inhaltsgrenzen, Definition of Done |
| `SPEC.md` | Vollständige Spezifikation (Prinzipien, Farbe, Typo, Raster, Komponenten, Dashboards, Diagramme, Folien, Bewegung, Barrierefreiheit, Agenten-Schnittstelle) |
| `GAPS.md` | Lückenanalysen und Prüfberichte |
| `tokens/` | `tokens.json` (Quelle, DTCG, alle Tokens beschrieben), `tokens.css`, `pptx.json` |
| `catalog/` | erzeugt: Komponenten (`components.json`, `COMPONENTS.md`), Klassen, Icons, Tokens flach, Folienlayouts, JS-API |
| `web/` | `odsv.css`, `odsv.js`, `odsv-charts.js`, `icons.svg` (Icons + 17 Signets), `signets/` (SVG-Dateien), Referenzseite, Beispiele |
| `templates/` | Startvorlagen: `website.html`, `dashboard.html`, `deck_example.py` |
| `pptx/` | `ODSV-Vorlage.potx` (16 Layouts), Beispielpräsentation, `odsv_pptx.py` (Helfer), `signets/` (Folienbilder) |
| `tools/` | Erzeuger und Prüfungen, `validate.sh` führt alles aus |

Änderungen immer in `tokens/tokens.json`, `web/odsv.css` und `catalog/src/components.meta.py`, danach `bash tools/validate.sh`.
