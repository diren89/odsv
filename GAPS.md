# ODSV – Lückenanalyse

Stand 17.11.2026 · bezogen auf ODSV v1.0.0

Frage: Was fehlte dem Ausgangsstil – einer einzelnen, scrollbasierten Produktseite –, um als System für **Websites, Dashboards und Präsentationen** zu taugen, und wie schließt ODSV die Lücke?

Der Ausgangsstil war für **eine** Seite gebaut: ein Thema, ein dunkles Theme, eine lineare Geschichte, kaum Eingaben, keine Daten im Zeitverlauf. Er ist in sich stimmig. Die Lücken entstehen erst durch die neuen Medien.

Legende: **geschlossen** = Token und Regel vorhanden · **teilweise** = Regel vorhanden, Umsetzung fehlt · **offen** = bewusst nicht in v1.0.

---

## 1. Fehler im bisherigen Stil (korrigiert)

Diese Punkte waren schon im Ausgangsstil Schwächen. Alle Zahlen nachgerechnet mit `tools/check_tokens.py`.

| # | Befund | Messwert | Lösung in ODSV | Verweis |
|---|---|---|---|---|
| 1.1 | **Fußnotengrau zu schwach.** `--ink-40` (Weiß 45 %) wurde für Fußnoten und den Grabber genutzt. | 4,43:1 auf Schwarz, 3,59:1 auf Karte – unter 4,5:1 | Neue Stufe `color.text.faint` #8E8E93: 6,44 / 5,22 / 4,81:1 auf Grund / Karte 1 / Karte 2. Die alte Stufe lebt nur als `color.text.disabled` weiter. | SPEC 3.3 |
| 1.2 | **Transparente Textfarben.** Weiß mit 90/80/62/45 % ergibt je Untergrund andere Farben; in PowerPoint, Diagramm-Bibliotheken und im Druck nicht verlässlich. | – | Deckende Stufen `color.text.primary … faint`. | `color.text.*` |
| 1.3 | **Kartenrand trägt nicht.** Rand #2C2C2E und Karte #1C1C1E heben sich kaum vom Grund ab. | Rand 1,51:1, Karte 1,23:1 gegen Schwarz | Als Dekor erklärt und geregelt: Eine Karte ist nie alleiniger Träger einer Gruppierung. Für alles Bedienbare gibt es `color.border.control` #7C7C80 (≥ 3,35:1 auf allen Flächen). | SPEC 3.3, 6.5 |
| 1.4 | **Spur der Fortschrittsleiste zu schwach.** Offene Segmente Weiß 22 %. | ca. 1,8:1 auf Schwarz | `color.progress.track` Weiß 38 % = 3,39:1; Spur des aktiven Segments 48 %, Füllung darauf 4,29:1. | SPEC 6.8 |
| 1.5 | **Inaktive Schritt-Karten zu dunkel.** `opacity: .45` auf der ganzen Karte. | Fließtext rechnerisch unter 4,5:1, grauer Erklärtext deutlich darunter | `opacity.inactive` 0,6 (hell 0,7): Titel 7,22:1, Fließtext 5,99:1. Grauer Text wird in inaktiven Karten auf `text.body` gesetzt. | SPEC 6.7 |
| 1.6 | **Versalien-Headline bricht mitten im Wort.** Lange Wörter wie „BARRIEREFREIHEIT“ brachen auf schmalen Displays ohne Trennstelle. | – | Regeln für Trennstellen, Höchstlänge 24 Zeichen, Notanker `font.tracking.display-tight` (0,12 em). Für Folien feste Zeichengrenzen je Layout. | SPEC 2, 4.3, 9.3 |
| 1.7 | **Checkbox-Rand hart weiß, Formularrand nicht definiert.** | – | `color.border.control`, Breite `border.width.control` 1,5 px; Weiß bleibt im dunklen Theme zulässig. | SPEC 6.10, 6.16 |
| 1.8 | **Hover nur über `filter: brightness`.** Nicht als Farbe greifbar, in PowerPoint und Figma nicht abbildbar. | – | Feste Farben `color.accent.hover` #FFF07A, `pressed` #E6C800, ebenso für Sekundär und Ghost. | `color.action.*` |
| 1.9 | **Zwei Orange-Bedeutungen.** Orange stand sowohl für Warnungen als auch für die Hervorhebung eines Bauteils im 3D-Modell. | – | Orange ist in ODSV ausschließlich `status.warning`. Hervorhebung im Bild ist Gelb (`lineart.marker`, `accent.line`). | SPEC 3.1, 10.1 |
| 1.10 | **Abstände ohne Raster.** Im CSS stehen 6, 10, 14, 18, 22, 26, 28 px nebeneinander; ein 8er-Raster war vorgesehen, wurde aber nicht eingehalten. | – | 4er-Raster `space.*`. Zwischenwerte (14, 18, 22, 26 px) werden auf 12/16/20/24 gerundet. | SPEC 5 |
| 1.11 | **Radien als Einzelwerte.** 2, 3, 7, 10, 12, 14, 16, 20, 22, 28 px ohne Namen. | – | Benannte Stufen `radius.*` mit Zweck. | `radius.*` |
| 1.12 | **Kein Druckstil.** Schwarze Seite druckt schwarz. | – | `@media print` in `tokens.css`: hell, Karten weiß mit Rand, Größen in pt. | SPEC 3.2 |

---

## 2. Was für ein System fehlte

### 2.1 Farbe und Themes

| Lücke | Warum sie zählt | Lösung | Status |
|---|---|---|---|
| Kein helles Theme | Druck, helle Räume, Beamer mit schwachem Schwarz, Dokumente | `theme.light` als Overrides, `[data-theme="light"]` | geschlossen |
| **Gelb auf Weiß** | #FFE94D auf Weiß hat 1,23:1 – als Text, Linie, Fokus unbrauchbar | Hell: `accent.text` #6B5800 (6,95:1), `accent.line` #8A7200 (4,68:1), Fokusring Schwarz, Primär-Button mit 1-px-Rand; Gelb bleibt nur Fläche mit schwarzer Schrift | geschlossen |
| Keine Info-Farbe | Ausgangsstil kannte nur Grün/Rot/Orange | `status.info` #64D2FF (hell #1F5FC4) | geschlossen |
| Status nur als Einzelfarbe | Für Callout, Badge, Banner braucht es Text-, Flächen-, Rand- und Auf-Farbe | fünf Stufen je Status: `base`, `text`, `subtle`, `border`, `on` | geschlossen |
| Rot als Text zu knapp | #FF453A auf Karte 4,99:1, auf Karte 2 4,61:1 – knapp; auf getöntem Grund darunter | `status.danger.text` #FF6961 (7,45 / 6,03 / 5,56:1) | geschlossen |
| Keine Zustandsfarben für deaktiviert | – | `color.action.disabled.*`, `color.text.disabled` | geschlossen |
| Keine dritte Flächenstufe | Dashboards brauchen „ausgewählt“ und „gedrückt“ | `color.surface.3`, dazu `overlay`, `bar`, `scrim`, `inverse` | geschlossen |
| Signet-Verlauf nur beschrieben, nicht im CSS | Nicht wiederverwendbar | `gradient.signet`, `color.signet.1–4`, `signet.dot` mit Einsatzregel | geschlossen |

### 2.2 Datenvisualisierung

| Lücke | Lösung | Status |
|---|---|---|
| Keinerlei Diagrammfarben | Kategorial 7 Farben + „Sonstige“, sequenziell 6 Stufen, divergierend 7 Stufen – je für Dunkel und Hell (`dataviz.*`) | geschlossen |
| Unterscheidbarkeit bei Farbfehlsichtigkeit ungeprüft | Reihenfolge per Aufzählung optimiert; benachbart ΔE ≥ 13,7 (dunkel) / ≥ 8,1 (hell); Grenzen für Streudiagramme dokumentiert | geschlossen, siehe 3.2 |
| Keine Regeln für Achsen, Gitter, Legende, Tooltip | SPEC 8.2 | geschlossen |
| Keine Auswahlhilfe für Diagrammtypen | SPEC 7.3 | geschlossen |
| Keine Farben für PowerPoint-Diagramme | `accent1–6` = kategoriale Slots 1–6, `pptx.json → chartRules` | geschlossen |
| Kein Diagramm-Code | Regeln in SPEC 8; `web/odsv-charts.js` liegt vor, Abgleich offen | teilweise (3.1) |

### 2.3 Typografie

| Lücke | Lösung | Status |
|---|---|---|
| Eine Schriftfamilie für alles, keine Mono | `font.family.display / text / mono` | geschlossen |
| Größen als lose Einzelwerte (11, 12, 13, 14, 15, 16, 17, 20, 22 px im CSS verstreut) | Skala `font.size.*` und fertige Stile `text.*` | geschlossen |
| Keine Größen für Folien | pt-Tabelle mit `spc`-Werten in `pptx.json → textStyles` | geschlossen |
| Laufweite in PowerPoint | CSS rechnet relativ (em), PowerPoint absolut (1/100 pt) – Formel und Tabelle | geschlossen |
| Schrift nicht portabel | SF Pro nur auf Apple-Geräten und nicht weitergebbar; auf anderen Systemen greift ein Ersatz | Web: Systemstapel; PowerPoint: Arial (Begründung SPEC 9.1) | geschlossen, mit Abstrich (3.3) |
| Versalien-Regeln nur für die eine Seite | allgemeine Regeln SPEC 4.3 | geschlossen |

### 2.4 Komponenten

Im Ausgangsstil vorhanden und übernommen: Button (3 Arten), Eyebrow, Headline-Gruppe, Karte, Spec-Kachel, Schritt-Karte, Fortschrittsleiste, Segment-Umschalter, Checkliste, Akkordeon, Tabelle (eine), Warn-Karte, Bottom-Sheet (im Fluss), Kapitelleiste, 3D-Label, Icon-Kachel, Ladekreis, Chips.

| Fehlte | Lösung | Status |
|---|---|---|
| **Formularfelder** (Text, Auswahl, Radio, Schalter, Regler, Fehlertext) | SPEC 6.16, Tokens `size.field`, `border.control` | geschlossen (Regel) |
| Tabs | SPEC 6.17 | geschlossen (Regel) |
| Tooltip, auch für Daten | SPEC 6.18, `shadow.overlay`, `z.tooltip` | geschlossen (Regel) |
| Badge / Pill als eigener Baustein | SPEC 6.19 | geschlossen (Regel) |
| Callout-Varianten Info, Erfolg, Fehler, neutral | SPEC 6.13 | geschlossen (Regel) |
| Leerzustand | SPEC 6.23 | geschlossen (Regel) |
| Ladezustand über den Ladekreis hinaus (Skelett) | SPEC 6.24 | geschlossen (Regel) |
| Diagramm-Rahmen | SPEC 6.21 | geschlossen (Regel) |
| KPI mit Veränderung, Ziel, Sparkline | SPEC 6.6, 7.2 | geschlossen (Regel) |
| Navigation für Anwendungen (Seitenleiste, Bereichs-Tabs) | SPEC 6.15 | geschlossen (Regel) |
| Modales Sheet / Dialog, Toast | SPEC 6.14, 6.25 | geschlossen (Regel) |
| **Tabellen-Dichte**, Sortierung, Auswahl, klebender Kopf | drei Dichten `size.row-*`, SPEC 6.12, 7.4 | geschlossen (Regel) |
| Zustände durchgängig (Hover, Gedrückt, Deaktiviert, Laden, Fehler) | Grundregel SPEC 6 + Farben `color.action.*` | geschlossen |
| **Fokus-Stile** als System | Ausgangsstil hatte einen gelben Ring und zwei Sonderfälle. Jetzt `color.focus.ring`, `ring-on-accent`, `border.width.focus`, `border.focus-offset`; hell Schwarz | geschlossen |
| Schatten | Karten bleiben ohne; für Schwebendes `shadow.overlay`, `shadow.sheet`, sparsam `glow-*` | geschlossen |
| Z-Ebenen | Ausgangsstil: 1, 2, 3, 4, 20, 30, 60, 70, 100 ohne Namen → `z.*` | geschlossen |

### 2.5 Layout je Medium

| Lücke | Lösung | Status |
|---|---|---|
| Nur Seitenraster (1120 px, Scroll-Sektionen) | Dashboard: 12 Spalten, Seitenleiste, `layout.maxw-wide`, Lücke 16 px | geschlossen |
| Kartenradius 28 px und 24 px Innenabstand zu groß für dichte Kacheln | Dashboard-Karte `radius.card-sm` 20 px, `layout.card-padding-compact` 16 px | geschlossen |
| Bedienhöhen nur 52/44 px | `size.control-sm` 36 px, `control-xs` 28 px – nur Zeigergerät | geschlossen |
| Breakpoints nur 380/768/1024/1280 | ergänzt um `sm` 600 und `2xl` 1536 | geschlossen |
| **Keine Folien** | Format, Raster in Zoll/EMU, Zonen, 16 Layouts mit Positionen und Platzhalter-Rollen, Farbthema, Schriften; Vorlage liegt vor | geschlossen (Spezifikation), Abgleich offen (3.1) |
| Fortschrittsleiste nur als Scroll-Anzeige | als Kapitelanzeige auf Folien und als Zähl-Leiste verallgemeinert | geschlossen |
| Bottom-Sheet nur als Seitenende | als Abschlussfolie und modale Variante | geschlossen |

### 2.6 Illustration und Icons

| Lücke | Lösung | Status |
|---|---|---|
| Line-Art-Farben nur im Code der Explosionszeichnung fest verdrahtet | `color.lineart.*` für Dunkel und Hell | geschlossen |
| Regeln für Line-Art, Hand, Explosionszeichnung nur verstreut | SPEC 10.1–10.3 | geschlossen |
| **Kein Icon-Satz** – Icons waren je Stelle von Hand gezeichnet | Maße und Pflichtliste festgelegt; `web/icons.svg` liegt vor, Abgleich offen | teilweise (3.1) |
| Signet war an ein Produktthema gebunden | allgemeine Bauregel SPEC 10.5 | geschlossen (Regel) |
| Helle Bilder auf schwarzem Grund ungeregelt | Regel „helle Karte“ SPEC 10.5 | geschlossen |

### 2.7 Bewegung und Technik

| Lücke | Lösung | Status |
|---|---|---|
| Dauern teils als Zahl im CSS (.2s, .3s, .5s, 2s) statt als Variable; `--dur-1` wurde benutzt, aber nie definiert | `motion.duration.*`, `motion.easing.*`, `motion.distance.*` | geschlossen |
| Reduzierte Bewegung musste je Baustein einzeln abgeschaltet werden | `tokens.css` setzt Dauern und Wege zentral auf null | geschlossen |
| Kein Token-Format für Werkzeuge | W3C-DTCG-JSON, CSS wird erzeugt, Prüfskript | geschlossen |
| Keine Versionierung | SemVer, SPEC 14 | geschlossen |

---

## 3. Bewusst offen in v1.0

### 3.1 Noch nicht gebaut oder noch nicht abgeglichen

Parallel zu dieser Analyse sind `web/` und `pptx/` entstanden. Geprüft wurde nur das Messbare: gleiche Token-Datei, alle verwendeten Variablen definiert, Farbthema und Schrift der Vorlage wie in `pptx.json`.

| Offen | Stand | Vorschlag |
|---|---|---|
| **Abgleich `web/odsv.css` ↔ SPEC 6** | Datei liegt vor (857 Zeilen). Ob alle 24 Komponenten mit Varianten und Zuständen der Spezifikation entsprechen, ist nicht geprüft. | Komponente für Komponente gegen SPEC 6 prüfen; Abweichungen in eine der beiden Richtungen bereinigen |
| **Abgleich `pptx/ODSV-Vorlage.pptx` ↔ SPEC 9.3** | Vorlage liegt vor (18 Folien, 16 Layouts); Spezifikation, `pptx.json` und `catalog/pptx-layouts.json` nennen alle 16, Rollen sind aus der Vorlage abgeleitet. Positionen der 13 Kernlayouts sind nicht maßgenau gegen die Vorlage verglichen. Auf Windows und Mac nicht geöffnet. | Layoutliste und Maße angleichen; in PowerPoint auf beiden Systemen öffnen, Umbruch der Versalien prüfen |
| **Icon-Satz** | `web/icons.svg` enthält 33 Icons und das Signet. Nicht geprüft gegen die Pflichtliste und die Maße aus SPEC 10.4. | abgleichen, fehlende ergänzen |
| **Diagramm-Code** | `web/odsv-charts.js` liegt vor; nicht gegen SPEC 8 geprüft. | abgleichen |
| **Signet-Baukasten** | Je Produkt eine eigene Form; kein Generator. | – |

### 3.2 Bekannte Grenzen

| Grenze | Folge |
|---|---|
| **Gelb liegt außerhalb des Helligkeitsbands** der kategorialen Palette (bewusst: Slot 1 ist die betonte Reihe). | Für gleich gewichtete Reihen bei Slot 2 beginnen. |
| **Streudiagramme:** alle Farbpaare unterscheidbar nur für 5 Farben (dunkel) bzw. 3 (hell). Blau↔Violett und Türkis↔Grün sind bei Rot-Grün-Schwäche nah. | Mehr Gruppen → kleine Vielfache oder Formen zusätzlich. |
| **Helle Diagrammfarben** Gold, Türkis, Orange haben 3,3–3,8:1 – genug für Flächen, nicht für dünne Linien ohne Beschriftung. | Direktbeschriftung oder Tabellenansicht ist Pflicht. |
| **Farbprüfung der Diagrammpalette** lief mit einem Validator außerhalb des Ordners. `check_tokens.py` prüft nur Kontraste. | Bei Änderung einer Diagrammfarbe neu prüfen. |
| **`text.faint` auf Karte 3** hat 4,27:1. | Auf `surface.3` mindestens `text.muted`. |
| **Helles Theme ist rechnerisch geprüft, nicht am Bildschirm.** Es gab keine helle Vorlage. | Vor dem ersten Einsatz Sichtprüfung. |
| **Info-Farbe Cyan** liegt nah am Türkis der Diagrammpalette. | Status und Reihenfarben nie im selben Diagramm (SPEC 8.1). |
| **Rundung auf das 4er-Raster** verschiebt einzelne Maße bestehender Seiten um 2 px. | Bestehende Seiten beim Umstieg auf ODSV nachziehen. |

### 3.3 Bewusst nicht Teil des Systems

| Nicht enthalten | Grund |
|---|---|
| Ausgelieferte Schrift | SF Pro ist nicht weitergebbar; eine Webschrift kostet Ladezeit. Folge: Schriftbild weicht je Gerät ab (SF Pro, Segoe UI, Roboto, Inter), in PowerPoint Arial. Wer Gleichheit braucht, bindet Inter ein. |
| Automatischer Wechsel nach `prefers-color-scheme` | Dunkel ist die Identität. Hell wird ausdrücklich gesetzt. |
| Hoher Kontrast als eigenes Theme | Das dunkle Theme liegt bereits weit über AA; erzwungene Farben werden über Ränder gestützt (SPEC 12). |
| AAA als Ziel | AA ist das Ziel; viele Paare erreichen AAA, zugesichert wird es nicht. |
| Rechts-nach-links-Schriften, andere Sprachen als Deutsch | Ton, Zahlenformate und Versalien-Regeln sind für Deutsch geschrieben. |
| 3D-Viewer und Explosionszeichnung als Systembausteine | Sie sind produktspezifisch; ODSV regelt nur ihren Stil (Bühne, Labels, Line-Art). |
| E-Mail, Druckvorlagen (Briefbogen, Flyer), Social-Media-Formate | Nicht im Auftrag; Druck ist nur als Ausgabe von Web-Seiten geregelt. |
| Markenname, Logo, Bildwelt | ODSV ist markenneutral; jedes Produkt bringt Signet und Wortmarke mit. |
| Fremdes Referenzmaterial | Screenshots anderer Produkte dienen nur als Stilreferenz und gehören in kein Produkt. |

---

## 4. Empfohlene nächste Schritte

1. `web/` und `pptx/` gegen SPEC 6, 8, 9.3 und 10.4 abgleichen (siehe 3.1).
2. Vorlage auf Windows und Mac in PowerPoint öffnen: Umbruch der Versalien, Farbzuordnung, Diagrammfarben.
3. Helles Theme und Druck an einer echten Seite ansehen.
4. Bestehende Seiten schrittweise auf ODSV-Tokens umstellen.

---

## 5. Playwright-Prüfung (17.11.2026)

Werkzeug: `tools/audit.js`. Geprüft wurden die Referenzseite und beide Beispiele, jeweils bei 390 px (Touch) und 1440 px, dunkel und hell. Prüfpunkte:
- Konsole und horizontales Scrollen
- Kontrast jedes Textes gegen seinen tatsächlichen Hintergrund
- Trefferflächen
- Farben, Schriftgrößen und Radien außerhalb der Tokens
- Überschriftenfolge, Fokus-Sichtbarkeit, Bedienelemente ohne Namen, überlappende Texte

Dazu kam eine Sichtprüfung aller 34 Sektionen.

| Befund | Behebung |
|---|---|
| Lange Versalien-Wörter brachen mitten im Wort (`overflow-wrap`) | `ODSV.fit` in `odsv.js`, Klasse `.odsv-fit-tight` |
| Zustandsraster der Referenz: Primär-Buttons (min. 240 px) und Umschalter überlappten | Zellen wachsen mit dem Inhalt |
| Liste und Fakten als Karte: Aufzählungspunkte am Kartenrand, Spalten versetzt | Innenabstand und Kartenrhythmus korrigiert |
| KPI-, Schritt- und Diagrammkarten einer Zeile unterschiedlich hoch | `height: 100%` im Raster |
| Achse im Balkendiagramm bis 500 bei Höchstwert 277 | feinere Achsenstufen (→ 300) |
| Labels auf der Bühne überlappten sich | Positionen relativ zur Mitte |
| Badge „Warnung“ hell 4,43:1 | `status.warning` hell #804900 |
| Trefferflächen unter 44 px auf Touch, leise Links unter 24 px | `pointer: coarse` bzw. min. 24 px |
| Deaktivierte Option nicht abgeschwächt, Tooltip ohne sichtbares Beispiel | Label in `text.disabled`, Demo mit `is-open` |

Ergebnis nach der Behebung: 0 Konsolenfehler, 0 Überlauf, alle Farben, Schriftgrößen und Radien aus Tokens, 0 Fokus- und Namensfehler. Verbleibend sind nur bewusste Ausnahmen:
- Die deaktivierte Option liegt unter 4,5:1; deaktivierte Elemente sind von WCAG ausgenommen.
- Die Schriftgrößen, die `ODSV.fit` verkleinert hat, liegen außerhalb der Token-Stufen.

---

## 6. Beschreibungslücken und Agenten-Optimierung (17.11.2026)

Vorgehen: Alle Klassen aus `odsv.css`, alle `data-odsv-*`-Attribute, alle Tokens und alle Folienlayouts wurden maschinell gegen die Beschreibungen abgeglichen.

| Lücke | Umfang | Geschlossen durch |
|---|---|---|
| Klassen-API nicht beschrieben (SPEC beschreibt Rollen, nicht Klassen) | 140 Wurzeln, 115 Modifier, 10 Zustände | `catalog/components.json` / `COMPONENTS.md`: 30 Komponenten mit Zweck, Abgrenzung, Varianten, Zuständen, Regeln, A11y, Inhaltsgrenzen und Referenz-Markup; `classes.json` als Whitelist |
| Verhalten undokumentiert | 14 data-Attribute, globale API, 2 Events | `catalog/js-api.md` |
| Diagramm-API nur im Quelltext-Kommentar | 6 Funktionen, Optionen `yMax`, `yTicks`, `yFormat` fehlten | `catalog/js-api.md` |
| Tokens ohne Beschreibung | 123 von 305 | alle 305 mit `$description` in `tokens.json` |
| Folien: Rollen ↔ Platzhalter nicht dokumentiert, `roles.json` veraltet (KPI, Abschluss) | 16 Layouts | `roles.json` aus Vorlage neu erzeugt, `catalog/pptx-layouts.json`, Spezifikation für Bild in Karte, Nur Titel, Leer ergänzt |
| Kein Werkzeug zum Befüllen der Vorlage | Fortschrittsleiste, Quelle, Diagramm- und Tabellenstil nur im Erzeugerskript | `pptx/odsv_pptx.py` (Deck, Rollen, Fortschritt, Diagramme, Tabellen, Bilder, Vergleich/Prozess-Icons, `check()`, `render_png()`) |
| Kein Startpunkt | – | `templates/website.html`, `dashboard.html`, `deck_example.py` |
| Keine Selbstprüfung für erzeugte Inhalte | – | `tools/lint-html.js` (18 Regel-IDs wie in AGENTS.md), `Deck.check()`, `tools/validate.sh` |
| Kein Einstieg für Agents | – | `AGENTS.md`, `llms.txt` |
| Beschreibung und Code können auseinanderlaufen | – | Katalog wird erzeugt; neue CSS-Wurzel ohne Eintrag lässt `validate.sh` scheitern |

Beim Abgleich gefundene Fehler im Code:
- Der Listen-Reset `ul[class], ol[class]` war spezifischer als die Abstandshelfer `.odsv-mt-*` und als `.odsv-card` (Innenabstand). Jetzt steht er in `:where()`.
- Leise Links in `.odsv-sheet__actions` waren seit der Trefferflächen-Regel nicht mehr zentriert.
- Im Dashboard-Beispiel fehlte bei drei Diagrammen die Quelle.
