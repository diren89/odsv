# ODSV 1.1.0 – Komponentenkatalog

> Erzeugt von `tools/build_catalog.py` aus `catalog/src/components.meta.py`, `web/odsv.css` und `web/index.html`. Nicht von Hand ändern.
> Maschinenlesbar: `catalog/components.json`. Gültige Klassen: `catalog/classes.json`.

| Komponente | Wurzelklassen | Wofür |
|---|---|---|
| [Typografie](#typography) | `.odsv-eyebrow` `.odsv-display` `.odsv-h1` `.odsv-h2` … | Textstile für jede Ausgabe. |
| [Layout-Primitive](#layout) | `.odsv-container` `.odsv-section` `.odsv-section-head` `.odsv-grid` … | Seitengerüst: . |
| [Icon](#icon) | `.odsv-icon` | Line-Icons aus dem Sprite web/icons. |
| [Button](#button) | `.odsv-btn` `.odsv-icon-btn` | Handlungen auslösen. |
| [Link](#link) | `.odsv-link` `.odsv-textbtn` | Navigation im Text oder leise Nebenaktion („Überspringen“). |
| [Karte](#card) | `.odsv-card` | Gruppiert zusammengehörige Inhalte auf einer Fläche (surface-1, 1-px-Rand, Radius 28). |
| [KPI- und Spec-Kachel](#kpi) | `.odsv-kpi` `.odsv-trend` `.odsv-spec` `.odsv-specs` | Kennzahl mit Label, Einheit, Veränderung und Bezug (. |
| [Schritt-Karte](#step) | `.odsv-step` | Nummerierte Schritte einer Anleitung oder eines Ablaufs. |
| [Fortschrittsleiste](#progress) | `.odsv-progress` | Segmentierte Leiste für Kapitel (Links) oder Zähler (Checkliste, Ziel). |
| [Segment-Umschalter](#segmented) | `.odsv-segmented` | Einen Wert aus 2–4 Optionen wählen, die Ansicht wechselt sofort (Zeitraum, Diagramm/Tabelle). |
| [Checkliste](#checklist) | `.odsv-checklist` `.odsv-check` | Abhaken mehrerer Punkte mit gespeichertem Stand und Fortschritt. |
| [Akkordeon](#accordion) | `.odsv-accordion` | Optionale Zusatzinformation (FAQ). |
| [Tabelle](#table) | `.odsv-table-wrap` `.odsv-table` | Datensätze vergleichen. |
| [Hinweis (Callout)](#callout) | `.odsv-callout` | Status- oder Sicherheitshinweis mit Icon und Wort. |
| [Badge und Pill](#badge) | `.odsv-badge` `.odsv-pill` | Badge: nicht klickbarer Status (1–2 Wörter). |
| [Tabs](#tabs) | `.odsv-tabs` `.odsv-tab` `.odsv-tabpanel` | Gleichrangige Ansichten auf derselben Seite wechseln. |
| [Formularfelder](#form) | `.odsv-field` `.odsv-input` `.odsv-select` `.odsv-textarea` … | Eingaben mit sichtbarem Label, Hinweis und Fehler am Feld. |
| [Tooltip](#tooltip) | `.odsv-tooltip` | Benennt Icon-Buttons oder ergänzt Unwichtiges. |
| [Navigation und Top-Bar](#navigation) | `.odsv-topbar` `.odsv-brand` `.odsv-nav` `.odsv-sidebar` … | Klebende Top-Bar mit Wortmarke, Navigation, Aktionen; Seitenleiste fürs Dashboard ab 1024 px. |
| [Bottom-Sheet](#sheet) | `.odsv-sheet` | Abschluss-Aufforderung (im Fluss) oder modale Rückfrage. |
| [Icon-Kachel](#tile) | `.odsv-tile` | App-Icon-artige Kachel über Karten oder Headline-Gruppen. |
| [Leer- und Ladezustand](#empty-loading) | `.odsv-empty` `.odsv-skeleton` `.odsv-spinner` | Sagt, was fehlt und was als Nächstes geht; Skelett/Ladekreis beim Laden. |
| [Diagramm-Rahmen](#chart) | `.odsv-chart` `.odsv-legend` `.odsv-swatch` `.odsv-stackbar` … | Rahmen mit Aussage-Titel, Legende, Zeichenfläche und Quelle; Zeichnen über odsv-charts. |
| [Analyse-Diagramme](#analysis) | `.odsv-data-cell` `.odsv-data-cell-text` `.odsv-data-bubble` `.odsv-data-outlier` … | Verteilung, Zusammenhang, Abweichung, Rang, Trichter, Heatmap und viele Reihen analysieren. |
| [Labels für 3D und Diagramme](#label3d) | `.odsv-label3d` `.odsv-marker` `.odsv-stage` `.odsv-leader` … | Pillen mit Hinweislinie über 3D-Bühnen oder Illustrationen; nummerierte Marken für schmale Flächen. |
| [Signet und Wortmarke](#signet) | `.odsv-signet-card` `.odsv-signet` `.odsv-signet-arc` `.odsv-signet-dot` … | Markenmoment (Hero, Titelfolie): Basis- oder Themen-Signet (KI, Netzwerk, Daten, Code, Berge, Fahrrad, Outdoor, Route). |
| [Liste und Fakten](#list-facts) | `.odsv-list` `.odsv-facts` | Aufzählung (Punkte gelb) oder nummerierte Liste; Fakten als <dl>. |
| [Headline-Gruppe](#hgroup) | `.odsv-hgroup` | Dreiklang Eyebrow → Headline → Zweitsatz als Block, optional mit Icon-Kachel. |
| [Toast](#toast) | `.odsv-toast` | Kurze Bestätigung nach einer Handlung („Stand gespeichert“). |
| [Fußbereich](#footer) | `.odsv-footer` | Stand, Quellen, Impressum links; Wortmarke rechts. |
| [Hilfsklassen](#utilities) | `.odsv-sr-only` `.odsv-mt` `.odsv-hide-lg` `.odsv-no-print` … | . |

<a id="typography"></a>
## Typografie

**Wofür:** Textstile für jede Ausgabe. Dreiklang je Abschnitt: .odsv-eyebrow → .odsv-display/.odsv-h1 → .odsv-sub, danach .odsv-body.

**Nicht für:** Versalien für Fließtext, Warnungen, Fehler oder Tabellenzellen (dafür .odsv-body, .odsv-body-small).

| Klasse/Variante | Bedeutung |
|---|---|
| `display` | Hero-/Titel-Headline, 28→64 px, Versalien 0,2 em |
| `h1` | Sektions-Headline, 22→40 px, Versalien |
| `h2` | Unterabschnitt, 24 px, Versalien 0,12 em |
| `h3` | Karten-/Block-Headline, normale Schreibweise |
| `h4` | kleine Überschrift 17 px |
| `sub` | grauer Zweitsatz unter jeder Headline |
| `body` | Fließtext 17 px, max. 640 px breit |
| `body-small` | Erklärtext in Karten/Tabellen 15 px |
| `small` | Fußnote, Quelle 14 px |
| `caption` | Achsen, Zeitstempel 12 px |
| `label` | Feld-/Gruppenlabel in Versalien 13 px |
| `number` | große Kennzahl 40→48 px, tabular-nums |
| `mono` | Code, IDs |
| `accent` | Hervorhebung in Akzentfarbe (sparsam) |
| `muted` | abgeschwächter Text |

**Regeln**

- Headline höchstens 3 Wörter / 24 Zeichen / 2 Zeilen.
- Versalien nur per CSS (text-transform), im Quelltext normale Schreibweise.
- Eyebrow ist ein <p>, keine Überschrift; Headline-Ebenen: ein h1 je Seite, h2 je Sektion, h3 in Karten (Klasse ≠ Element: <h2 class="odsv-h1"> ist erlaubt).
- Lange Wörter: &shy; setzen oder odsv.js einbinden (ODSV.fit verhindert Bruch mitten im Wort).
- Zahlen, die untereinander stehen oder sich ändern: .odsv-tabular bzw. .odsv-number.

**Barrierefreiheit**

- Text nie als Bild.
- Kontrast: Fließtext ≥ 4,5:1 – .odsv-muted/.odsv-caption nicht auf surface-3.

**Inhaltsgrenzen:** eyebrow: 1–4 Wörter · headline: 1–3 Wörter, ≤ 24 Zeichen · sub: 1 Satz, ≤ 90 Zeichen · body: Absätze ≤ 4 Sätze

<a id="layout"></a>
## Layout-Primitive

**Wofür:** Seitengerüst: .odsv-container (max. Breite) → .odsv-section (vertikaler Rhythmus) → .odsv-grid mit .odsv-col-N / .odsv-col-{sm|md|lg|xl}-N; innen .odsv-stack (vertikal) und .odsv-cluster (horizontal, bricht um).

**Nicht für:** Eigene Abstände per style-Attribut oder feste px-Breiten.

| Klasse/Variante | Bedeutung |
|---|---|
| `container--wide` | breiter Container (Dashboard) |
| `container--text` | Lesebreite für Fließtext |
| `section--tight` | weniger Innenabstand |
| `section--rule` | Haarlinie oben |
| `grid--dashboard` | Dashboard-Raster, Lücke 16 px |
| `stack--N` | Abstand space-N zwischen Kindern (1,2,3,6,8,12) |
| `cluster--2|6` | Abstand space-2/space-6 |
| `cluster--between|center|start` | Verteilung |
| `section-head--center` | zentrierter Sektionskopf |

**Elemente:** `__main`

**Regeln**

- Mobile-First: .odsv-col-12 als Basis, ab Breakpoint überschreiben (sm 600, md 768, lg 1024, xl 1280).
- Karten/Kacheln in einer Rasterzeile werden automatisch gleich hoch.
- Breite Inhalte (Tabellen) in .odsv-scroll-x bzw. .odsv-table-wrap, nie die Seite seitlich scrollen lassen.

**Barrierefreiheit**

- Reihenfolge im DOM = Lesereihenfolge; Raster nicht per order umsortieren.

**Beispiel – Raster** (weitere in `components.json`, live: `web/index.html#layout`)

```html
<div class="odsv-grid">
<div class="odsv-col-md-4"><div class="docs-box">md-4</div></div>
<div class="odsv-col-md-4"><div class="docs-box">md-4</div></div>
<div class="odsv-col-md-4"><div class="docs-box">md-4</div></div>
<div class="odsv-col-6 odsv-col-lg-3"><div class="docs-box">6 / lg-3</div></div>
<div class="odsv-col-6 odsv-col-lg-3"><div class="docs-box">6 / lg-3</div></div>
<div class="odsv-col-12 odsv-col-lg-6"><div class="docs-box">12 / lg-6</div></div>
</div>
```

<a id="icon"></a>
## Icon

**Wofür:** Line-Icons aus dem Sprite web/icons.svg: <svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-NAME"/></svg>.

**Nicht für:** Gefüllte oder mehrfarbige Icons, Emoji, Icons ohne Bedeutung.

| Klasse/Variante | Bedeutung |
|---|---|
| `icon--sm` | 18 px (in Buttons) |
| `icon--lg` | 44 px (Kachel) |

**Regeln**

- 24er-Raster, Strich 2 px, runde Enden, Farbe currentColor.
- Verfügbare Namen siehe catalog/icons.json; fehlende aus Lucide (gleiche Maße) ergänzen.

**Barrierefreiheit**

- Dekorativ: aria-hidden="true". Allein stehend (Icon-Button): Name per aria-label oder .odsv-sr-only.

**Beispiel – Größen** (weitere in `components.json`, live: `web/index.html#icons`)

```html
<svg aria-hidden="true" class="odsv-icon odsv-icon--sm"><use href="#odsv-icon-bolt"></use></svg>
<svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-bolt"></use></svg>
<svg aria-hidden="true" class="odsv-icon odsv-icon--lg"><use href="#odsv-icon-bolt"></use></svg>
```

<a id="button"></a>
## Button

**Wofür:** Handlungen auslösen. Primär = die eine Haupthandlung der Ansicht.

**Nicht für:** Navigation zu anderer Seite ohne Handlung (dafür .odsv-link); mehrere Primär-Buttons nebeneinander.

| Klasse/Variante | Bedeutung |
|---|---|
| `btn--primary` | gelb, Haupthandlung, ab 600 px min. 240 px breit |
| `btn--secondary` | hellgrau, zweite Handlung |
| `btn--ghost` | dunkel mit Rand, Nebenhandlung |
| `btn--danger` | zerstörerische Handlung (rot) |
| `btn--md` | 44 px hoch |
| `btn--sm` | 36 px hoch (auf Touch 44 px) |
| `btn--icon` | quadratisch, nur Icon |
| `btn--block` | volle Breite |
| `btn--block-sm` | volle Breite nur mobil |

**Zustände:** `is-loading` – zeigt Ladekreis, aria-busy="true" setzen · `disabled / aria-disabled="true"` – deaktiviert · `is-hover / is-active / is-focus` – nur für Dokumentation

**Regeln**

- Genau ein .odsv-btn--primary je Ansicht.
- Beschriftung = Verb + Ziel („Projekt starten“), nie „OK“, „Hier klicken“, „Weiter“ ohne Ziel.
- Element: <button type="button"> für Handlungen, <a href> nur wenn navigiert wird.

**Barrierefreiheit**

- Icon-only braucht aria-label.
- Fokusring nie entfernen.

**Inhaltsgrenzen:** label: 1–3 Wörter

**Beispiel – Varianten** (weitere in `components.json`, live: `web/index.html#buttons`)

```html
<button class="odsv-btn odsv-btn--primary" type="button">Projekt starten</button>
<button class="odsv-btn odsv-btn--secondary" type="button">Zur Übersicht</button>
<button class="odsv-btn odsv-btn--ghost" type="button">Bericht öffnen</button>
<button class="odsv-btn odsv-btn--ghost odsv-btn--danger" type="button">Löschen</button>
```

<a id="link"></a>
## Link

**Wofür:** Navigation im Text oder leise Nebenaktion („Überspringen“).

**Nicht für:** Haupthandlungen (dafür Button).

| Klasse/Variante | Bedeutung |
|---|---|
| `link--muted` | leiser Link in Grau |
| `link--plain` | ohne Unterstreichung (nur in Navigation) |
| `textbtn` | Button im Link-Stil für leise Aktionen ohne Navigation |

**Regeln**

- Im Fließtext immer unterstrichen.
- Linktext nennt das Ziel; Dateien mit Typ und Größe: „Bericht (PDF, 1,2 MB)“.
- Externe Links mit Icon external.

**Barrierefreiheit**

- Leise Links: Trefferfläche ≥ 24 px (Maus) bzw. 44 px (Touch) – erledigt odsv.css.

**Beispiel** (weitere in `components.json`, live: `web/index.html#links`)

```html
<p class="odsv-body">Die <a class="odsv-link" href="#links">Bedienungsanleitung (PDF, 1,2 MB)</a> enthält alle Details. <a class="odsv-link" href="https://example.org">Externer Link<svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-external"></use></svg></a></p>
<p class="odsv-small"><a class="odsv-link odsv-link--muted" href="#links">Überspringen</a> · <button class="odsv-textbtn" type="button">Zurücksetzen</button> · <a class="odsv-link is-hover" href="#links">Hover</a></p>
```

<a id="card"></a>
## Karte

**Wofür:** Gruppiert zusammengehörige Inhalte auf einer Fläche (surface-1, 1-px-Rand, Radius 28).

**Nicht für:** Eine Karte als einziger Träger einer Gruppierung bei wichtigen Informationen (Rand ist Dekor); Karten in Karten in Karten.

| Klasse/Variante | Bedeutung |
|---|---|
| `card--level-0|2|3` | Flächenstufe (0 = Grund, 2 = Karte in Karte, 3 = gedrückt) |
| `card--inset` | eingelassene Fläche |
| `card--stage` | Bühne für 3D/Illustration |
| `card--outline` | nur Rand |
| `card--accent` | gelber Rand – Empfehlung, sparsam |
| `card--active` | aktiver/ausgewählter Zustand |
| `card--success|warning|danger` | Rand in Statusfarbe |
| `card--compact` | Dashboard: Radius 20, Abstand 16 |
| `card--interactive` | ganze Karte klickbar (als <a>) |
| `card--flush` | ohne Innenabstand (z. B. Tabelle) |

**Elemente:** `__footer`, `__label`, `__text`, `__title`

**Regeln**

- Aufbau: .odsv-card__label (optional) → .odsv-card__title (h3) → .odsv-card__text → .odsv-card__footer.
- Kein Schatten; Tiefe nur über Flächenstufen.
- Statusfarbe am Rand nur zusammen mit Wort/Icon im Inhalt.

**Barrierefreiheit**

- Klickbare Karte: genau ein Link (die Karte selbst), keine verschachtelten Buttons.

**Inhaltsgrenzen:** title: ≤ 40 Zeichen · text: 1–2 Sätze

**Beispiel** (weitere in `components.json`, live: `web/index.html#karten`)

```html
<div class="odsv-card"><p class="odsv-label odsv-card__label">Vorbereitung</p><h3 class="odsv-card__title">Zugang anlegen</h3><p class="odsv-card__text">Konto erstellen und Rolle festlegen.</p></div>
<div class="odsv-card odsv-card--level-2"><h3 class="odsv-card__title">Ebene 2</h3><p class="odsv-card__text">Für Karte in Karte und Hover.</p></div>
<a class="odsv-card odsv-card--interactive" href="#karten"><h3 class="odsv-card__title">Klickbar</h3><p class="odsv-card__text">Hover hebt auf Ebene 2.</p></a>
<div class="odsv-card odsv-card--compact"><h3 class="odsv-card__title">Kompakt</h3><p class="odsv-card__text">Dashboard: Radius 20, Abstand 16.</p></div>
<div class="odsv-card odsv-card--accent"><h3 class="odsv-card__title">Akzent</h3><p class="odsv-card__text">Sparsam für Empfehlungen.</p></div>
<div class="odsv-card odsv-card--success"><h3 class="odsv-card__title">Erfolg</h3><p class="odsv-card__text">Rand in Statusfarbe.</p></div>
<div class="odsv-card odsv-card--warning"><h3 class="odsv-card__title">Warnung</h3><p class="odsv-card__text">Rand in Statusfarbe.</p></div>
<div class="odsv-card odsv-card--danger"><h3 class="odsv-card__title">Fehler</h3><p class="odsv-card__text">Rand in Statusfarbe.</p></div>
```

<a id="kpi"></a>
## KPI- und Spec-Kachel

**Wofür:** Kennzahl mit Label, Einheit, Veränderung und Bezug (.odsv-kpi); Produktdaten im 2×2-Raster (.odsv-specs/.odsv-spec).

**Nicht für:** Zahlen ohne Einheit, Bezug oder Quelle; mehr als eine gelbe Zahl je Kachelgruppe.

| Klasse/Variante | Bedeutung |
|---|---|
| `kpi--lead` | Leit-KPI (größer) |
| `kpi--lg` | große Zahl |
| `kpi__value--accent` | Zahl in Akzentfarbe (eine je Gruppe) |
| `trend--positive|negative|neutral` | Veränderung (Farbe + Icon + Wort) |
| `specs--4` | vier Spalten |

**Elemente:** `__goal`, `__label`, `__note`, `__row`, `__spark`, `__unit`, `__value`

**Regeln**

- Aufbau: <dl class="odsv-kpi"><dt class="odsv-kpi__label">…</dt><dd class="odsv-kpi__value">Wert<span class="odsv-kpi__unit">Einheit</span></dd><dd class="odsv-kpi__row">Trend + .odsv-kpi__note (Bezug)</dd></dl>.
- Leerer Wert: „–“ plus .odsv-kpi__note mit Grund („Noch keine Daten für diesen Zeitraum.“).
- Trendfarbe nach Bedeutung, nicht nach Richtung: steigende Bearbeitungszeit = negativ.

**Barrierefreiheit**

- Trend nie nur über Farbe: Icon und Vorzeichen/Wort.

**Inhaltsgrenzen:** label: 1–3 Wörter · note: Bezug, z. B. „ggü. Vormonat“

**Beispiel – KPI-Reihe mit Trend** (weitere in `components.json`, live: `web/index.html#kpi`)

```html
<div class="odsv-grid odsv-grid--dashboard">
<div class="odsv-col-6 odsv-col-lg-3"><dl class="odsv-kpi">
<dt class="odsv-kpi__label">Aktive Nutzer</dt>
<dd class="odsv-kpi__value">1.284</dd>
<dd class="odsv-kpi__row"><span class="odsv-trend odsv-trend--positive"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-trend-up"></use></svg>+4,2 %</span><span class="odsv-kpi__note">ggü. Vormonat</span></dd>
</dl></div>
<div class="odsv-col-6 odsv-col-lg-3"><dl class="odsv-kpi">
<dt class="odsv-kpi__label">Ø Bearbeitungszeit</dt>
<dd class="odsv-kpi__value">22<span class="odsv-kpi__unit">min</span></dd>
<dd class="odsv-kpi__row"><span class="odsv-trend odsv-trend--negative"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-trend-up"></use></svg>+1,5 min</span><span class="odsv-kpi__note">ggü. Vormonat</span></dd>
</dl></div>
<div class="odsv-col-6 odsv-col-lg-3"><dl class="odsv-kpi">
<dt class="odsv-kpi__label">Supportanfragen</dt>
<dd class="odsv-kpi__value">96</dd>
<dd class="odsv-kpi__row"><span class="odsv-trend odsv-trend--neutral"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-minus"></use></svg>±0 %</span><span class="odsv-kpi__note">ggü. Vormonat</span></dd>
</dl></div>
<div class="odsv-col-6 odsv-col-lg-3"><dl class="odsv-kpi">
<dt class="odsv-kpi__label">Abschlussquote</dt>
<dd class="odsv-kpi__value">–</dd>
<dd class="odsv-kpi__note">Noch keine Daten für diesen Zeitraum.</dd>
</dl></div>
</div>
```

<a id="step"></a>
## Schritt-Karte

**Wofür:** Nummerierte Schritte einer Anleitung oder eines Ablaufs.

**Nicht für:** Ungeordnete Inhalte (dafür Karte).

| Klasse/Variante | Bedeutung |
|---|---|
| `step--active` | aktueller Schritt |
| `step--done` | erledigt |
| `step--inactive` | noch nicht dran (Deckkraft 0,6, bleibt lesbar) |

**Elemente:** `__media`, `__num`, `__skip`, `__text`, `__title`

**Regeln**

- In <ol> setzen; Nummer .odsv-step__num ist dekorativ (aria-hidden), Titel enthält „Schritt N:“ als .odsv-sr-only.
- Aufbau: __num, __media (Line-Art), __title, __text, optional __skip (leiser Link).

**Barrierefreiheit**

- Inaktive Schritte bleiben bedienbar.

**Inhaltsgrenzen:** title: ≤ 30 Zeichen · text: 1–2 Sätze

**Beispiel** (weitere in `components.json`, live: `web/index.html#schritt`)

```html
<ol class="odsv-grid">
<li class="odsv-col-12 odsv-col-md-6">
<article class="odsv-step odsv-step--active">
<span aria-hidden="true" class="odsv-step__num">2</span>
<div aria-hidden="true" class="odsv-step__media">
<svg class="odsv-lineart" viewbox="0 0 220 120"><rect height="58" rx="12" width="120" x="30" y="34"></rect><path class="odsv-lineart--dim" d="M150 52h24a8 8 0 018 8v12a8 8 0 01-8 8h-24"></path><path class="odsv-lineart--marker" d="M62 63h56"></path></svg>
</div>
<h3 class="odsv-step__title"><span class="odsv-sr-only">Schritt 2: </span>Daten importieren</h3>
<p class="odsv-step__text">Vorhandene Daten als CSV-Datei hochladen und Spalten zuordnen.</p>
<a class="odsv-link odsv-link--muted odsv-step__skip" href="#schritt">Überspringen</a>
</article>
</li>
<li class="odsv-col-12 odsv-col-md-6">
<article class="odsv-step odsv-step--inactive">
<span aria-hidden="true" class="odsv-step__num">3</span>
<div aria-hidden="true" class="odsv-step__media">
<svg class="odsv-lineart" viewbox="0 0 220 120"><circle cx="110" cy="60" r="30"></circle><path class="odsv-lineart--marker" d="M110 40v20l14 8"></path></svg>
</div>
<h3 class="odsv-step__title"><span class="odsv-sr-only">Schritt 3: </span>Team einladen</h3>
<p class="odsv-step__text">Inaktive Karten bleiben lesbar und bedienbar.</p>
</article>
</li>
</ol>
```

<a id="progress"></a>
## Fortschrittsleiste

**Wofür:** Segmentierte Leiste für Kapitel (Links) oder Zähler (Checkliste, Ziel).

**Nicht für:** Prozentringe, Fortschritt nur über Farbe.

| Klasse/Variante | Bedeutung |
|---|---|
| `progress--dashed` | Zähl-Leiste, ein Segment je Einheit |
| `progress--success` | Füllung grün (Checkliste) |
| `progress--thick` | dickere Segmente |

**Zustände:** `aria-current="step"` – aktives Segment · `--p (0…1)` – Füllgrad eines Segments per style

**Elemente:** `__bar`, `__link`, `__meta`, `__seg`

**Regeln**

- Kapitelleiste: Segmente sind Links mit aria-label; data-odsv-scrollprogress koppelt die Füllung an den Scroll.
- Zähler daneben als Text: „7 von 12“.

**Barrierefreiheit**

- Zähl-Leiste: role="img" + aria-label oder role="progressbar" mit aria-valuenow.

**Beispiel – Kapitelleiste** (weitere in `components.json`, live: `web/index.html#fortschritt`)

```html
<nav aria-label="Kapitel">
<ol class="odsv-progress">
<li class="odsv-progress__seg" style="--p:1"><a aria-label="Überblick" class="odsv-progress__link" href="#fortschritt"><span class="odsv-progress__bar"></span></a></li>
<li class="odsv-progress__seg" style="--p:1"><a aria-label="Grundlagen" class="odsv-progress__link" href="#fortschritt"><span class="odsv-progress__bar"></span></a></li>
<li aria-current="step" class="odsv-progress__seg" style="--p:0.55"><a aria-current="step" aria-label="Umsetzung" class="odsv-progress__link" href="#fortschritt"><span class="odsv-progress__bar"></span></a></li>
<li class="odsv-progress__seg" style="--p:0"><a aria-label="Test" class="odsv-progress__link" href="#fortschritt"><span class="odsv-progress__bar"></span></a></li>
<li class="odsv-progress__seg" style="--p:0"><a aria-label="Abschluss" class="odsv-progress__link" href="#fortschritt"><span class="odsv-progress__bar"></span></a></li>
</ol>
</nav>
<p class="odsv-eyebrow odsv-mt-4">Umsetzung</p>
```

<a id="segmented"></a>
## Segment-Umschalter

**Wofür:** Einen Wert aus 2–4 Optionen wählen, die Ansicht wechselt sofort (Zeitraum, Diagramm/Tabelle).

**Nicht für:** Mehr als 4 Optionen (dafür Auswahl), Navigation zwischen Seiten (dafür Tabs/Links).

| Klasse/Variante | Bedeutung |
|---|---|
| `segmented--inverse` | aktiv weiß statt gelb (Gegenwahl) |
| `segmented--sm` | klein |
| `segmented--block` | volle Breite |

**Zustände:** `aria-checked="true"` – gewählt

**Elemente:** `__item`

**Regeln**

- Items sind <button role="radio" aria-checked>.

**Barrierefreiheit**

- Container mit aria-label.

**Verhalten (odsv.js):** data-odsv-segmented am Container: role=radiogroup, Pfeiltasten, Event odsv:change.

**Inhaltsgrenzen:** item: 1–2 Wörter

**Beispiel** (weitere in `components.json`, live: `web/index.html#segment`)

```html
<div aria-label="Zeitraum" class="odsv-segmented" data-odsv-segmented="" role="radiogroup">
<button aria-checked="true" class="odsv-segmented__item" data-value="7" role="radio" type="button">7 Tage</button>
<button aria-checked="false" class="odsv-segmented__item" data-value="30" role="radio" type="button">30 Tage</button>
<button aria-checked="false" class="odsv-segmented__item" data-value="90" role="radio" type="button">90 Tage</button>
</div>
<div aria-label="Antwort" class="odsv-segmented odsv-segmented--inverse" data-odsv-segmented="" role="radiogroup">
<button aria-checked="false" class="odsv-segmented__item" data-value="ja" role="radio" type="button">Ja</button>
<button aria-checked="true" class="odsv-segmented__item" data-value="nein" role="radio" type="button">Nein</button>
</div>
<div aria-label="Ansicht" class="odsv-segmented" data-odsv-segmented="" role="radiogroup">
<button aria-checked="true" class="odsv-segmented__item" data-value="chart" role="radio" type="button"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-chart"></use></svg>Diagramm</button>
<button aria-checked="false" class="odsv-segmented__item" data-value="table" role="radio" type="button">Tabelle</button>
</div>
<div aria-label="Dichte" class="odsv-segmented odsv-segmented--sm" data-odsv-segmented="" role="radiogroup">
<button aria-checked="false" class="odsv-segmented__item" data-value="a" role="radio" type="button">Bequem</button>
<button aria-checked="true" class="odsv-segmented__item" data-value="b" role="radio" type="button">Kompakt</button>
</div>
```

<a id="checklist"></a>
## Checkliste

**Wofür:** Abhaken mehrerer Punkte mit gespeichertem Stand und Fortschritt.

**Nicht für:** Einzelne Zustimmung (dafür Checkbox in .odsv-option).

**Elemente:** `__body`, `__group`, `__items`, `__summary`, `__text`, `__title`

**Regeln**

- Label in Versalien (.odsv-check__title), Erklärung grau (.odsv-check__text).
- Gruppen in <fieldset> mit <legend class="odsv-label">.

**Barrierefreiheit**

- Zähler mit role="status".

**Verhalten (odsv.js):** data-odsv-checklist="schlüssel" am Container; Kinder data-odsv-checklist-progress, -count, -reset; jede Checkbox mit data-id. Stand in localStorage (still bei Fehlern).

**Inhaltsgrenzen:** title: 1–2 Wörter · text: ≤ 60 Zeichen

**Beispiel** (weitere in `components.json`, live: `web/index.html#checkliste`)

```html
<div class="odsv-checklist" data-odsv-checklist="docs-demo">
<div class="odsv-checklist__summary">
<ol class="odsv-progress odsv-progress--dashed" data-odsv-checklist-progress=""></ol>
<div class="odsv-progress__meta"><span class="odsv-body-small" data-odsv-checklist-count="" role="status">0 von 4</span><button class="odsv-textbtn" data-odsv-checklist-reset="" type="button">Zurücksetzen</button></div>
<p class="odsv-caption">Dein Fortschritt bleibt auf diesem Gerät gespeichert.</p>
</div>
<fieldset class="odsv-fieldset">
<legend class="odsv-label odsv-checklist__title">Vorbereitung</legend>
<ul class="odsv-checklist__items">
<li><label class="odsv-check"><input class="odsv-checkbox" data-id="anleitung" type="checkbox"/><span class="odsv-check__body"><span class="odsv-check__title">Anleitung</span><span class="odsv-check__text">Anleitung gelesen</span></span></label></li>
<li><label class="odsv-check"><input class="odsv-checkbox" data-id="material" type="checkbox"/><span class="odsv-check__body"><span class="odsv-check__title">Daten</span><span class="odsv-check__text">Daten für den Import vorbereitet</span></span></label></li>
<li><label class="odsv-check"><input class="odsv-checkbox" data-id="zugang" type="checkbox"/><span class="odsv-check__body"><span class="odsv-check__title">Zugang</span><span class="odsv-check__text">Konto angelegt und Rolle zugewiesen</span></span></label></li>
<li><label class="odsv-check"><input class="odsv-checkbox" data-id="team" type="checkbox"/><span class="odsv-check__body"><span class="odsv-check__title">Team</span><span class="odsv-check__text">Teammitglieder eingeladen</span></span></label></li>
</ul>
</fieldset>
</div>
```

<a id="accordion"></a>
## Akkordeon

**Wofür:** Optionale Zusatzinformation (FAQ).

**Nicht für:** Warnungen, Pflichtinformationen oder Hauptinhalt.

| Klasse/Variante | Bedeutung |
|---|---|
| `accordion--card` | als Karte |
| `accordion--last` | letzter Eintrag ohne Linie |

**Elemente:** `__body`

**Regeln**

- Natives <details class="odsv-accordion"><summary>Frage</summary><div class="odsv-accordion__body">…</div></details>.

**Barrierefreiheit**

- summary-Text als Frage formulieren.

**Inhaltsgrenzen:** summary: ≤ 60 Zeichen

**Beispiel** (weitere in `components.json`, live: `web/index.html#akkordeon`)

```html
<div>
<details class="odsv-accordion" open="">
<summary>Wie lange dauert die Einrichtung?</summary>
<div class="odsv-accordion__body"><p>Rund 15 Minuten, ohne Installation.</p></div>
</details>
<details class="odsv-accordion">
<summary>Welche Dateiformate werden unterstützt?</summary>
<div class="odsv-accordion__body"><p>CSV und XLSX.</p></div>
</details>
<details class="odsv-accordion odsv-accordion--last">
<summary>Funktioniert das auch auf dem Smartphone?</summary>
<div class="odsv-accordion__body"><p>Ja, alle Ansichten sind für Mobilgeräte optimiert.</p></div>
</details>
</div>
```

<a id="table"></a>
## Tabelle

**Wofür:** Datensätze vergleichen. Dichten: bequem (Website), kompakt (Dashboard), dicht (nur Zeigergerät).

**Nicht für:** Layout-Zwecke; Versalien in Zellen.

| Klasse/Variante | Bedeutung |
|---|---|
| `table--compact` | Dashboard-Standard |
| `table--dense` | viele Zeilen, nur Zeigergerät |
| `table--hover` | Zeilen-Hover |
| `table--sticky` | fester Kopf |
| `table__num` | Zahlenspalte rechtsbündig, tabular |
| `table__strong` | betonte Zelle |

**Zustände:** `aria-selected="true" an <tr>` – ausgewählte Zeile

**Elemente:** `__num`, `__strong`

**Regeln**

- Immer in .odsv-table-wrap (role="region", aria-label, tabindex="0") – scrollt seitlich statt die Seite.
- Zahlen rechtsbündig, Text links; Kopf in Versalien klein.

**Barrierefreiheit**

- <caption> (gern .odsv-sr-only), <th scope>.

**Beispiel – Bequem (Website)** (weitere in `components.json`, live: `web/index.html#tabellen`)

```html
<div aria-label="Tarife" class="odsv-table-wrap" role="region" tabindex="0">
<table class="odsv-table">
<caption class="odsv-sr-only">Tarife mit Preis und Nutzerzahl</caption>
<thead><tr><th scope="col">Tarif</th><th class="odsv-table__num" scope="col">€/Monat</th><th class="odsv-table__num" scope="col">Nutzer</th><th scope="col">Status</th></tr></thead>
<tbody>
<tr><th scope="row">Team</th><td class="odsv-table__num">49</td><td class="odsv-table__num">25</td><td><span class="odsv-badge odsv-badge--success"><span class="odsv-badge__dot"></span>Aktiv</span></td></tr>
<tr><th scope="row">Basis</th><td class="odsv-table__num">19</td><td class="odsv-table__num">5</td><td><span class="odsv-badge">Bereit</span></td></tr>
</tbody>
</table>
</div>
```

<a id="callout"></a>
## Hinweis (Callout)

**Wofür:** Status- oder Sicherheitshinweis mit Icon und Wort.

**Nicht für:** Dekoration; Warnungen einklappen oder kürzen.

| Klasse/Variante | Bedeutung |
|---|---|
| `callout--info` | Hinweis |
| `callout--success` | Richtig/Erfolg |
| `callout--warning` | Vorsicht (vor dem Schritt, volle Länge) |
| `callout--danger` | Falsch/Gefahr |
| `callout--banner` | kompakt mit getöntem Grund |

**Elemente:** `__head`, `__label`, `__text`, `__title`

**Regeln**

- Aufbau: __head (Icon + __label) → __title (optional) → __text.
- Warnung steht vor dem betroffenen Schritt.
- role: warning → note, danger → alert, success → status.

**Barrierefreiheit**

- Status nie nur über Farbe.

**Inhaltsgrenzen:** label: 1–2 Wörter · title: ≤ 50 Zeichen

**Beispiel** (weitere in `components.json`, live: `web/index.html#callouts`)

```html
<div class="odsv-stack">
<div class="odsv-callout odsv-callout--warning" role="note">
<p class="odsv-callout__head"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-warning"></use></svg><span class="odsv-callout__label">Vorsicht</span></p>
<p class="odsv-callout__title">Änderungen nicht gespeichert</p>
<p class="odsv-callout__text">Erst speichern, dann die Seite verlassen. Warnungen stehen vor dem Schritt, in voller Länge.</p>
</div>
<div class="odsv-callout odsv-callout--info"><p class="odsv-callout__head"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-info"></use></svg><span class="odsv-callout__label">Hinweis</span></p><p class="odsv-callout__text">Zusatzinformation, die den Ablauf nicht stoppt.</p></div>
<div class="odsv-callout odsv-callout--success" role="status"><p class="odsv-callout__head"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-check"></use></svg><span class="odsv-callout__label">Richtig</span></p><p class="odsv-callout__text">Der Import ist abgeschlossen. Alle Datensätze wurden übernommen.</p></div>
<div class="odsv-callout odsv-callout--danger" role="alert"><p class="odsv-callout__head"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-error"></use></svg><span class="odsv-callout__label">Falsch</span></p><p class="odsv-callout__text">Die Datei enthält ungültige Zeilen. Bitte korrigieren und erneut hochladen.</p></div>
<div class="odsv-callout"><p class="odsv-callout__head"><span class="odsv-callout__label">Gut zu wissen</span></p><p class="odsv-callout__text">Neutral: ein Merksatz ohne Status.</p></div>
<div class="odsv-callout odsv-callout--banner odsv-callout--warning"><p class="odsv-callout__head"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-warning"></use></svg><span class="odsv-callout__label">Vorsicht</span></p><p class="odsv-callout__text">Kompaktes Banner mit getöntem Grund.</p></div>
</div>
```

<a id="badge"></a>
## Badge und Pill

**Wofür:** Badge: nicht klickbarer Status (1–2 Wörter). Pill: klickbarer Filter.

**Nicht für:** Badges als Buttons; mehr als ein gelbes Badge je Gruppe.

| Klasse/Variante | Bedeutung |
|---|---|
| `badge--accent` | neu/hervorgehoben |
| `badge--success|warning|danger|info` | Status mit Punkt oder Icon |
| `badge--solid` | gefüllt (starker Status) |
| `badge--count` | Zähler |

**Zustände:** `aria-pressed="true" (Pill)` – aktiver Filter

**Elemente:** `__dot`

**Regeln**

- Status-Badges mit __dot oder Icon plus Wort.

**Barrierefreiheit**

- Pill ist <button aria-pressed>.

**Inhaltsgrenzen:** label: 1–2 Wörter

**Beispiel – Badges** (weitere in `components.json`, live: `web/index.html#badges`)

```html
<div class="odsv-cluster">
<span class="odsv-badge">Neutral</span>
<span class="odsv-badge odsv-badge--accent">Neu</span>
<span class="odsv-badge odsv-badge--success"><span class="odsv-badge__dot"></span>Aktiv</span>
<span class="odsv-badge odsv-badge--warning"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-warning"></use></svg>Vorsicht</span>
<span class="odsv-badge odsv-badge--danger"><span class="odsv-badge__dot"></span>Fehler</span>
<span class="odsv-badge odsv-badge--info"><span class="odsv-badge__dot"></span>Info</span>
</div>
<div class="odsv-cluster odsv-mt-4">
<span class="odsv-badge odsv-badge--solid odsv-badge--success">Fertig</span>
<span class="odsv-badge odsv-badge--solid odsv-badge--warning">Offen</span>
<span class="odsv-badge odsv-badge--solid odsv-badge--danger">Alarm</span>
<span class="odsv-badge odsv-badge--solid odsv-badge--info">Info</span>
<span aria-label="3 neue Meldungen" class="odsv-badge odsv-badge--count">3</span>
</div>
```

<a id="tabs"></a>
## Tabs

**Wofür:** Gleichrangige Ansichten auf derselben Seite wechseln.

**Nicht für:** Schrittfolgen (dafür Schritte), Wertwahl (dafür Segment-Umschalter).

**Zustände:** `aria-selected="true"` – aktiver Tab · `disabled` – nicht verfügbar

**Regeln**

- Tab = <button role="tab" aria-controls>, Panel = role="tabpanel" aria-labelledby.

**Barrierefreiheit**

- Nur aktiver Tab im Tab-Fokus (tabindex=-1 für andere) – erledigt odsv.js.

**Verhalten (odsv.js):** data-odsv-tabs am role="tablist": Pfeiltasten, Pos1/Ende, schaltet Panels (aria-controls).

**Inhaltsgrenzen:** tab: 1–2 Wörter

**Beispiel** (weitere in `components.json`, live: `web/index.html#tabs`)

```html
<div>
<div aria-label="Bereiche" class="odsv-tabs" data-odsv-tabs="" role="tablist">
<button aria-controls="dp-1" aria-selected="true" class="odsv-tab" id="dt-1" role="tab" type="button">Übersicht</button>
<button aria-controls="dp-2" aria-selected="false" class="odsv-tab" id="dt-2" role="tab" tabindex="-1" type="button">Qualität</button>
<button aria-controls="dp-3" aria-selected="false" class="odsv-tab" id="dt-3" role="tab" tabindex="-1" type="button">Support</button>
<button aria-selected="false" class="odsv-tab" disabled="" role="tab" type="button">Archiv</button>
</div>
<div aria-labelledby="dt-1" class="odsv-tabpanel" id="dp-1" role="tabpanel" tabindex="0"><p class="odsv-body">Inhalt der Übersicht.</p></div>
<div aria-labelledby="dt-2" class="odsv-tabpanel" hidden="" id="dp-2" role="tabpanel" tabindex="0"><p class="odsv-body">Inhalt der Qualität.</p></div>
<div aria-labelledby="dt-3" class="odsv-tabpanel" hidden="" id="dp-3" role="tabpanel" tabindex="0"><p class="odsv-body">Inhalt des Supports.</p></div>
</div>
```

<a id="form"></a>
## Formularfelder

**Wofür:** Eingaben mit sichtbarem Label, Hinweis und Fehler am Feld.

**Nicht für:** Platzhalter als Label; Fehler nur über Farbe.

| Klasse/Variante | Bedeutung |
|---|---|
| `field__label` | sichtbares Label |
| `field__opt` | „(optional)“ |
| `field__hint` | Hinweis unter dem Feld |
| `field__error` | Fehlertext mit Icon |
| `option` | Checkbox/Radio/Schalter mit Text, min. 44 px |
| `switch` | An/Aus mit sichtbarem Wort („Benachrichtigungen: an“) |

**Zustände:** `is-invalid (an .odsv-field) + aria-invalid="true"` – Fehler · `disabled` – deaktiviert (Label wird grau) · `readonly` – nur lesen

**Elemente:** `__control`, `__error`, `__hint`, `__icon`, `__label`, `__opt`

**Regeln**

- Fehler: Text sagt, was zu tun ist („Bitte eine vollständige Adresse angeben.“), per aria-describedby verknüpft.
- Radiogruppen in <fieldset> mit <legend class="odsv-label">.
- Auswahl = natives <select> in .odsv-select mit Chevron-Icon.

**Barrierefreiheit**

- Jedes Feld hat <label for>.
- Fehler mit role="alert".

**Inhaltsgrenzen:** label: 1–3 Wörter · error: 1 Satz mit Lösung

**Beispiel – Textfelder und Zustände** (weitere in `components.json`, live: `web/index.html#formulare`)

```html
<div class="odsv-field"><label class="odsv-field__label" for="f1">Projektname</label><input autocomplete="off" class="odsv-input" id="f1" placeholder="z. B. Website-Relaunch" type="text"/></div>
<div class="odsv-field"><label class="odsv-field__label" for="f2">Projektname</label><input class="odsv-input is-hover" id="f2" type="text" value="Website-Relaunch"/></div>
<div class="odsv-field"><label class="odsv-field__label" for="f3">Projektname</label><input class="odsv-input is-focus" id="f3" type="text" value="Website-Relaunch"/></div>
<div class="odsv-field is-invalid"><label class="odsv-field__label" for="f4">E-Mail</label><input aria-describedby="f4e" aria-invalid="true" class="odsv-input" id="f4" type="email" value="name@"/><p class="odsv-field__error" id="f4e" role="alert"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-error"></use></svg>Bitte eine vollständige Adresse angeben.</p></div>
<div class="odsv-field"><label class="odsv-field__label" for="f5">Projekt-ID</label><input class="odsv-input" disabled="" id="f5" type="text" value="PRJ-0042"/></div>
<div class="odsv-field"><label class="odsv-field__label" for="f6">Erstellt von</label><input class="odsv-input" id="f6" readonly="" type="text" value="Admin"/></div>
```

<a id="tooltip"></a>
## Tooltip

**Wofür:** Benennt Icon-Buttons oder ergänzt Unwichtiges.

**Nicht für:** Nötige Information (auf Touch unerreichbar).

| Klasse/Variante | Bedeutung |
|---|---|
| `tooltip--start|end` | Ausrichtung am Rand |
| `tooltip--below` | unterhalb |

**Zustände:** `is-open` – dauerhaft sichtbar (Doku) · `is-dismissed` – per Escape geschlossen

**Elemente:** `__content`

**Regeln**

- Erscheint bei Hover (300 ms) und sofort bei Fokus; Escape schließt.

**Barrierefreiheit**

- role="tooltip" + aria-describedby am Auslöser.

**Inhaltsgrenzen:** text: ≤ 80 Zeichen

**Beispiel** (weitere in `components.json`, live: `web/index.html#tooltip`)

```html
<div class="odsv-cluster odsv-cluster--6" style="padding-top:var(--odsv-space-12)">
<span class="odsv-tooltip is-open"><button aria-describedby="tt1" class="odsv-icon-btn" type="button"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-download"></use></svg><span class="odsv-sr-only">Herunterladen</span></button><span class="odsv-tooltip__content" id="tt1" role="tooltip">Anleitung herunterladen</span></span>
<span class="odsv-tooltip odsv-tooltip--start"><button aria-describedby="tt2" class="odsv-btn odsv-btn--ghost odsv-btn--md" type="button">Ausgerichtet links</button><span class="odsv-tooltip__content" id="tt2" role="tooltip">Linksbündig zum Auslöser, falls der Rand knapp ist.</span></span>
</div>
```

<a id="navigation"></a>
## Navigation und Top-Bar

**Wofür:** Klebende Top-Bar mit Wortmarke, Navigation, Aktionen; Seitenleiste fürs Dashboard ab 1024 px.

**Nicht für:** Mehr als 5 Hauptpunkte in der Top-Bar.

| Klasse/Variante | Bedeutung |
|---|---|
| `topbar--static` | nicht klebend |
| `topbar--wide` | breit (Dashboard) |
| `nav--stacked` | untereinander |
| `sidebar--collapsed` | eingeklappt |

**Zustände:** `aria-current="page"` – aktueller Punkt

**Elemente:** `__actions`, `__group`, `__inner`, `__link`, `__mark`, `__meta`, `__moon`, `__name`, `__nav`, `__progress`, `__sun`, `__text`, `__toggle`

**Regeln**

- Erster Link der Seite: .odsv-skip „Zum Inhalt“.
- Mobil: Navigation hinter Menü-Button.

**Barrierefreiheit**

- <nav aria-label>, aria-current="page".

**Verhalten (odsv.js):** data-odsv-nav-toggle (mobiles Menü, aria-expanded) · data-odsv-theme-toggle (Theme, gespeichert).

**Inhaltsgrenzen:** item: 1–2 Wörter

**Beispiel – Top-Bar** (weitere in `components.json`, live: `web/index.html#navigation`)

```html
<header class="odsv-topbar odsv-topbar--static">
<div class="odsv-topbar__inner">
<a class="odsv-brand" href="#navigation"><span class="odsv-brand__name">Produktname</span></a>
<nav aria-label="Hauptnavigation" class="odsv-topbar__nav" id="demo-nav">
<ul class="odsv-nav">
<li><a aria-current="page" class="odsv-nav__link" href="#navigation">Übersicht</a></li>
<li><a class="odsv-nav__link" href="#navigation">Berichte</a></li>
<li><a class="odsv-nav__link" href="#navigation">Hilfe</a></li>
</ul>
</nav>
<div class="odsv-topbar__actions">
<button aria-controls="demo-nav" aria-expanded="false" aria-label="Menü" class="odsv-icon-btn odsv-topbar__toggle" data-odsv-nav-toggle="" type="button"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-menu"></use></svg></button>
</div>
</div>
</header>
```

<a id="sheet"></a>
## Bottom-Sheet

**Wofür:** Abschluss-Aufforderung (im Fluss) oder modale Rückfrage.

**Nicht für:** Lange Formulare, mehrere Primär-Aktionen.

| Klasse/Variante | Bedeutung |
|---|---|
| `sheet--inline` | im Fluss |
| `sheet--static` | statisch |
| `sheet--sticky` | am unteren Rand klebend |

**Elemente:** `__actions`, `__backdrop`, `__grabber`, `__panel`, `__text`, `__title`

**Regeln**

- Aufbau: __grabber, __title (fett, zentriert), __text, __actions (gelber Button + leiser Link).

**Barrierefreiheit**

- Modal: role="dialog" aria-modal="true" aria-labelledby.

**Verhalten (odsv.js):** data-odsv-sheet-open="#id" / data-odsv-sheet-close: Fokusfalle, Escape, Fokus zurück.

**Inhaltsgrenzen:** title: ≤ 40 Zeichen

**Beispiel – Im Fluss** (weitere in `components.json`, live: `web/index.html#sheet`)

```html
<div class="odsv-sheet odsv-sheet--inline">
<div class="odsv-sheet__panel">
<span aria-hidden="true" class="odsv-sheet__grabber"></span>
<h3 class="odsv-sheet__title">Bereit für den Start?</h3>
<p class="odsv-sheet__text">Die Einrichtung führt dich in fünf Schritten durch.</p>
<div class="odsv-sheet__actions">
<a class="odsv-btn odsv-btn--primary" href="#sheet">Einrichtung starten</a>
<a class="odsv-link odsv-link--muted" href="#sheet">Später</a>
</div>
</div>
</div>
```

<a id="tile"></a>
## Icon-Kachel

**Wofür:** App-Icon-artige Kachel über Karten oder Headline-Gruppen.

**Nicht für:** Mehr als eine gelbe Kachel je Ansicht.

| Klasse/Variante | Bedeutung |
|---|---|
| `tile--accent` | gelber Verlauf (Hauptmoment) |
| `tile--sm` | 44 px |
| `tile--lg` | 88 px |
| `tile--xl` | 96 px (Hero) |

**Regeln**

- Dekorativ: aria-hidden="true".

**Beispiel** (weitere in `components.json`, live: `web/index.html#kacheln`)

```html
<span aria-hidden="true" class="odsv-tile"><svg class="odsv-icon"><use href="#odsv-icon-chart"></use></svg></span>
<span aria-hidden="true" class="odsv-tile odsv-tile--accent"><svg class="odsv-icon"><use href="#odsv-icon-user"></use></svg></span>
<span aria-hidden="true" class="odsv-tile odsv-tile--lg"><svg class="odsv-icon"><use href="#odsv-icon-shield"></use></svg></span>
<span aria-hidden="true" class="odsv-tile odsv-tile--xl odsv-tile--accent"><svg class="odsv-icon"><use href="#odsv-icon-bell"></use></svg></span>
<span aria-hidden="true" class="odsv-tile odsv-tile--sm"><svg class="odsv-icon"><use href="#odsv-icon-clock"></use></svg></span>
```

<a id="empty-loading"></a>
## Leer- und Ladezustand

**Wofür:** Sagt, was fehlt und was als Nächstes geht; Skelett/Ladekreis beim Laden.

**Nicht für:** „Ups“, Schuldzuweisung, Leerzustand ohne Handlung.

| Klasse/Variante | Bedeutung |
|---|---|
| `skeleton--title|text|short|block|circle` | Platzhalterformen |

**Elemente:** `__text`, `__title`

**Regeln**

- Leerzustand: Icon-Kachel, __title, __text, eine Handlung (Button).

**Barrierefreiheit**

- Behälter aria-busy="true", Meldung role="status"; Puls entfällt bei reduzierter Bewegung.

**Inhaltsgrenzen:** title: ≤ 40 Zeichen · text: 1 Satz mit nächster Handlung

**Beispiel – Leerzustand** (weitere in `components.json`, live: `web/index.html#leer`)

```html
<div class="odsv-empty">
<span aria-hidden="true" class="odsv-tile"><svg class="odsv-icon"><use href="#odsv-icon-search"></use></svg></span>
<h3 class="odsv-empty__title">Keine Daten für diesen Zeitraum</h3>
<p class="odsv-empty__text">Wähle einen anderen Zeitraum oder setze die Filter zurück.</p>
<button class="odsv-btn odsv-btn--ghost odsv-btn--md" type="button">Filter zurücksetzen</button>
</div>
```

<a id="chart"></a>
## Diagramm-Rahmen

**Wofür:** Rahmen mit Aussage-Titel, Legende, Zeichenfläche und Quelle; Zeichnen über odsv-charts.js oder eigene SVG mit den .odsv-dv-N-Klassen.

**Nicht für:** Diagramm ohne Quelle, Themen-Titel statt Aussage, Status- und Reihenfarben im selben Diagramm.

| Klasse/Variante | Bedeutung |
|---|---|
| `dv-1…dv-7` | kategoriale Farben in fester Reihenfolge |
| `dv-highlight` | betonte Reihe |
| `dv-context` | Kontextreihe grau |
| `dv-neutral` | Sonstige |
| `dv-positive|negative` | Statusbedeutung |
| `dv-seq-1…6` | Menge, sequenzielle Palette (wenig → viel) |
| `dv-div-neg|div-pos` | Richtung unter/über Basis (Blau ↔ Orange), Stufen -3 … 3 und div-mid |
| `swatch--line` | Legendenmarke als Linie |
| `chart__tools` | Platz für den Tabellen-Schalter im Kopf |

**Elemente:** `__footer`, `__header`, `__item`, `__multiple`, `__multiple-title`, `__multiples`, `__plot`, `__subtitle`, `__table`, `__tip`, `__title`, `__tools`

**Regeln**

- Aufbau: <figure class="odsv-chart"> → __header (Eyebrow, <figcaption class="odsv-chart__title">, __subtitle, optional __tools) → .odsv-legend → __plot → __footer (Quelle · Stand).
- Ab 2 Reihen Legende, höchstens 4 Reihen direkt beschriften.
- Balken beginnen bei 0; Achse endet beim nächsten runden Wert.
- Legendentext trägt nie die Reihenfarbe: die dv-Klasse sitzt an der .odsv-swatch, nicht am Text.

**Barrierefreiheit**

- SVG mit role="img" und aria-label, das die Aussage enthält (label-Option).
- Jedes Diagramm bietet die Daten als Tabelle: Button [data-odsv-chart-table] im Kopf.

**Verhalten (odsv.js):** window.ODSVCharts.line|bars|donut|spark; Analyseformen siehe Komponente „Analyse-Diagramme“ und catalog/js-api.md.

**Inhaltsgrenzen:** title: Aussage, ≤ 60 Zeichen · subtitle: Einheit/Bezug

**Beispiel – Linie mit Legende** (weitere in `components.json`, live: `web/index.html#diagramm`)

```html
<figure class="odsv-chart">
<div class="odsv-chart__header">
<div><p class="odsv-eyebrow">Registrierungen</p><figcaption class="odsv-chart__title">Registrierungen wachsen seit Januar stetig</figcaption><p class="odsv-chart__subtitle">je Monat, Anzahl</p></div>
</div>
<ul aria-label="Legende" class="odsv-legend">
<li class="odsv-legend__item odsv-dv-1"><span class="odsv-swatch odsv-swatch--line"></span><span style="color:var(--odsv-color-text-secondary)">Registrierungen</span></li>
<li class="odsv-legend__item odsv-dv-2"><span class="odsv-swatch odsv-swatch--line"></span><span style="color:var(--odsv-color-text-secondary)">Supportanfragen</span></li>
</ul>
<div class="odsv-chart__plot" data-demo-chart="line"></div>
<p class="odsv-chart__footer">Quelle: Beispieldaten · Stand 17.11.2026</p>
</figure>
```

<a id="analysis"></a>
## Analyse-Diagramme

**Wofür:** Verteilung, Zusammenhang, Abweichung, Rang, Trichter, Heatmap und viele Reihen analysieren.

**Nicht für:** Zwei y-Achsen, 3D, Verläufe in Datenflächen, Regenbogen-Heatmaps, Rot/Grün ohne Vorzeichen, Streudiagramm mit mehr als 5 Farben (hell 3), Kreis statt sortierter Balken.

| Klasse/Variante | Bedeutung |
|---|---|
| `line + annotations/target/endLabels` | Verlauf mit Ereignislinie und Pille, Zielwert gestrichelt, Reihen am Ende beschriftet |
| `columns mode grouped|stacked|percent` | Säulen mit mehreren Reihen |
| `hbars` | waagrecht, absteigend sortiert; eine Kategorie dv-highlight, Rest dv-context |
| `diverging` | ab Nulllinie, negativ dv-div-neg, positiv dv-div-pos, Werte mit Vorzeichen |
| `funnel` | abgestufte Einzelfarbe dv-seq, Wert und Quote zum Vorschritt |
| `histogram` | Klassen gleicher Breite, optional Median oder Mittelwert |
| `boxplot` | Strich = Spanne bis 1,5 × IQR, dicker Strich = mittlere Hälfte, Punkt = Median, Ringe = Ausreißer |
| `scatter` | Punkte oder Blasen (r), optional Trendlinie mit R² |
| `heatmap` | 6 Stufen dv-seq mit Skala, leere Zelle gestrichelt |
| `slope` | zwei Zeitpunkte, eine Reihe betont, Rest Kontext |
| `multiples` | kleine Vielfache mit gleicher Achse, übrige Reihen als Kontext |

**Zustände:** `Legende aria-pressed="false"` – Reihe ausgeblendet (letzte sichtbare Reihe bleibt) · `[data-odsv-chart-table] aria-expanded="true"` – Tabelle unter der Zeichnung sichtbar · `SVG im Fokus` – Pfeiltasten wandern durch Punkte/Balken/Zellen, Wert wird angesagt, Esc schließt den Tooltip

**Regeln**

- Form nach Aufgabe der Daten wählen (SPEC 7.3), nicht nach Optik.
- Titel ist die Aussage; der Zweitsatz nennt Einheit, Bezug und bei Verteilungen n.
- Eine Sache betonen: dv-highlight für die eine Kategorie oder Reihe, Rest dv-context.
- Menge in dv-seq, Richtung in dv-div, Zugehörigkeit in dv-1…7 – Paletten nie mischen.
- Einheit einmal an der Achse (unit, xLabel, yLabel), nicht an jedem Wert.
- Balken und Säulen beginnen bei 0; Streudiagramm und Boxplot dürfen ohne 0 beginnen.
- Zu jedem Diagramm den Tabellen-Schalter anbieten.

**Barrierefreiheit**

- label-Option nennt die Aussage mit den wichtigsten Zahlen (role="img").
- Tastatur: Tab fokussiert die Zeichnung, Pfeiltasten wandern, eine aria-live-Region sagt den Wert an.
- Tabellenansicht mit Zeilen- und Spaltenköpfen für jede Form.
- Farbe nie allein: Vorzeichen bei Abweichungen, Beschriftung der Betonung, Skala bei der Heatmap.

**Verhalten (odsv.js):** window.ODSVCharts.columns|hbars|diverging|funnel|histogram|boxplot|scatter|heatmap|slope|multiples und line mit annotations, target, endLabels – siehe catalog/js-api.md.

**Inhaltsgrenzen:** title: Aussage, ≤ 60 Zeichen · subtitle: Einheit, Bezug, n · Kategorien: hbars bis 12, columns bis 12 Gruppen, heatmap bis 24 Spalten · Reihen: line bis 4, columns bis 4, scatter bis 5 (hell 3), multiples bis 12

**Beispiel – Verlauf mit Ereignis und Ziel** (weitere in `components.json`, live: `web/index.html#analyse`)

```html
<figure class="odsv-chart">
<div class="odsv-chart__header">
<div><p class="odsv-eyebrow">Umsatz</p><figcaption class="odsv-chart__title">Nach dem Relaunch übertrifft Web das Ziel</figcaption><p class="odsv-chart__subtitle">je Monat, in Tsd. €</p></div>
<div class="odsv-chart__tools"><button aria-expanded="false" class="odsv-btn odsv-btn--ghost odsv-btn--sm" data-odsv-chart-table="" type="button"><span data-odsv-label="">Daten als Tabelle</span></button></div>
</div>
<ul aria-label="Reihen ein- und ausblenden" class="odsv-legend"><li><button aria-pressed="true" class="odsv-legend__item" data-odsv-series="Web" type="button"><span class="odsv-swatch odsv-swatch--line odsv-dv-1"></span>Web</button></li><li><button aria-pressed="true" class="odsv-legend__item" data-odsv-series="App" type="button"><span class="odsv-swatch odsv-swatch--line odsv-dv-2"></span>App</button></li><li><button aria-pressed="true" class="odsv-legend__item" data-odsv-series="Händler" type="button"><span class="odsv-swatch odsv-swatch--line odsv-dv-3"></span>Händler</button></li></ul>
<div class="odsv-chart__plot" data-demo-chart="line-annot"></div>
<p class="odsv-chart__footer">Quelle: Beispieldaten · Stand 17.11.2026</p>
</figure>
```

<a id="label3d"></a>
## Labels für 3D und Diagramme

**Wofür:** Pillen mit Hinweislinie über 3D-Bühnen oder Illustrationen; nummerierte Marken für schmale Flächen.

**Nicht für:** Mehr als ein betontes Label je Ansicht.

| Klasse/Variante | Bedeutung |
|---|---|
| `label3d--strong` | betont (gelb) |
| `label3d--bad` | Problem (roter Rand) |
| `label3d--wrong` | falsch (rot gefüllt) |
| `label3d--static` | im Fluss statt absolut |
| `lineart--dim` | gedämpfte Linie |
| `lineart--marker` | gelbe Markierung |

**Elemente:** `__controls`, `__hint`, `__loading`

**Regeln**

- Labels im Overlay aria-hidden; dieselbe Information als Liste daneben.
- Position relativ zur Bühnenmitte (calc(50% ± px)), nicht absolut in px vom Rand.

**Barrierefreiheit**

- Bühne: role="img" mit aria-label.

**Inhaltsgrenzen:** label: 1–2 Wörter

**Beispiel – Varianten** (weitere in `components.json`, live: `web/index.html#labels3d`)

```html
<span class="odsv-label3d odsv-label3d--static">Bauteil</span>
<span class="odsv-label3d odsv-label3d--static odsv-label3d--strong">Zielposition</span>
<span class="odsv-label3d odsv-label3d--static odsv-label3d--bad">Kollision</span>
<span class="odsv-label3d odsv-label3d--static odsv-label3d--wrong">Falsch</span>
<span class="odsv-cluster odsv-cluster--2"><span aria-hidden="true" class="odsv-marker">1</span><span class="odsv-body-small">Komponente</span></span>
```

<a id="signet"></a>
## Signet und Wortmarke

**Wofür:** Markenmoment (Hero, Titelfolie): Basis- oder Themen-Signet (KI, Netzwerk, Daten, Code, Berge, Fahrrad, Outdoor, Route). Erzählmoment: Situations-Signet (Erfolg, Fail, Konflikt, Einigung, Idee, Frage, In Arbeit, Neustart). Liste: catalog/signets.json.

**Nicht für:** Signet-Verlauf als Button, Text, Diagrammfarbe oder Fläche; mehrere Signet-Varianten auf einer Seite; umgefärbte oder selbst gezeichnete Varianten.

| Klasse/Variante | Bedeutung |
|---|---|
| `<use href="#odsv-signet-THEMA"/>` | Themen: ai, network, data, code, mountains, bike, outdoor, route · Situationen: success, fail, conflict, agreement, idea, question, progress, restart · ohne Suffix = Basis |
| `signet-card--landscape` | Karte 4:3 für Kopfbereiche |
| `signet-mark` | Signet ohne Karte, 48 px (Mindestgröße für Themen-Signets) |
| `signet-arc--1…4` | Bögen (Basis-Signet als Einzelpfade) |
| `signet-arc--draw` | Zeichen-Animation |

**Elemente:** `__svg`

**Regeln**

- Basis/Thema: ein Signet je Produkt/Seite/Präsentation, groß höchstens einmal; Auswahl nach dem Kernthema, im Zweifel Basis.
- Situation: höchstens eins je Ansicht/Folie, nie mit Themen-Signet in derselben Ansicht, nie als Statusanzeige (dafür Callout/Badge).
- Karte: <svg class="odsv-signet-card__svg" viewBox="0 0 400 400" preserveAspectRatio="xMaxYMid slice">.
- Wortmarke unten links in gesperrten Versalien; die Grammatik hält diese Zone frei.
- Immer auf dunklem Grund (auch im hellen Theme in der dunklen Karte).
- Neue Varianten nur über tools/build_signets.py, geprüft mit tools/check_signets.js.

**Barrierefreiheit**

- SVG role="img" mit aria-label, das das Motiv beschreibt.

**Signet-Familie** (`catalog/signets.json`, SPEC 10.6)

| ID | Gruppe | Thema | Bedeutung |
|---|---|---|---|
| `odsv-signet` | Basis | Signal / Wirkung | Standard für alle Themen |
| `odsv-signet-ai` | Technik | KI | Funke: Intelligenz, Generierung, Assistenz |
| `odsv-signet-network` | Technik | Netzwerk | Knoten und Verbindungen: Vernetzung, Plattform, Integration |
| `odsv-signet-data` | Technik | Daten | Steigende Säulen: Analyse, Kennzahlen, Wachstum |
| `odsv-signet-code` | Technik | Code | Klammern und Cursor: Entwicklung, Software, Engineering |
| `odsv-signet-mountains` | Lifestyle | Berge | Gestaffelte Grate und Sonne: Alpin, Wandern, Weitblick |
| `odsv-signet-bike` | Lifestyle | Fahrrad | Räder und Rahmen: Radfahren, Mobilität, Touren |
| `odsv-signet-outdoor` | Lifestyle | Outdoor | Zelt unter der Sonne: Draußen, Camping, Abenteuer |
| `odsv-signet-route` | Lifestyle | Route | Geschwungene Strecke zum Ziel: Training, Tour, Fortschritt |
| `odsv-signet-success` | Situation | Erfolg | Haken erreicht das Ziel, Strahlen feiern: Erfolg, Meilenstein, Abschluss |
| `odsv-signet-fail` | Situation | Fail | Kurve steigt und bricht ein: Misserfolg, Rückschlag, Learnings |
| `odsv-signet-conflict` | Situation | Konflikt | Zwei Pfeile prallen aufeinander: Konflikt, Zielkonflikt, Reibung |
| `odsv-signet-agreement` | Situation | Einigung | Zwei Wege werden einer: Einigung, Lösung, Zusammenarbeit |
| `odsv-signet-idea` | Situation | Idee | Glühbirne mit Strahlen: Idee, Innovation, Vorschlag |
| `odsv-signet-question` | Situation | Frage | Fragezeichen: offene Frage, Unklarheit, Diskussion |
| `odsv-signet-progress` | Situation | In Arbeit | Ring aus Bogenstücken: in Arbeit, läuft, Zwischenstand |
| `odsv-signet-restart` | Situation | Neustart | Kreispfeil: Neustart, Iteration, Wiederholung |

**Inhaltsgrenzen:** wordmark: 1–3 Zeilen à ≤ 20 Zeichen

**Beispiel – Basis-Signet** (weitere in `components.json`, live: `web/index.html#signet`)

```html
<div class="odsv-signet-card" style="max-width:360px">
<svg aria-label="Signet aus vier Bögen und einem gelben Kreis" class="odsv-signet-card__svg" preserveaspectratio="xMaxYMid slice" role="img" viewbox="0 0 400 400"><use href="#odsv-signet"></use></svg>
<p class="odsv-wordmark">Produktname<br/>Untertitel</p>
</div>
```

<a id="list-facts"></a>
## Liste und Fakten

**Wofür:** Aufzählung (Punkte gelb) oder nummerierte Liste; Fakten als <dl>.

**Nicht für:** Mehr als 7 Punkte ohne Gliederung.

| Klasse/Variante | Bedeutung |
|---|---|
| `list--numbered` | nummeriert |
| `facts--cols` | zwei Spalten ab 600 px |

**Regeln**

- Als Karte: zusätzlich .odsv-card an <ul>/<ol>/<dl>.

**Inhaltsgrenzen:** item: ≤ 1 Zeile

**Beispiel – Liste und Fakten** (weitere in `components.json`, live: `web/index.html#weitere`)

```html
<div class="odsv-grid">
<div class="odsv-col-12 odsv-col-md-6"><ul class="odsv-list odsv-card"><li>Keine Installation</li><li>Daten in der EU gespeichert</li><li>Barrierearm nach WCAG 2.2 AA</li></ul></div>
<div class="odsv-col-12 odsv-col-md-6"><ol class="odsv-list odsv-list--numbered odsv-card"><li>Konto anlegen</li><li>Daten importieren</li><li>Team einladen</li></ol></div>
<div class="odsv-col-12"><dl class="odsv-facts odsv-facts--cols odsv-card"><div><dt>Version</dt><dd>1.1.0</dd></div><div><dt>Lizenz</dt><dd>intern</dd></div></dl></div>
</div>
```

<a id="hgroup"></a>
## Headline-Gruppe

**Wofür:** Dreiklang Eyebrow → Headline → Zweitsatz als Block, optional mit Icon-Kachel.

**Nicht für:** Headline ohne Zweitsatz.

| Klasse/Variante | Bedeutung |
|---|---|
| `hgroup--center` | zentriert (Sektionsauftakt) |
| `hgroup--compact` | Dashboard-Seitenkopf |

**Beispiel – Headline-Gruppe (Dreiklang)** (weitere in `components.json`, live: `web/index.html#weitere`)

```html
<header class="odsv-hgroup odsv-hgroup--center">
<span aria-hidden="true" class="odsv-tile odsv-tile--accent"><svg class="odsv-icon"><use href="#odsv-icon-shield"></use></svg></span>
<p class="odsv-eyebrow">Zum Schluss</p>
<h2 class="odsv-h1">Zusammenfassung</h2>
<p class="odsv-sub">Alles Wichtige auf einen Blick.</p>
</header>
```

<a id="toast"></a>
## Toast

**Wofür:** Kurze Bestätigung nach einer Handlung („Stand gespeichert“).

**Nicht für:** Fehler, die eine Handlung erfordern (dafür Callout am Ort).

| Klasse/Variante | Bedeutung |
|---|---|
| `toast--fixed` | am unteren Rand fixiert |

**Regeln**

- Ein- und Ausblenden steuert die Anwendung (odsv.js tut es nicht): nach ca. 4 s ausblenden, nicht während Fokus oder Hover.

**Barrierefreiheit**

- role="status".

**Inhaltsgrenzen:** text: ≤ 40 Zeichen

**Beispiel – Toast** (weitere in `components.json`, live: `web/index.html#weitere`)

```html
<div class="odsv-toast" role="status"><svg aria-hidden="true" class="odsv-icon"><use href="#odsv-icon-check"></use></svg>Stand gespeichert</div>
```

<a id="footer"></a>
## Fußbereich

**Wofür:** Stand, Quellen, Impressum links; Wortmarke rechts.

**Elemente:** `__grid`

**Beispiel – Fußbereich** (weitere in `components.json`, live: `web/index.html#weitere`)

```html
<footer class="odsv-footer"><div class="odsv-footer__grid"><p>Stand 17.11.2026 · <a href="#weitere">Quellen</a> · <a href="#weitere">Impressum</a></p><span class="odsv-wordmark">Produktname</span></div></footer>
```

<a id="utilities"></a>
## Hilfsklassen

**Wofür:** .odsv-sr-only (nur Screenreader), .odsv-mt-0|4|8 (Abstand oben), .odsv-hide-lg, .odsv-no-print, .odsv-reveal (Einblenden beim Scrollen), .odsv-fit-tight (setzt odsv.js).

**Nicht für:** Hilfsklassen statt Komponenten-Modifier.
