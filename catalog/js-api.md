# ODSV 1.1 – JavaScript-API

`odsv.css` gestaltet vollständig ohne JavaScript. Die beiden Skripte sind optional und brauchen keine Bibliothek.

## odsv.js – Verhalten

Einbindung **im `<head>` ohne `defer`**. So wird das gespeicherte Theme vor dem ersten Zeichnen gesetzt. Alle Hooks werden beim Laden einmal initialisiert. Für Inhalte, die später eingefügt werden: `ODSV.init(container)`.

| Attribut | Wirkung | Erwartete Struktur |
|---|---|---|
| `data-odsv-theme-toggle` | Schaltet dunkel/hell und speichert in `localStorage["odsv-theme"]`. Event `odsv:theme` auf `document` (`detail.theme`). | `<button aria-label="Theme wechseln">` |
| `data-odsv-segmented` | Segment-Umschalter: Klick, Pfeiltasten, Pos1/Ende. Setzt `aria-checked` und `tabindex`. Event `odsv:change` (`detail.value` = `data-value` des Items). | Container `role="radiogroup" aria-label`, Kinder `<button role="radio" aria-checked data-value>` |
| `data-odsv-tabs` | Tabs: Pfeiltasten, Pos1/Ende. Blendet Panels über `aria-controls` ein und aus. Event `odsv:change`. | `role="tablist"` mit `<button role="tab" aria-selected aria-controls>`, Panels `role="tabpanel" aria-labelledby` |
| `data-odsv-checklist="schlüssel"` | Speichert den Stand unter `localStorage["odsv-checklist:schlüssel"]`. Fehler beim Speichern werden still ignoriert. | Checkboxen mit `data-id`; optional `[data-odsv-checklist-count]` (Text „n von m“), `[data-odsv-checklist-progress]` (leere `<ol class="odsv-progress odsv-progress--dashed">`, wird befüllt), `[data-odsv-checklist-reset]` (Button) |
| `data-odsv-scrollprogress` | Kapitelleiste folgt dem Scroll: setzt `--p` je Segment und `aria-current="step"` am aktiven Link. | `<ol class="odsv-progress">` mit Links `href="#kapitel-id" aria-label`; optional ein Element `[data-odsv-scrollprogress-label]`, das den Kapitelnamen anzeigt (`data-title` oder `aria-label` des Links) |
| `data-odsv-nav-toggle` | Mobiles Menü der Top-Bar: `is-open` an `.odsv-topbar`, `aria-expanded`. Escape schließt, Klick auf einen Link schließt. | Button innerhalb `.odsv-topbar` |
| `data-odsv-sheet-open="#id"` / `data-odsv-sheet-close` | Bottom-Sheet als Dialog: Fokus geht hinein und bleibt dort, Escape schließt, Fokus kehrt zum Auslöser zurück. | `<div class="odsv-sheet" id role="dialog" aria-modal="true" aria-labelledby hidden>` mit `.odsv-sheet__backdrop[data-odsv-sheet-close]` |
| `data-odsv-copy="#id"` | Kopiert den Text des Ziels in die Zwischenablage; der Button zeigt 1,6 s lang „Kopiert“. | `<button data-odsv-copy="#code">` |
| `data-odsv-fit` | Wendet `ODSV.fit` auch auf Elemente an, die keine Headline-Klasse tragen. | beliebiges Textelement |
| Tooltips | `.odsv-tooltip`: Escape schließt (`is-dismissed`), Hover oder Fokus öffnet wieder. | siehe Komponentenkatalog |

**Globale API**

```js
ODSV.version                // "1.0.0"
ODSV.setTheme('light')      // 'dark' | 'light', speichert die Wahl
ODSV.init(container)        // Hooks und fit für nachträglich eingefügtes HTML
ODSV.fit(container?)        // lange Versalien-Wörter einpassen (läuft automatisch bei Laden, Resize, fonts.ready)
```

`ODSV.fit` wirkt auf `.odsv-display`, `.odsv-h1`, `.odsv-h2` und `[data-odsv-fit]`. Passt das längste Wort nicht in die Breite, setzt es zuerst `.odsv-fit-tight` (Laufweite 0,12 em) und verkleinert dann die Schrift auf höchstens 72 %. Steht im Text ein `&shy;`, greift es nicht ein.

## odsv-charts.js – Diagramme

Zeichnet reines SVG in einen Container. Farben und Schrift kommen ausschließlich aus `odsv.css`: Zugehörigkeit `odsv-dv-1…7`, Betonung `odsv-dv-highlight` + `odsv-dv-context`, Sonstige `odsv-dv-neutral`, Status `odsv-dv-positive|negative`, Menge `odsv-dv-seq-1…6`, Richtung `odsv-dv-div-neg|div-pos` (Stufen `-3 … 3`, Mitte `div-mid`). Die Zeichnung passt sich der Containerbreite an (ResizeObserver).

**Gemeinsam für alle Formen**
- `label` ist Pflicht: die Aussage mit den wichtigsten Zahlen, wird zum `aria-label` (`role="img"`).
- Tastatur: Tab fokussiert die Zeichnung, Pfeiltasten/Pos1/Ende wandern, Esc schließt den Tooltip; eine `aria-live`-Region sagt den Wert an (außer `multiples`, `donut`, `spark`).
- Tabellenansicht: ein Button `[data-odsv-chart-table]` in derselben `.odsv-chart` blendet die Daten als `.odsv-table` unter der Zeichnung ein (`aria-expanded`, Beschriftung im Kind `[data-odsv-label]`).
- Legende als Schalter: `button.odsv-legend__item[data-odsv-series="Name"][aria-pressed="true"]` blendet die Reihe mit diesem `name` aus und ein (`line`, `columns`, `scatter`, `slope` über `label`). Die letzte sichtbare Reihe bleibt.
- Formatierung: `yFormat`/`xFormat`/`format` erhalten eine Zahl und geben Text zurück; Standard ist `ODSVCharts.format` (deutsch, echtes Minuszeichen).

```js
// Verlauf
ODSVCharts.line(el, {
  labels: ['Jan', 'Feb', …],
  series: [{ name: 'Web', values: [62, 64, …], cls: 'odsv-dv-1', area: false, dash: false }, …], // null = Lücke
  unit: 'Tsd. €',                                  // einmal oben an der Achse
  annotations: [{ at: 6, label: 'Relaunch' }],     // Ereignis: Index in labels
  target: { value: 95, label: 'Ziel 95' },         // Zielwert, gestrichelt
  endLabels: true,                                 // Reihen am Linienende beschriften (bis 4)
  height: 240, yMin, yMax, yTicks: 4, yFormat, label
});
ODSVCharts.bars(el, { labels, values, colors: [...] | cls, unit, height, yMax, yTicks, yFormat, label });

// Mehrere Reihen je Kategorie
ODSVCharts.columns(el, { labels, series: [{ name, values, cls }], mode: 'grouped' | 'stacked' | 'percent', unit, height, yMax, yFormat, valueFormat, label });

// Kategorien, Abweichung, Trichter (waagrecht)
ODSVCharts.hbars(el, { labels, values, colors | cls, sort: true /* absteigend */, unit, format, axisFormat, labelWidth, label });
ODSVCharts.diverging(el, { labels, values, negLabel: 'unter Plan', posLabel: 'über Plan', sort: false, format, label });  // Werte mit Vorzeichen
ODSVCharts.funnel(el, { steps: [{ label: 'Besuch', value: 48200 }, …], format, label });                              // Wert · Quote zum Vorschritt

// Verteilung
ODSVCharts.histogram(el, { values: [...], binWidth | bins: 10, mark: 'median' | 'mean', unit: 'Anzahl', xFormat, cls, height, label });
ODSVCharts.boxplot(el, { groups: [{ label: 'Team A', values: [...], cls }], format, unit, min, max, label });         // Spanne bis 1,5 × IQR, Ausreißer als Ringe
ODSVCharts.stats([...])                           // { n, min, q1, med, q3, max, out[] } – dieselbe Rechnung wie boxplot

// Zusammenhang
ODSVCharts.scatter(el, {
  series: [{ name: 'Online', cls: 'odsv-dv-2', points: [{ x, y, r /* optional: Blasengröße */, label, highlight }] }],
  xLabel: 'Budget, Tsd. €', yLabel: 'Leads', sizeName: 'Umsatz', trend: true /* lineare Regression mit R² */,
  xZero, yZero, xMin, xMax, yMin, yMax, xFormat, yFormat, height, label
});

// Zwei Dimensionen, zwei Zeitpunkte, viele Reihen
ODSVCharts.heatmap(el, { rows: ['Mo', …], cols: ['7', …], values: [[43, 56, …], …] /* null = leer */, min, max, scaleTitle, showValues: true, cellHeight: 30, format, label });
ODSVCharts.slope(el, { from: '2025', to: '2026', items: [{ label: 'Hamburg', a: 68, b: 81, cls: 'odsv-dv-highlight' }, …], format, min, max, zero, label });
ODSVCharts.multiples(el, { labels, series: [{ name, values, cls }], columns, height: 120, context: true, yMax, yFormat, label });

ODSVCharts.donut(el, { items: [{ label, value, cls }], size: 200, center: { value: '62 %', label: 'fertig' }, label });
ODSVCharts.spark(el, values, 'odsv-dv-1');       // Sparkline ohne Achsen, letzter Punkt markiert; el mit data-odsv-spark, damit redraw() sie mitzeichnet
ODSVCharts.redraw();                              // alle neu zeichnen (läuft bei odsv:theme automatisch)
ODSVCharts.format(-1234.5)                        // "−1.234,5"
```

**Markup**

```html
<figure class="odsv-chart">
  <div class="odsv-chart__header">
    <div><p class="odsv-eyebrow">Umsatz</p><figcaption class="odsv-chart__title">Aussage als Titel</figcaption><p class="odsv-chart__subtitle">Einheit, Bezug</p></div>
    <div class="odsv-chart__tools"><button class="odsv-btn odsv-btn--ghost odsv-btn--sm" type="button" data-odsv-chart-table aria-expanded="false"><span data-odsv-label>Daten als Tabelle</span></button></div>
  </div>
  <ul class="odsv-legend" aria-label="Reihen ein- und ausblenden">
    <li><button class="odsv-legend__item" type="button" aria-pressed="true" data-odsv-series="Web"><span class="odsv-swatch odsv-swatch--line odsv-dv-1"></span>Web</button></li>
  </ul>
  <div class="odsv-chart__plot"></div>
  <p class="odsv-chart__footer">Quelle: … · Stand …</p>
</figure>
```

**Regeln**
- `el` ist `.odsv-chart__plot` innerhalb einer `<figure class="odsv-chart">` mit Titel, Legende und Quelle. Die Legende ist HTML, nicht SVG.
- Form nach Aufgabe der Daten wählen (SPEC 7.3). Reihenfarben in fester Reihenfolge `dv-1`, `dv-2`, … Für das Fokus-Muster `dv-highlight` plus `dv-context`.
- Balken und Säulen beginnen immer bei 0. `yMax` nur setzen, wenn mehrere Diagramme vergleichbar sein müssen.
- Streudiagramm dunkel höchstens 5, hell höchstens 3 Farben. Heatmap nur in `dv-seq`, Abweichung nur in `dv-div`.
- Der Donut hat höchstens 3 Teile, „Offen“ oder „Sonstige“ in `odsv-dv-neutral`.
- Sparkline-Container tragen `data-odsv-spark` (und eine Höhe, z. B. 32 px): `ODSVCharts.redraw()` zeichnet nur `.odsv-chart__plot` und `[data-odsv-spark]` neu.
- Daten gelangen als Text ins SVG und in die Tabelle (`textContent`); Tooltip-Inhalte werden maskiert.
