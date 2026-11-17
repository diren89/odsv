# ODSV – Anleitung für AI-Agents

ODSV 1.0.0 ist ein dunkles, markenneutrales Design-System für **Websites, Dashboards und Präsentationen**. Es setzt auf gesperrte Versalien-Headlines, genau einen gelben Akzent, dunkle Karten mit großen Radien und Line-Art. Diese Datei ist der Einstieg: Sie sagt, was du liest, was du baust und wie du prüfst. Menschen lesen `SPEC.md`.

## 0. Voraussetzungen

- Web: nur ein Browser. Zum Prüfen Node 18+ mit Playwright (`npm i playwright`, Chrome oder Chromium; Pfad über `CHROME_PATH`).
- Folien: Python 3.10+ mit `python-pptx` und `lxml`. Für `render_png` LibreOffice (`soffice`) und `pdftoppm`.
- Katalog neu erzeugen: Python mit `beautifulsoup4`.

## 1. Quellen der Wahrheit

| Frage | Datei | Hinweis |
|---|---|---|
| Welcher Wert? | `tokens/tokens.json` (DTCG) | flach mit Beschreibung: `catalog/tokens.flat.json`; im Web nur `var(--odsv-…)` |
| Welche Komponente, welches Markup? | `catalog/components.json` | lesbar: `catalog/COMPONENTS.md`; live: `web/index.html` |
| Welche Klassen gibt es? | `catalog/classes.json` | andere `.odsv-*`-Klassen sind Fehler |
| Welches Signet? | `catalog/signets.json` | Basis + 8 Themen (KI, Netzwerk, Daten, Code, Berge, Fahrrad, Outdoor, Route) + 8 Situationen (Erfolg, Fail, Konflikt, Einigung, Idee, Frage, In Arbeit, Neustart), SPEC 10.6 |
| Welche Icons? | `catalog/icons.json` | `<svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-NAME"/></svg>` |
| Verhalten, Diagramme | `catalog/js-api.md` | `odsv.js` (data-Attribute), `odsv-charts.js` |
| Folienlayouts, Platzhalter | `catalog/pptx-layouts.json` | Helfer: `pptx/odsv_pptx.py` |
| Warum, Gestaltungsregeln | `SPEC.md` | Kapitel 2 Ton, 3 Farbe, 4 Typo, 6 Komponenten, 8 Diagramme, 9 Folien |

Die Katalogdateien sind **erzeugt**. Ändere sie nie direkt, siehe Abschnitt 9.

## 2. Entscheidungsbaum

```
Was soll entstehen?
├─ Website / Landingpage / Produktseite / Anleitung
│    → templates/website.html kopieren · Komponenten aus catalog/components.json · Prüfung: lint-html
├─ Dashboard / Kennzahlenseite / Bericht mit Zahlen
│    → templates/dashboard.html kopieren · Diagramme mit ODSVCharts · jede Zahl mit Quelle
├─ Präsentation / Folien (.pptx)
│    → pptx/odsv_pptx.py (Deck) · Beispiel templates/deck_example.py · d.check() + render_png ansehen
├─ Dokument (Docs, Word, PDF)
│    → helles Theme (SPEC 3.2): Text #000, Akzent nur als Linie #8A7200 oder Text #6B5800
└─ Einzelne Komponente in bestehendes Projekt
     → tokens.css + odsv.css einbinden · Markup aus components.json → examples[0].html übernehmen
```

Ist ein Artifact-Typ der Plattform vorgeschrieben (Slides, Dashboard, Docs, Design System), nutze ihn und übertrage nur Farben, Typografie und Regeln von ODSV.

## 3. Muss-Regeln (prüfbar)

In Klammern steht die Regel-ID, die `tools/lint-html.js` meldet.

1. `tokens.css` und `odsv.css` einbinden, `odsv.js` im `<head>` ohne `defer`, `<html lang="de" data-theme="dark">` (einbindung).
2. Nur Klassen aus `catalog/classes.json` (klasse). Keine Farben im `style`-Attribut, nur `var(--odsv-…)` (token).
3. Genau **ein** `.odsv-btn--primary` je Ansicht (Sektion, Dialog) (primaer).
4. Buttons: Verb plus Ziel, nie „OK“, „Weiter“ oder „Hier klicken“ (buttontext). Jedes Bedienelement hat einen Namen (name).
5. Headlines **nicht in Versalien tippen**, das CSS setzt sie (versalien). Höchstens 24 Zeichen und 3 Wörter (headline).
6. Dreiklang: `.odsv-eyebrow` → `.odsv-display` oder `.odsv-h1` → `.odsv-sub` (dreiklang). Genau ein `<h1>`, keine übersprungenen Ebenen (ueberschriften).
7. Diagramme in `<figure class="odsv-chart">`: Titel als **Aussage**, SVG mit `aria-label`, Fuß „Quelle: … · Stand …“ (diagramm).
8. Tabellen in `.odsv-table-wrap` mit `<caption>` (tabelle). Felder mit `<label>` (formular). Bilder mit `alt` (alt).
9. Warnungen nie im Akkordeon und nie gekürzt (warnung). Status immer mit Icon und Wort, nie nur über Farbe.
10. Kein seitliches Scrollen bei 390 px (ueberlauf). Auf Touch sind alle Ziele mindestens 44 px groß (erledigt `odsv.css`).

## 4. Nicht tun

- Gelb als Fläche hinter Text, als Dekor oder als zweiten Akzent einsetzen. Im hellen Theme nie Gelb auf Weiß.
- Den Signet-Verlauf (Pink → Gelb) außerhalb von Hero oder Titelfolie verwenden, Signet-Varianten mischen oder eigene Signets zeichnen (neue nur über `tools/build_signets.py`).
- Schatten unter Karten setzen; Tiefe entsteht nur über Flächenstufen `surface-1…3`.
- Fremde Marken, Logos, Fotos realer Personen oder Webfonts von CDNs einbinden.
- Zahlen erfinden. Beispieldaten kennzeichnen („Quelle: Beispieldaten“).
- Begriffe aus anderen Projekten übernehmen. Inhalte gehören zum Thema der Aufgabe und sind fachlich korrekt.
- Diagrammfarben umsortieren. Die Reihenfolge ist fest: `dv-1` Gelb, `dv-2` Blau, `dv-3` Pink, `dv-4` Türkis, `dv-5` Orange, `dv-6` Violett, `dv-7` Grün.

## 5. Arbeitsablauf

**Web (Website, Dashboard)**
1. Vorlage aus `templates/` kopieren (Pfade auf `tokens.css`, `odsv.css`, `odsv.js` anpassen; Sprite: `node tools/build-web.js` oder Inhalt von `web/icons.svg` zwischen `<!--ODSV-SPRITE-->`-Marker kopieren).
2. Je Bedarf die Komponente in `catalog/components.json` suchen (Felder `use`, `avoid`) und `examples[].html` übernehmen.
3. Inhalte nach den Grenzen in Abschnitt 6 schreiben.
4. `node tools/lint-html.js deine-seite.html` ausführen, bis 0 Fehler stehen. Warnungen begründet stehen lassen oder beheben.
5. Sichtprüfung bei 390 und 1440 px in beiden Themes, z. B. mit `node tools/audit.js deine-seite.html` (Screenshots in `web/_audit/`).

**Präsentation**
```python
import sys; sys.path.insert(0, 'pptx'); from odsv_pptx import Deck
d = Deck()
d.slide('Titel', eyebrow='Bericht · Q3 2026', title='Kennzahlen', sub='Was im dritten Quartal zählt.')
s = d.slide('Diagramm', chapter=1, source='Quelle: …', eyebrow='Umsatz', title='Q4 liegt vorn', sub='je Quartal, in Mio. €',
            ilabel='Kernaussage', itext='Q4 wächst am stärksten.', inote='Eine Säule gelb, Rest grau.')
d.chart(s, 'bar', ['Q1','Q2','Q3','Q4'], {'Umsatz': [1.2,1.4,1.5,2.1]}, highlight=3, alt='Q4 mit 2,1 am höchsten')
assert not d.check(), d.check()
d.save('out.pptx'); d.render_png('vorschau')   # danach jede PNG ansehen
```
- Die Rollen je Layout stehen in `catalog/pptx-layouts.json`. Unbekannte Rollen bricht der Helfer mit Liste ab.
- `chapter` ist der aktive Kapitelindex 0…6; die Leiste hat fest 7 Segmente.
- Diagramme, Tabellen und Bilder nur über `d.chart`, `d.table` und `d.image`.
- Auf einer Folie bleibt kein Platzhalter leer: füllen oder `d.drop(slide, rolle)`.
- Themen-Signet: `d.slide('Titel', signet='ai', wordmark='Produktname', …)`, auf Kapiteltrennern dieselbe Variante als Marke (`signet='ai'`). Situations-Signet auf einer Inhaltsfolie: `d.mark(slide, 'success')`.

## 6. Inhaltsgrenzen

| Element | Grenze |
|---|---|
| Eyebrow | 1–4 Wörter |
| Headline Web | 1–3 Wörter, ≤ 24 Zeichen, ≤ 2 Zeilen |
| Folientitel | ≤ 34 Zeichen je Zeile (28 pt, 0,15 em) |
| Titelfolie / Display | ≤ 12 Zeichen je Zeile, 2 Zeilen |
| Zweitsatz | 1 Satz, ≤ 90 Zeichen |
| Fließtext | Absätze ≤ 4 Sätze, Zeilenlänge ≤ 640 px |
| Button | 1–3 Wörter, Verb + Ziel |
| Badge, Tab, Segment | 1–2 Wörter |
| Folie | 1 Aussage, ≤ 5 Aufzählungspunkte |
| Diagrammtitel | Aussage, ≤ 60 Zeichen; darunter Einheit, Fuß mit Quelle |
| KPI | Label + Wert + Einheit + Trend (Icon + Wort) + Bezug |

Zahlen: deutsches Format (1.284; 2,1), Einheit mit geschütztem Leerzeichen, „ca.“ für Schätzungen.

## 7. Absicht → Komponente

| Absicht | Komponente (`id` in components.json) |
|---|---|
| Haupthandlung auslösen | `button` (primary, einmal) |
| zu anderer Seite / Datei | `link` |
| Inhalte gruppieren | `card` |
| Kennzahl zeigen | `kpi` |
| Ablauf in Schritten | `step` (+ `progress` für Kapitel) |
| Wert aus 2–4 Optionen, Ansicht wechselt | `segmented` |
| gleichrangige Ansichten | `tabs` |
| Status / Sicherheitshinweis | `callout` (Warnung vor dem Schritt) |
| Moment einer Geschichte (Erfolg, Fail, Konflikt …) | `signet` Situation, z. B. `#odsv-signet-success`; höchstens eins je Ansicht, kein Status-Ersatz |
| Status-Etikett | `badge`; Filter: `pill` |
| optionale Zusatzinfo (FAQ) | `accordion` |
| Datensätze vergleichen | `table` |
| Abhaken mit Fortschritt | `checklist` |
| Eingaben | `form` |
| Abschluss-Aufforderung / Rückfrage | `sheet` |
| nichts da / lädt | `empty-loading` |
| Diagramm | `chart` + `catalog/js-api.md` |
| Beschriftung auf Bild/3D | `label3d` |
| Markenmoment | `signet` (einmal; Variante nach Kernthema: `#odsv-signet-ai`, `-network`, `-data`, `-code`, `-mountains`, `-bike`, `-outdoor`, `-route`; im Zweifel Basis) |

## 8. Fertig, wenn

- [ ] `node tools/lint-html.js …` meldet 0 Fehler (Web) bzw. `d.check()` ist leer (Folien).
- [ ] Sichtprüfung erledigt: Web bei 390 und 1440 px dunkel und hell; Folien als PNG, jede einzeln.
- [ ] Nichts überlappt, nichts ist abgeschnitten, Karten einer Zeile sind gleich hoch.
- [ ] Jede Zahl hat Einheit und Quelle; Beispieldaten sind gekennzeichnet.
- [ ] Genau ein Akzent je Ansicht; der Signet-Verlauf höchstens einmal.

## 9. Das System selbst ändern

1. Werte nur in `tokens/tokens.json` ändern (mit `$description`). Komponenten in `web/odsv.css` nur mit `var(--odsv-…)` gestalten. Zweck, Regeln und Grenzen in `catalog/src/components.meta.py` eintragen. Ein Beispiel als `<template class="docs-src">` in `web/index.html` ergänzen.
2. `bash tools/validate.sh` ausführen. Das erzeugt `tokens.css`, Sprite und Katalog und prüft Tokens, CSS und HTML. Mit `--full` läuft zusätzlich der Playwright-Audit. Eine CSS-Wurzel ohne Katalogeintrag lässt die Prüfung scheitern.
3. PowerPoint-Vorlage: `bash pptx/_build/build_all.sh`.
4. Version (SemVer) in `tokens.json` → `$extensions.odsv.version` und `pptx.json` → `version` anheben; Änderung in `SPEC.md` Kapitel 14 eintragen.

## 10. Bekannte Grenzen

- Die PowerPoint-Vorlage gibt es nur dunkel. Die Fortschrittsleiste auf Folien hat fest 7 Segmente. Getestet ist die Vorlage mit LibreOffice, nicht mit PowerPoint selbst.
- Das helle Theme ist rechnerisch und per Screenshot geprüft, aber nicht in einem echten Projekt abgenommen.
- Diagramm-Tooltips gibt es nur für Maus und Touch; eine Tabellenansicht je Diagramm gibt es nicht. Wo nötig, die Daten zusätzlich als Tabelle zeigen.
- Toasts blendet die Anwendung selbst aus; `odsv.js` übernimmt das nicht.
