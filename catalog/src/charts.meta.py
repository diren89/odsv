# Quelle für catalog/charts.json – Diagrammformen von web/odsv-charts.js für Agents.
# Je Form: Aufgabe der Daten (SPEC 7.3), wann/nicht, Funktion, Optionen (Typ, Pflicht, Standard, Bedeutung), Grenzen, Beispiel.
# Nach Änderungen: python3 tools/build_catalog.py (prüft, dass jede exportierte Funktion beschrieben ist).
# Optionstypen: string, number, boolean, function (Zahl → Text), array<…>, object, enum(a|b)

COMMON = {
    "label": dict(type="string", required=True, desc="Aussage mit den wichtigsten Zahlen; wird zum aria-label (role=\"img\")."),
}
FMT = dict(type="function", desc="Zahl → Text; Standard ODSVCharts.format (deutsch, echtes Minus).")

CHARTS = {
  "line": dict(
    task="Verlauf über Zeit", use="bis 4 Reihen über eine Zeitachse; Ereignis, Zielwert, Endbeschriftung", avoid="Säulen für lange Zeitreihen; mehr als 4 Reihen (→ multiples)",
    options={"labels": dict(type="array<string>", required=True, desc="x-Achse, z. B. Monate"),
             "series": dict(type="array<{name:string, values:array<number|null>, cls?:string, area?:boolean, dash?:boolean}>", required=True, desc="null = Lücke; Fläche nur bei einer Reihe"),
             "unit": dict(type="string", desc="Einheit einmal oben an der Achse"),
             "annotations": dict(type="array<{at:number, label:string}>", desc="Ereignis: Index in labels"),
             "target": dict(type="{value:number, label?:string}", desc="Zielwert, gestrichelt"),
             "endLabels": dict(type="boolean", default=False, desc="Reihen am Linienende beschriften"),
             "height": dict(type="number", default=240), "yMin": dict(type="number"), "yMax": dict(type="number"), "yTicks": dict(type="number", default=4), "yFormat": FMT},
    limits={"series": 4, "labels": 36}, keyboard=True, table=True, legend_toggle=True,
    example="ODSVCharts.line(el, { labels: ['Jan','Feb','Mär'], series: [{ name: 'Web', values: [62, 64, 71], cls: 'odsv-dv-1' }], unit: 'Tsd. €', label: 'Web steigt von 62 auf 71 Tausend Euro.' })"),
  "bars": dict(
    task="Vergleich über wenige Zeitpunkte", use="eine Reihe, bis 12 Säulen; Fokus-Muster dv-highlight + dv-context", avoid="lange Zeitreihen; Kategorien mit langen Namen (→ hbars)",
    options={"labels": dict(type="array<string>", required=True), "values": dict(type="array<number>", required=True),
             "colors": dict(type="array<string>", desc="Klasse je Säule"), "cls": dict(type="string", default="odsv-dv-1"),
             "unit": dict(type="string"), "height": dict(type="number", default=240), "yMax": dict(type="number"), "yTicks": dict(type="number", default=4), "yFormat": FMT},
    limits={"labels": 12}, keyboard=False, table=True, legend_toggle=False,
    example="ODSVCharts.bars(el, { labels: ['Q1','Q2','Q3','Q4'], values: [145,184,224,277], colors: ['odsv-dv-context','odsv-dv-context','odsv-dv-context','odsv-dv-highlight'], label: 'Q4 ist mit 277 am höchsten.' })"),
  "columns": dict(
    task="Teile und Summe / Vergleich mehrerer Reihen über wenige Zeitpunkte", use="mode grouped (Teile vergleichen), stacked (Summe und Teile), percent (Anteile)", avoid="mehr als 4 Teile je Säule; lange Zeitreihen",
    options={"labels": dict(type="array<string>", required=True), "series": dict(type="array<{name:string, values:array<number>, cls:string}>", required=True),
             "mode": dict(type="enum(grouped|stacked|percent)", default="grouped"), "unit": dict(type="string"), "height": dict(type="number", default=260),
             "yMax": dict(type="number"), "yFormat": FMT, "valueFormat": FMT},
    limits={"series": 4, "labels": 12}, keyboard=True, table=True, legend_toggle=True,
    example="ODSVCharts.columns(el, { labels: ['Q1','Q2'], mode: 'stacked', series: [{ name: 'Bestand', values: [120,124], cls: 'odsv-dv-2' }, { name: 'Neukunden', values: [24,38], cls: 'odsv-dv-1' }], label: 'Neukunden wachsen von 24 auf 38.' })"),
  "hbars": dict(
    task="Vergleich von Kategorien", use="waagrecht, absteigend sortiert; eine Kategorie betont", avoid="Kreis; senkrechte Säulen mit schrägen Beschriftungen",
    options={"labels": dict(type="array<string>", required=True), "values": dict(type="array<number>", required=True), "colors": dict(type="array<string>"), "cls": dict(type="string", default="odsv-dv-1"),
             "sort": dict(type="boolean", default=True, desc="absteigend"), "unit": dict(type="string"), "format": FMT, "axisFormat": FMT, "labelWidth": dict(type="number")},
    limits={"labels": 12}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.hbars(el, { labels: ['Berlin','Hamburg'], values: [1840,1120], colors: ['odsv-dv-highlight','odsv-dv-context'], label: 'Berlin führt mit 1.840 Bestellungen.' })"),
  "diverging": dict(
    task="Abweichung von Ziel oder Null", use="Balken ab Nulllinie, negativ dv-div-neg, positiv dv-div-pos, Werte mit Vorzeichen", avoid="Rot/Grün ohne Vorzeichen",
    options={"labels": dict(type="array<string>", required=True), "values": dict(type="array<number>", required=True),
             "negLabel": dict(type="string", desc="z. B. „unter Plan“"), "posLabel": dict(type="string"), "sort": dict(type="boolean", default=False), "format": FMT, "axisFormat": FMT},
    limits={"labels": 12}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.diverging(el, { labels: ['Vertrieb','Technik'], values: [8.5,-6.1], negLabel: 'unter Plan', posLabel: 'über Plan', label: 'Vertrieb liegt 8,5 Punkte über Plan, Technik 6,1 darunter.' })"),
  "funnel": dict(
    task="Ablauf / Trichter", use="abgestufte Einzelfarbe dv-seq; Wert und Quote zum Vorschritt", avoid="bunte Stufen",
    options={"steps": dict(type="array<{label:string, value:number}>", required=True), "format": FMT, "unit": dict(type="string"), "name": dict(type="string", desc="Spaltenkopf der Tabelle")},
    limits={"steps": 7}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.funnel(el, { steps: [{ label: 'Besuch', value: 48200 }, { label: 'Kauf', value: 3100 }], label: 'Von 48.200 Besuchen kaufen 3.100.' })"),
  "histogram": dict(
    task="Verteilung einer Größe", use="Klassen gleicher Breite; Median oder Mittelwert markieren; n im Zweitsatz", avoid="zu wenige Werte (unter ca. 30)",
    options={"values": dict(type="array<number>", required=True), "binWidth": dict(type="number", desc="Klassenbreite; sonst aus bins"), "bins": dict(type="number", default=10),
             "mark": dict(type="enum(median|mean)"), "unit": dict(type="string", default="Anzahl"), "xFormat": FMT, "cls": dict(type="string", default="odsv-dv-2"), "height": dict(type="number", default=220)},
    limits={"bins": 30}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.histogram(el, { values: zeiten, binWidth: 0.5, mark: 'median', xFormat: v => ODSVCharts.format(v) + ' h', label: 'Die meisten Tickets sind nach 1 bis 2 Stunden gelöst.' })"),
  "boxplot": dict(
    task="Verteilung je Gruppe vergleichen", use="Strich = Spanne bis 1,5 × IQR, dicker Strich = mittlere Hälfte, Punkt = Median, Ringe = Ausreißer", avoid="Gruppen mit sehr wenigen Werten (Punkte zeigen)",
    options={"groups": dict(type="array<{label:string, values:array<number>, cls?:string}>", required=True), "format": FMT, "unit": dict(type="string"), "min": dict(type="number"), "max": dict(type="number")},
    limits={"groups": 10}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.boxplot(el, { groups: [{ label: 'Team A', values: a }, { label: 'Team B', values: b, cls: 'odsv-dv-highlight' }], label: 'Team B streut am stärksten.' })"),
  "scatter": dict(
    task="Zusammenhang zweier Größen", use="Punkte oder Blasen (r = dritte Größe); Trendlinie mit R²", avoid="mehr als 5 Farben (hell 3); Trendlinie bei wenigen Punkten",
    options={"series": dict(type="array<{name:string, cls:string, points:array<{x:number, y:number, r?:number, label?:string, highlight?:boolean}>}>", required=True),
             "xLabel": dict(type="string"), "yLabel": dict(type="string"), "sizeName": dict(type="string", desc="Name der Blasengröße"), "trend": dict(type="boolean", default=False),
             "xZero": dict(type="boolean", default=False), "yZero": dict(type="boolean", default=False), "xMin": dict(type="number"), "xMax": dict(type="number"), "yMin": dict(type="number"), "yMax": dict(type="number"),
             "xFormat": FMT, "yFormat": FMT, "height": dict(type="number", default=300)},
    limits={"series": 5, "series_light": 3, "points": 500}, keyboard=True, table=True, legend_toggle=True,
    example="ODSVCharts.scatter(el, { series: [{ name: 'Online', cls: 'odsv-dv-2', points: [{ x: 10, y: 52 }, { x: 25, y: 81 }] }], xLabel: 'Budget, Tsd. €', yLabel: 'Leads', trend: true, label: 'Mehr Budget bringt mehr Leads.' })"),
  "heatmap": dict(
    task="Größe über zwei Dimensionen", use="6 Stufen dv-seq mit Skala; leere Zelle = null", avoid="Regenbogen; divergierende Daten ohne Mittelwert",
    options={"rows": dict(type="array<string>", required=True), "cols": dict(type="array<string>", required=True), "values": dict(type="array<array<number|null>>", required=True, desc="Zeilen × Spalten"),
             "min": dict(type="number"), "max": dict(type="number"), "scaleTitle": dict(type="string"), "showValues": dict(type="boolean", default=True, desc="Zahl in der Zelle ab 40 px Zellbreite"),
             "cellHeight": dict(type="number", default=30), "format": FMT},
    limits={"cols": 24, "rows": 20}, keyboard=True, table=True, legend_toggle=False,
    example="ODSVCharts.heatmap(el, { rows: ['Mo','Di'], cols: ['9','10'], values: [[83,101],[80,98]], scaleTitle: 'Anfragen je Stunde', label: 'Spitze montags um 10 Uhr mit 101 Anfragen.' })"),
  "slope": dict(
    task="Rang oder Wert an zwei Zeitpunkten", use="eine Reihe betont (cls), Rest Kontext", avoid="mehr als zwei Zeitpunkte (→ line)",
    options={"from": dict(type="string", required=True), "to": dict(type="string", required=True), "items": dict(type="array<{label:string, a:number, b:number, cls?:string}>", required=True),
             "format": FMT, "min": dict(type="number"), "max": dict(type="number"), "zero": dict(type="boolean", default=False), "height": dict(type="number")},
    limits={"items": 12}, keyboard=True, table=True, legend_toggle=True,
    example="ODSVCharts.slope(el, { from: '2025', to: '2026', items: [{ label: 'Hamburg', a: 68, b: 81, cls: 'odsv-dv-highlight' }, { label: 'Berlin', a: 74, b: 76 }], label: 'Hamburg steigt von 68 auf 81.' })"),
  "multiples": dict(
    task="viele Reihen", use="kleine Vielfache mit gleicher Achse; übrige Reihen als Kontext", avoid="eine Linie je Farbe ab der 8. Reihe",
    options={"labels": dict(type="array<string>", required=True), "series": dict(type="array<{name:string, values:array<number>, cls?:string}>", required=True),
             "columns": dict(type="number", desc="sonst nach Breite"), "height": dict(type="number", default=120), "context": dict(type="boolean", default=True), "yMax": dict(type="number"), "yFormat": FMT, "cls": dict(type="string", default="odsv-dv-highlight")},
    limits={"series": 12}, keyboard=False, table=True, legend_toggle=False,
    example="ODSVCharts.multiples(el, { labels: monate, series: regionen, columns: 2, label: 'Nur Region Ost wächst durchgehend.' })"),
  "donut": dict(
    task="Anteile an einem Ganzen (wenige Teile)", use="bis 3 Teile, „Offen“/„Sonstige“ in dv-neutral, Wert in der Mitte", avoid="mehr als 3 Teile (→ hbars oder .odsv-stackbar)",
    options={"items": dict(type="array<{label:string, value:number, cls:string}>", required=True), "size": dict(type="number", default=200), "center": dict(type="{value:string, label:string}")},
    limits={"items": 3}, keyboard=False, table=True, legend_toggle=False,
    example="ODSVCharts.donut(el, { items: [{ label: 'Fertig', value: 62, cls: 'odsv-dv-1' }, { label: 'Offen', value: 38, cls: 'odsv-dv-neutral' }], center: { value: '62 %', label: 'fertig' }, label: '62 Prozent sind fertig.' })"),
  "spark": dict(
    task="Verlauf ohne Details (in KPI-Kachel)", use="Linie 4:1 ohne Achsen, letzter Punkt markiert; Aufruf ODSVCharts.spark(el, values, cls)", avoid="als alleinige Datenquelle (Wert steht daneben)",
    options={"values": dict(type="array<number>", required=True, desc="2. Argument"), "cls": dict(type="string", default="odsv-dv-1", desc="3. Argument")},
    limits={"values": 60}, keyboard=False, table=False, legend_toggle=False, decorative=True,
    example="ODSVCharts.spark(el, [3, 5, 4, 7], 'odsv-dv-1')"),
}
HELPERS = {
  "redraw": "alle Diagramme neu zeichnen; läuft bei odsv:theme automatisch",
  "format": "Zahl → deutscher Text mit echtem Minuszeichen, z. B. −1.234,5",
  "stats": "Fünf-Punkte-Zusammenfassung {n, min, q1, med, q3, max, out[]} wie im boxplot",
}
MARKUP = {
  "figure": "<figure class=\"odsv-chart\"> → .odsv-chart__header (Eyebrow, <figcaption class=\"odsv-chart__title\">, .odsv-chart__subtitle, .odsv-chart__tools) → .odsv-legend → .odsv-chart__plot → .odsv-chart__footer",
  "table_button": "<button class=\"odsv-btn odsv-btn--ghost odsv-btn--sm\" type=\"button\" data-odsv-chart-table aria-expanded=\"false\"><span data-odsv-label>Daten als Tabelle</span></button>",
  "legend_toggle": "<li><button class=\"odsv-legend__item\" type=\"button\" aria-pressed=\"true\" data-odsv-series=\"Name\"><span class=\"odsv-swatch odsv-swatch--line odsv-dv-1\"></span>Name</button></li>",
  "palettes": {"Zugehörigkeit": "odsv-dv-1…7", "Betonung": "odsv-dv-highlight + odsv-dv-context", "Sonstige": "odsv-dv-neutral", "Status": "odsv-dv-positive|negative", "Menge": "odsv-dv-seq-1…6", "Richtung": "odsv-dv-div-neg|div-pos (Stufen -3 … 3, div-mid)"},
}
