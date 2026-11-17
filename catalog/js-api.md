# ODSV 1.0 – JavaScript-API

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

Zeichnet reines SVG in einen Container. Farben und Schrift kommen ausschließlich aus `odsv.css`, über die Klassen `odsv-dv-1…7`, `odsv-dv-highlight`, `odsv-dv-context`, `odsv-dv-neutral`, `odsv-dv-positive` und `odsv-dv-negative`. Die Zeichnung passt sich der Containerbreite an (ResizeObserver) und zeigt bei Hover einen Daten-Tooltip.

```js
ODSVCharts.line(el, {
  labels: ['Jan', 'Feb', …],                      // x-Achse
  series: [{ name: 'Registrierungen', values: [42, 48, …], cls: 'odsv-dv-1', area: true },
           { name: 'Supportanfragen', values: [18, 17, …], cls: 'odsv-dv-2' }],
  height: 240,                                    // px, Standard 240
  yMax: 100, yTicks: 4,                           // optional; sonst nächster runder Wert, 4 Teilstriche
  yFormat: v => v + ' %',                         // optional; Standard deutsches Zahlenformat
  label: 'Registrierungen steigen von 42 auf 97.' // Pflicht: Aussage als Alternativtext (role="img")
});
ODSVCharts.bars(el, { labels, values, colors: ['odsv-dv-context', …, 'odsv-dv-highlight'] /* oder cls */, height, yMax, yTicks, yFormat, label });
ODSVCharts.donut(el, { items: [{ label, value, cls }], size: 200, center: { value: '62 %', label: 'fertig' }, label });
ODSVCharts.spark(el, values, 'odsv-dv-1');       // Sparkline ohne Achsen, letzter Punkt markiert
ODSVCharts.redraw();                              // alle neu zeichnen (z. B. nach Theme-Wechsel)
ODSVCharts.format(1234.5)                         // "1.234,5"
```

**Regeln**
- `el` ist `.odsv-chart__plot` innerhalb einer `<figure class="odsv-chart">` mit Titel, Legende und Quelle. Die Legende ist HTML, nicht SVG.
- Reihenfarben in fester Reihenfolge `dv-1`, `dv-2`, … Für das Fokus-Muster `dv-highlight` plus `dv-context`.
- Balken beginnen immer bei 0. `yMax` nur setzen, wenn mehrere Diagramme vergleichbar sein müssen.
- Der Donut hat höchstens 4 Segmente, „Offen“ oder „Sonstige“ in `odsv-dv-neutral`.
