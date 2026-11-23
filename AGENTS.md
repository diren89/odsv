# ODSV – Anleitung für AI-Agents

ODSV 1.2.0 ist ein dunkles, markenneutrales Design-System für **Websites, Dashboards und Präsentationen**. Es setzt auf gesperrte Versalien-Headlines, genau einen gelben Akzent, dunkle Karten mit großen Radien und Line-Art. Diese Datei ist der Einstieg: Sie sagt, was du liest, was du baust und wie du prüfst. Menschen lesen `SPEC.md`.

## 0. Voraussetzungen

- Web: nur ein Browser. Zum Prüfen Node 18+ mit Playwright (`npm i playwright`, Chrome oder Chromium; Pfad über `CHROME_PATH`).
- Folien: Python 3.10+ mit `python-pptx` und `lxml`. Für `render_png` LibreOffice (`soffice`) und `pdftoppm`.
- Katalog neu erzeugen: Python mit `beautifulsoup4`. Website erzeugen: nur Python-Standardbibliothek.
- Schnellcheck der Umgebung: `python3 -c "import bs4, pptx"` · `node -e "require('playwright')"` · `echo $CHROME_PATH`. Einrichtung auf macOS und ohne `package.json` im Repo: `CLAUDE.md`.

## 1. Quellen der Wahrheit

| Frage | Datei | Hinweis |
|---|---|---|
| Welcher Wert? | `tokens/tokens.json` (DTCG) | flach mit Beschreibung: `catalog/tokens.flat.json`; im Web nur `var(--odsv-…)` |
| Welche Komponente, welches Markup? | `catalog/components.json` | lesbar: `catalog/COMPONENTS.md`; live: `web/index.html` |
| Welche Klassen gibt es? | `catalog/classes.json` | andere `.odsv-*`-Klassen sind Fehler |
| Welches Signet? | `catalog/signets.json` | Basis + 9 Themen (KI, Netzwerk, Daten, Code, Schwarm, Berge, Fahrrad, Outdoor, Route) + 8 Situationen (Erfolg, Fail, Konflikt, Einigung, Idee, Frage, In Arbeit, Neustart), SPEC 10.6 |
| Welche Icons? | `catalog/icons.json` | `<svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-NAME"/></svg>` |
| Verhalten | `catalog/js-api.md` | `odsv.js` (data-Attribute, globale API, Events) |
| Welche Diagrammform, welche Optionen? | `catalog/charts.json` | je Form: Aufgabe der Daten, wann/nicht, Optionen mit Typ/Pflicht/Standard, Grenzen, Beispielaufruf; Prosa in `catalog/js-api.md`, Regeln SPEC 7.3 und 8 |
| Was meldet die Prüfung? | `tools/lint-html.js` | Regel-IDs und Behebung in Abschnitt 3.1 |
| Folienlayouts, Platzhalter | `catalog/pptx-layouts.json` | Helfer: `pptx/odsv_pptx.py` |
| Warum, Gestaltungsregeln | `SPEC.md` | Kapitel 2 Ton, 3 Farbe, 4 Typo, 6 Komponenten, 8 Diagramme, 9 Folien |

Die Katalogdateien sind **erzeugt** (Ausnahme: `catalog/js-api.md` wird von Hand gepflegt). Ändere sie nie direkt, siehe Abschnitt 9. Gerendert ansehen: Website `python3 tools/build_site.py` → `site/index.html` (live: https://diren89.github.io/odsv/).

## 2. Entscheidungsbaum

```
Was soll entstehen?
├─ Website / Landingpage / Produktseite / Anleitung
│    → templates/website.html kopieren · Komponenten aus catalog/components.json · Prüfung: lint-html
├─ Dashboard / Kennzahlenseite / Bericht mit Zahlen
│    → templates/dashboard.html kopieren · KPI-Reihe oben · Diagramme mit ODSVCharts · jede Zahl mit Quelle
│    └─ Welche Diagrammform? → Aufgabe der Daten in catalog/charts.json (Feld task) suchen:
│         Verlauf → line · Kategorien → hbars · wenige Zeitpunkte → bars/columns · Teile+Summe → columns stacked
│         Verteilung → histogram/boxplot · Zusammenhang → scatter · Abweichung → diverging
│         zwei Dimensionen → heatmap · zwei Zeitpunkte → slope · Ablauf → funnel · viele Reihen → multiples
├─ Präsentation / Folien (.pptx)
│    → pptx/odsv_pptx.py (Deck) · Beispiel templates/deck_example.py · d.check() + render_png ansehen
├─ Dokument (Docs, Word, PDF)
│    → helles Theme (SPEC 3.2): Text #000, Akzent nur als Linie #8A7200 oder Text #6B5800
├─ Einzelne Komponente in bestehendes Projekt
│    → tokens.css + odsv.css einbinden · Markup aus components.json → examples[0].html übernehmen
└─ ODSV selbst ändern (Token, Komponente, Diagrammform, Doku)
     → Abschnitt 9 · danach bash tools/validate.sh
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
7. Diagramme in `<figure class="odsv-chart">`: Titel als **Aussage**, SVG mit `aria-label`, Fuß „Quelle: … · Stand …“ (diagramm). Form nach Aufgabe der Daten (SPEC 7.3), Tabellenansicht über `[data-odsv-chart-table]` anbieten.
8. Tabellen in `.odsv-table-wrap` mit `<caption>` (tabelle). Felder mit `<label>` (formular). Bilder mit `alt` (alt).
9. Warnungen nie im Akkordeon und nie gekürzt (warnung). Status immer mit Icon und Wort, nie nur über Farbe.
10. Kein seitliches Scrollen bei 390 px (ueberlauf). Auf Touch sind alle Ziele mindestens 44 px groß (erledigt `odsv.css`).
11. Icons dekorativ mit `aria-hidden="true"`, allein stehend mit Namen (icon). Höchstens eine gelbe Icon-Kachel je Ansicht (akzent).

### 3.1 Meldung → Behebung

`node tools/lint-html.js seite.html` gibt je Fund `Fehler|Warnung · regel-id · Text` aus. Fehler müssen weg; Warnungen nur mit Begründung stehen lassen.

| Regel | Stufe | Auslöser | Behebung |
|---|---|---|---|
| `einbindung` | Fehler / Warnung | `tokens.css` oder `odsv.css` fehlt; `lang="de"` fehlt | `<link>` auf beide CSS im `<head>`, `<html lang="de" data-theme="dark">` |
| `klasse` | Fehler | Klasse mit `odsv-` nicht in `catalog/classes.json` | Klasse aus dem Katalog nehmen; nie eigene `odsv-*`-Klassen erfinden, eigene Klassen ohne Präfix |
| `token` | Fehler / Warnung | Farbe im `style`-Attribut bzw. Hex/rgb in `<style>` | `var(--odsv-…)` aus `catalog/tokens.flat.json` |
| `primaer` | Fehler | mehr als ein `.odsv-btn--primary` in einer Sektion/einem Dialog | weitere auf `--secondary` oder `--ghost` |
| `name` | Fehler | Button oder Link ohne Text/`aria-label` | sichtbaren Text oder `aria-label` ergänzen |
| `buttontext` | Warnung | „OK“, „Weiter“, „Hier klicken“ u. ä. | Verb + Ziel: „Bericht öffnen“ |
| `versalien` | Warnung | Headline im Quelltext in Großbuchstaben | normal schreiben; das CSS versalisiert |
| `headline` | Warnung | Headline über 24 Zeichen oder 3 Wörter | kürzen; Erklärung in den Zweitsatz |
| `dreiklang` | Warnung | Headline ohne `.odsv-sub` direkt danach | Zweitsatz ergänzen (1 Satz, ≤ 90 Zeichen) |
| `ueberschriften` | Warnung | Ebene übersprungen oder nicht genau ein `<h1>` | Ebenen lückenlos; Klasse ≠ Element (`<h2 class="odsv-h1">` ist erlaubt) |
| `alt` | Fehler | `<img>` ohne `alt` | Inhalt beschreiben; dekorativ `alt=""` |
| `icon` | Warnung | Icon-SVG ohne `aria-hidden` und ohne Namen | dekorativ `aria-hidden="true"`, sonst `role="img"` + `aria-label` |
| `diagramm` | Fehler / Warnung | kein `.odsv-chart__title`, kein `aria-label` am SVG; kein Fuß | Titel als Aussage, `label`-Option setzen, `.odsv-chart__footer` „Quelle: … · Stand …“ |
| `tabelle` | Fehler / Warnung | Tabelle ohne `.odsv-table-wrap`; ohne `<caption>` | in `<div class="odsv-table-wrap" role="region" tabindex="0" aria-label="…">`; `<caption class="odsv-sr-only">` |
| `formular` | Fehler | Feld ohne `<label>` | `<label for>` bzw. `.odsv-field__label` |
| `warnung` | Fehler | Warn-Callout im Akkordeon | Warnung vor den Schritt, voll ausgeschrieben |
| `akzent` | Warnung | mehrere gelbe Icon-Kacheln (`.odsv-tile--accent`) | eine behalten, Rest `.odsv-tile` |
| `ueberlauf` | Fehler | Seite scrollt seitlich (390 px) | breite Inhalte in `.odsv-table-wrap`/`.odsv-scroll-x`, Raster mobil `odsv-col-12` |

## 4. Nicht tun

- Gelb als Fläche hinter Text, als Dekor oder als zweiten Akzent einsetzen. Im hellen Theme nie Gelb auf Weiß.
- Den Signet-Verlauf (Pink → Gelb) außerhalb von Hero oder Titelfolie verwenden, Signet-Varianten mischen oder eigene Signets zeichnen (neue nur über `tools/build_signets.py`).
- Schatten unter Karten setzen; Tiefe entsteht nur über Flächenstufen `surface-1…3`.
- Fremde Marken, Logos, Fotos realer Personen oder Webfonts von CDNs einbinden.
- Zahlen erfinden. Beispieldaten kennzeichnen („Quelle: Beispieldaten“).
- Begriffe aus anderen Projekten übernehmen. Inhalte gehören zum Thema der Aufgabe und sind fachlich korrekt.
- `odsv-*`-Klassen, Tokens, Icons oder Signets erfinden. Fehlt etwas: Abschnitt 11.
- Paletten mischen: Zugehörigkeit `dv-1…7`, Menge `dv-seq-1…6`, Richtung `dv-div-*` – je Diagramm genau eine Palette (plus `dv-context`).
- Diagrammfarben umsortieren. Die Reihenfolge ist fest: `dv-1` Gelb, `dv-2` Blau, `dv-3` Pink, `dv-4` Türkis, `dv-5` Orange, `dv-6` Violett, `dv-7` Grün.

## 5. Arbeitsablauf

**Web (Website, Dashboard)**
1. Vorlage aus `templates/` kopieren (Pfade auf `tokens.css`, `odsv.css`, `odsv.js` anpassen; Sprite: `node tools/build-web.js` oder Inhalt von `web/icons.svg` zwischen `<!--ODSV-SPRITE-->`-Marker kopieren).
2. Je Bedarf die Komponente in `catalog/components.json` suchen (Felder `use`, `avoid`) und `examples[].html` übernehmen.
3. Inhalte nach den Grenzen in Abschnitt 6 schreiben.
4. `node tools/lint-html.js deine-seite.html` ausführen, bis 0 Fehler stehen. Warnungen begründet stehen lassen oder beheben.
5. Sichtprüfung bei 390 und 1440 px in beiden Themes, z. B. mit `node tools/audit.js deine-seite.html` (Screenshots in `web/_audit/`).

**Diagramm (Web)**
1. Form wählen: Aufgabe der Daten in `catalog/charts.json` → `task`; `avoid` und `limits` prüfen (z. B. `line` bis 4 Reihen, `donut` bis 3 Teile).
2. Markup aus `charts.json → markup` (Figure, Tabellen-Button, Legende als Schalter) übernehmen. Die dv-Klasse sitzt an der `.odsv-swatch`, nie am Text.
3. Aufruf aus `charts.json → charts[].example` anpassen. Pflicht ist `label`: die Aussage mit den wichtigsten Zahlen. Titel = Aussage, Zweitsatz = Einheit/Bezug/n, Fuß = Quelle · Stand.
4. `odsv-charts.js` mit `defer` einbinden und nach `DOMContentLoaded` zeichnen; nachgeladene Daten: Aufruf wiederholen (ersetzt die Zeichnung).
5. Prüfen: lint-html (Regel `diagramm`), Tab + Pfeiltasten wandern, Tabellen-Button zeigt die Daten.

```html
<figure class="odsv-chart">
  <div class="odsv-chart__header">
    <div><figcaption class="odsv-chart__title">Berlin führt mit Abstand</figcaption><p class="odsv-chart__subtitle">Bestellungen je Stadt, November</p></div>
    <div class="odsv-chart__tools"><button class="odsv-btn odsv-btn--ghost odsv-btn--sm" type="button" data-odsv-chart-table aria-expanded="false"><span data-odsv-label>Daten als Tabelle</span></button></div>
  </div>
  <div class="odsv-chart__plot" id="staedte"></div>
  <p class="odsv-chart__footer">Quelle: Beispieldaten · Stand 17.11.2026</p>
</figure>
<script>document.addEventListener('DOMContentLoaded', function () {
  ODSVCharts.hbars(document.getElementById('staedte'), { labels: ['Berlin', 'Hamburg', 'München'], values: [1840, 1120, 1065],
    colors: ['odsv-dv-highlight', 'odsv-dv-context', 'odsv-dv-context'], label: 'Berlin hat mit 1.840 die meisten Bestellungen, vor Hamburg mit 1.120.' });
});</script>
```

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
| KPI | Label + Wert + Einheit + Trend (Icon + Wort) + Bezug; höchstens 6 je Seite |
| Diagramm-Mengen | je Form `limits` in `catalog/charts.json` (Reihen, Kategorien, Teile) |

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
| Diagramm-Rahmen, Verlauf, Säulen, Anteile | `chart` + `catalog/charts.json` |
| Verteilung, Zusammenhang, Abweichung, Rang, Trichter, Heatmap, viele Reihen | `analysis` (Form nach SPEC 7.3) + `catalog/charts.json` |
| Text setzen (Headline, Fließtext, Label, Zahl) | `typography` |
| Seitengerüst, Raster, Abstände zwischen Blöcken | `layout` |
| Abschnittsauftakt (Eyebrow → Headline → Zweitsatz) | `hgroup` |
| Bildzeichen in Text, Button, Navigation | `icon` |
| dekoratives Symbol über Karte oder Headline | `tile` |
| Aufzählung, nummerierte Liste, Eckdaten (`<dl>`) | `list-facts` |
| Seitenkopf mit Navigation, Seitenleiste | `navigation` |
| kurze Erklärung beim Zeigen/Fokus | `tooltip` |
| kurze Bestätigung nach einer Handlung | `toast` (blendet die Anwendung aus) |
| Stand, Quellen, Impressum am Seitenende | `footer` |
| nur vorlesen, Abstand oben, ausblenden, Druck | `utilities` |
| Beschriftung auf Bild/3D | `label3d` |
| Markenmoment | `signet` (einmal; Variante nach Kernthema: `#odsv-signet-ai`, `-network`, `-data`, `-code`, `-swarm`, `-mountains`, `-bike`, `-outdoor`, `-route`; im Zweifel Basis) |

## 8. Fertig, wenn

- [ ] `node tools/lint-html.js …` meldet 0 Fehler (Web) bzw. `d.check()` ist leer (Folien).
- [ ] Sichtprüfung erledigt: Web bei 390 und 1440 px dunkel und hell; Folien als PNG, jede einzeln.
- [ ] Nichts überlappt, nichts ist abgeschnitten, Karten einer Zeile sind gleich hoch.
- [ ] Jede Zahl hat Einheit und Quelle; Beispieldaten sind gekennzeichnet.
- [ ] Genau ein Akzent je Ansicht; der Signet-Verlauf höchstens einmal.
- [ ] Jedes Diagramm: Form passt zur Aufgabe (SPEC 7.3), `label` mit Aussage, Tabellen-Button, Tastatur geprüft.
- [ ] Keine erfundenen Klassen, Tokens, Icons; jede Lücke nach Abschnitt 11 vermerkt.

## 9. Das System selbst ändern

Welche Datei Quelle ist und welche erzeugt wird: Tabelle in `CLAUDE.md`.

1. Werte nur in `tokens/tokens.json` ändern (mit `$description`). Komponenten in `web/odsv.css` nur mit `var(--odsv-…)` gestalten. Zweck, Regeln, A11y und Inhaltsgrenzen in `catalog/src/components.meta.py` eintragen (neue CSS-Wurzeln in `roots`). Ein Beispiel als `<template class="docs-src">` in `web/index.html` ergänzen.
2. **Neue Diagrammform:** Funktion in `web/odsv-charts.js` (SVG über `h()`, Tabelle über `setTable()`, Tastatur über `keys()`), Klassen in `web/odsv.css`, Eintrag in `catalog/src/charts.meta.py`, Beispiel in `web/index.html` (Sektion `analyse`, `data-demo-chart="…"`) mit Demodaten in `web/docs.js → renderCharts`, Zeile in SPEC 7.3, Abschnitt in `catalog/js-api.md`.
3. `bash tools/validate.sh` ausführen. Das erzeugt `tokens.css`, Signets, Sprite, Katalog (inkl. `charts.json`) und Website und prüft Tokens, CSS, Doku (`tools/check_docs.py`) und HTML. Mit `--full` läuft zusätzlich der Playwright-Audit. Die Prüfung scheitert bei einer CSS-Wurzel ohne Katalogeintrag, einer `ODSVCharts`-Funktion ohne `charts.meta.py`-Eintrag oder Doku, die nicht mehr zum Code passt.
4. PowerPoint-Vorlage: `bash pptx/_build/build_all.sh`.
5. Version (SemVer) anheben, Dateien siehe `CLAUDE.md`; Änderung in `SPEC.md` Kapitel 14 eintragen.
6. Veröffentlichen: Push auf `main`; der Workflow baut die Website neu.

## 10. Bekannte Grenzen

- Die PowerPoint-Vorlage gibt es nur dunkel. Die Fortschrittsleiste auf Folien hat fest 7 Segmente. Getestet ist die Vorlage mit LibreOffice, nicht mit PowerPoint selbst.
- Das helle Theme ist rechnerisch und per Screenshot geprüft, aber nicht in einem echten Projekt abgenommen.
- Kleine Vielfache (`multiples`) haben keine Pfeiltasten-Navigation; ihre Werte stehen in der Tabellenansicht. Diagramme zeichnen nur im Browser (`odsv-charts.js`); für Folien gilt `d.chart` im PowerPoint-Helfer.
- Toasts blendet die Anwendung selbst aus; `odsv.js` übernimmt das nicht.
- Von der Icon-Pflichtliste fehlen Pfeil links/oben/unten, Vollbild und Drehen (SPEC 10.4).

## 11. Wenn etwas fehlt

| Fehlt | So vorgehen |
|---|---|
| Komponente | aus vorhandenen bauen (Karte + Layout-Primitive + Typografie); eigene Klassen **ohne** `odsv-`-Präfix, Werte nur über `var(--odsv-…)`; im Ergebnis benennen, was fehlte |
| Icon | `arrow`/`chevron` drehen oder aus Lucide mit gleichen Maßen (24er-Raster, 2 px, runde Enden) übernehmen; vermerken |
| Token/Farbe | nächstliegende Rolle aus `catalog/tokens.flat.json`; nie neue Hex-Werte |
| Diagrammform | die Aufgabe in SPEC 7.3 suchen; passt keine Form, Tabelle zeigen statt etwas zu erfinden |
| Folienlayout | nächstliegendes aus `catalog/pptx-layouts.json`; Platzhalter nie leer lassen (`d.drop`) |
| Daten | nicht erfinden; Beispieldaten nur gekennzeichnet („Quelle: Beispieldaten“) |
