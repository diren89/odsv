# ODSV v1.1 – Web-Umsetzung

Dunkles Design-System (gesperrte Versalien, gelber Akzent, dunkle Karten mit großen Radien, segmentierte Fortschrittsleiste, Verlaufs-Signet). Werte stammen ausschließlich aus `tokens/tokens.css`; Regeln aus `SPEC.md`.

## Dateien

| Datei | Zweck |
|---|---|
| `tokens.css` | Kopie von `../tokens/tokens.css` (erzeugt, nicht ändern; mit `node tools/build-web.js` aktualisieren) |
| `odsv.css` | Komponentenbibliothek, Präfix `.odsv-`, nur `var(--odsv-…)` |
| `odsv.js` | optionales Verhalten (Theme, Segment, Tabs, Checkliste, Scroll-Fortschritt, Menü, Sheet, Kopieren) |
| `odsv-charts.js` | optional: 14 Diagrammformen als SVG (Linie, Säulen gruppiert/gestapelt, Balken, Abweichung, Trichter, Histogramm, Boxplot, Streudiagramm, Heatmap, Steigung, kleine Vielfache, Donut, Sparkline) mit Tastatur, Tabellenansicht und Legenden-Schalter; Optionen in `../catalog/charts.json` |
| `icons.svg` | Sprite, 33 Line-Art-Icons + Signet (`#odsv-icon-…`, `#odsv-signet`) |
| `index.html` | Referenzseite (`docs.css`, `docs.js` gehören nur dazu) |
| `examples/website.html`, `examples/dashboard.html` | Beispiele |

## Einbindung

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="odsv.css">
<script src="odsv.js"></script>           <!-- im head, ohne defer: Theme ohne Flackern -->
<script src="odsv-charts.js" defer></script>
```

Icons: Inhalt von `icons.svg` als Inline-Sprite in den `body` kopieren (`tools/build-web.js` tut das zwischen `<!--ODSV-SPRITE-->`-Markern). Dann:
`<svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-check"/></svg>`.
Über `file://` blockiert der Browser externe `<use href="icons.svg#…">`; über HTTP geht beides.

Theme: `data-theme="light"` an `html` (oder an einem Teilbereich). Dunkel ist Standard, Druck schaltet automatisch auf Hell. Dichte: `data-density="comfortable|compact|dense"` am `body`.

## Klassenübersicht

Vollständig mit Zweck, Varianten, Regeln und Referenz-Markup: `../catalog/COMPONENTS.md` (maschinenlesbar `../catalog/components.json`, Whitelist `../catalog/classes.json`). JS- und Diagramm-API: `../catalog/js-api.md`.


- **Base/Typo:** `odsv-eyebrow`, `-label`, `-display`, `-h1…h4`, `-sub`, `-body`, `-body-small`, `-small`, `-caption`, `-mono`, `-number`, `-muted`, `-accent`
- **Layout:** `odsv-container(--wide|--text)`, `-section`, `-section-head`, `-grid` + `-col-N` / `-col-sm|md|lg|xl-N`, `-stack(--1…12)`, `-cluster(--between|--center)`, `-hgroup`
- **Button/Link:** `odsv-btn` + `--primary|--secondary|--ghost|--danger`, `--md|--sm|--icon|--block`, `is-loading`; `odsv-icon-btn`, `odsv-link(--muted|--plain)`, `odsv-textbtn`
- **Karten:** `odsv-card` + `--level-0|2|3|inset|stage|outline|accent|active|success|warning|danger|compact|interactive`; `odsv-kpi` (`__label|__value|__unit|__note|__row`, `--lg|--lead`), `odsv-trend--positive|negative|neutral`, `odsv-specs`/`odsv-spec`, `odsv-step` (`__num|__media|__title|__text|__skip`, `--active|--inactive`)
- **Fortschritt/Auswahl:** `odsv-progress` (`__seg|__link|__bar|__meta`, `--dashed|--success|--thick`), `odsv-segmented` (`__item`, `--inverse|--sm|--block`), `odsv-checklist`, `odsv-check`, `odsv-checkbox`, `odsv-radio`, `odsv-switch`, `odsv-accordion` (`--card`)
- **Daten:** `odsv-table-wrap`, `odsv-table` (`--compact|--dense|--hover|--sticky`, `__num`), `odsv-chart` (`__header|__title|__subtitle|__tools|__plot|__table|__multiples|__footer|__tip`), `odsv-legend`, `odsv-swatch`, `odsv-dv-1…7|neutral|context|highlight|positive|negative`, `odsv-dv-seq-1…6`, `odsv-dv-div-neg|div-pos` (Stufen, `div-mid`), `odsv-axis-text`, `odsv-grid-line`, `odsv-data-line|bar|area|slice|point|cell|bubble|whisker|box|outlier|trend|ref|event|pill|band|focus`, `odsv-stackbar`
- **Rückmeldung:** `odsv-callout` (`__head|__label|__title|__text`, `--info|success|warning|danger|banner`), `odsv-badge` (`--accent|success|warning|danger|info|solid|count`), `odsv-pill`, `odsv-toast`, `odsv-empty`, `odsv-skeleton`, `odsv-spinner`
- **Formulare:** `odsv-field` (`__label|__hint|__error|__opt`, `is-invalid`), `odsv-input`, `odsv-select` + `__control|__icon`, `odsv-textarea`, `odsv-search`, `odsv-option`, `odsv-fieldset`
- **Navigation/Überlagerung:** `odsv-topbar` (`__inner|__nav|__actions|__toggle|__progress|__meta`), `odsv-brand`, `odsv-nav`, `odsv-sidebar`, `odsv-app`, `odsv-tabs`/`odsv-tab`/`odsv-tabpanel`, `odsv-tooltip` (`__content`, `--start|--end|--below`), `odsv-sheet` (`__panel|__grabber|__title|__text|__actions`, `--inline|--sticky`)
- **Illustration:** `odsv-tile` (`--accent|--lg|--xl|--sm`), `odsv-signet-card`, `odsv-wordmark`, `odsv-stage`, `odsv-label3d` (`--strong|bad|wrong|static`), `odsv-marker`, `odsv-lineart`, `odsv-leader`
- **Weitere:** `odsv-list`, `odsv-facts`, `odsv-footer`, `odsv-skip`, `odsv-sr-only`, `odsv-reveal`

## Verhalten (`odsv.js`)

`data-odsv-theme-toggle` · `data-odsv-segmented` · `data-odsv-tabs` · `data-odsv-checklist="schlüssel"` (+ `-count`, `-progress`, `-reset`) · `data-odsv-scrollprogress` (+ `data-odsv-scrollprogress-label`) · `data-odsv-nav-toggle` · `data-odsv-sheet-open="#id"` / `data-odsv-sheet-close` · `data-odsv-copy="#id"`. Diagramme (`odsv-charts.js`): `data-odsv-chart-table` (Tabellenansicht), `data-odsv-series` (Legende als Schalter). Nachträglich eingefügtes Markup: `ODSV.init(element)`. Änderungen melden `odsv:change` (Segment, Tabs) und `odsv:theme`.

## Regeln

1. Keine Hex-, rgb- oder hsl-Werte in `odsv.css`; jede `var(--odsv-…)` muss in `tokens.css` existieren. Prüfen: `node tools/check-css.js`.
2. Private Hilfsvariablen heißen `--p` oder `--_x` (kein `odsv`-Präfix, nur lokal).
3. Ein gelber Primär-Button je Ansicht; Gelb nie als Dekor; Status immer mit Icon und Wort.
4. Versalien nur per Stil, nie getippt; nie für Fließtext, Warnungen, Fehler.
5. Warnungen stehen in voller Länge vor dem Schritt, nie im Akkordeon.
6. Breakpoints (Media Queries können kein `var()`): 600 / 768 / 1024 / 1280 px.

## Prüfen

`bash tools/validate.sh` (alles) · `node tools/lint-html.js seite.html` (ODSV-Regeln für eigene Seiten) · `node tools/audit.js` (Playwright: Kontrast, Trefferflächen, Token-Treue, Screenshots nach `web/_audit/`) · `node tools/func-test.js`.
