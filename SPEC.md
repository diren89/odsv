# ODSV – Design-System, Spezifikation v1.0.0

Stand 17.11.2026 · Quelle der Wahrheit für Werte: `tokens/tokens.json` · Diese Datei beschreibt Regeln, nicht Werte. Wo beides steht, gilt das Token.

ODSV ist ein markenneutrales System für **Websites, Dashboards und Präsentationen**. Stilmerkmale: fast schwarzer Grund, gesperrte Versalien-Headlines, ein gelber Akzent, dunkle Karten mit großen Radien, weiße Line-Art, segmentierte Fortschrittsleiste, ein Signet im Verlauf Pink → Orange → Gelb.

**Für AI-Agents:** Einstieg ist `AGENTS.md`; maschinenlesbar sind `catalog/` (Komponenten, Klassen, Tokens, Icons, Folienlayouts) und die Prüfwerkzeuge `tools/lint-html.js` und `tools/validate.sh` (Kapitel 15).

**So liest man Token-Namen:** `color.text.muted` (JSON-Pfad) = `--odsv-color-text-muted` (CSS) = Rolle `text.muted` in `pptx.json`.

Inhalt: 1 Markenidee · 2 Ton · 3 Farbe · 4 Typografie · 5 Raster · 6 Komponenten · 7 Dashboards · 8 Diagramme · 9 Präsentationen · 10 Illustration · 11 Bewegung · 12 Barrierefreiheit · 13 Dateistruktur · 14 Versionierung · 15 Agenten-Schnittstelle

---

## 1. Markenidee und Prinzipien

**Idee:** Ein Werkzeug, das sich wie ein gutes Kamera-Onboarding anfühlt. Schwarz ist die Bühne, der Inhalt ist das Licht. Ein einziger Akzent sagt „hier“. Alles andere ist Weiß in Abstufungen.

| # | Prinzip | Do | Don't |
|---|---|---|---|
| 1 | **Schwarz ist die Bühne.** Der Grund ist `color.bg.base`, Tiefe entsteht durch Flächenstufen, nicht durch Schatten. | Karten in `surface.1` mit 1-px-Rand; Karte in Karte `surface.2`. | Schlagschatten unter Karten, farbige Sektionshintergründe, Verläufe als Fläche. |
| 2 | **Ein Akzent, eine Bedeutung.** Gelb heißt „hier handeln“ oder „hier schauen“. | Ein gelber Button je Ansicht; eine gelbe Zahl je Kachelgruppe; die betonte Diagrammreihe. | Gelb als Dekor, zwei gelbe Buttons nebeneinander, gelber Fließtext, Gelb für „Warnung“. |
| 3 | **Dreiklang.** Jeder Abschnitt beginnt mit Eyebrow → Versalien-Headline → grauem Zweitsatz. | Headline ein bis drei Wörter; der Zweitsatz erklärt in einem Satz. | Headline als ganzer Satz in Versalien; Zweitsatz weglassen und die Headline überladen. |
| 4 | **Linie statt Fläche.** Illustrationen und Icons sind Strichzeichnungen; gefüllt ist nur, was Akzent oder Hand ist. | Weiße Line-Art 2–3 px, runde Enden, Gelb als einziger Farbfleck. | Fotostock, 3D-Glanz, Emoji, mehrfarbige Icons, gefüllte Icon-Sets. |
| 5 | **Fortschritt ist sichtbar.** Wer liest, sieht, wo er ist: segmentierte Leiste, Schrittnummer, Zähler. | Segment je Kapitel; „7 von 23“ neben der Leiste. | Prozentringe, Konfetti, Fortschritt nur über Farbe. |
| 6 | **Ruhig und genau.** Bewegung erklärt einen Zustandswechsel und endet. | 200–400 ms, eine Bewegung zur Zeit, Scroll steuert. | Federn, Schleifen, Parallax-Dekor, Scroll-Hijacking. |
| 7 | **Ehrlich vor elegant.** Warnungen, Grenzen und Quellen stehen sichtbar da. | Warn-Karte in voller Länge vor dem Schritt; Quelle unter jeder Zahl. | Hinweise in Fußnoten verstecken, Zahlen runden, Superlative. |

Abgrenzung: ODSV ist eine eigene Gestaltungssprache (Typo, Farbe, Form). Fremde Marken, fremde Screens und SF Pro als ausgelieferte Schrift gehören nicht in Produkte (siehe 4.1).

---

## 2. Ton und Sprache

Sprache ist Deutsch, Anrede „du“ oder neutral – je Produkt einmal festlegen und halten.

**Dreiklang**

| Teil | Form | Länge | Beispiel |
|---|---|---|---|
| Eyebrow | kleine gesperrte Versalien, ordnet ein (Kategorie, Quelle, Kapitel) | 1–4 Wörter | `QUARTALSBERICHT` |
| Headline | große gesperrte Versalien, benennt | 1–3 Wörter, höchstens 24 Zeichen | `KENNZAHLEN` |
| Zweitsatz | normale Schreibweise, grau, erklärt | ein Satz, höchstens 90 Zeichen | „Alle Werte beziehen sich auf das dritte Quartal.“ |

Erst danach folgt Fließtext. In Karten gilt das kleine Muster: fette Kurz-Headline in normaler Schreibweise + grauer Erklärsatz.

**Regeln**

1. **Kurz und selbstbewusst, nie übertrieben.** Keine Superlative („revolutionär“, „garantiert“). Was nicht belegt ist, wird nicht behauptet.
2. **Verben auf Buttons.** „Projekt starten“, „Zur Übersicht“, „Bericht öffnen“. Nie „OK“, „Weiter“ ohne Ziel, „Hier klicken“.
3. **Zahlen mit Einheit und geschütztem Leerzeichen:** `1.284&nbsp;Nutzer`, `ca.&nbsp;15&nbsp;min`, `3–5&nbsp;Tage`. Dezimalkomma, Tausenderpunkt, Bis-Strich ohne Leerzeichen. Unsichere Werte mit „ca.“ oder „bis zu“.
4. **Versalien nur per Stil**, nie im Quelltext getippt (`text-transform: uppercase`, in PowerPoint „Großbuchstaben“ / `cap="all"`). Sonst buchstabieren Screenreader, und Kopieren liefert Geschrei.
5. **„ß“ in Versalien vermeiden.** Headline umformulieren; wenn unvermeidbar, bewusst „SS“.
6. **Lange deutsche Wörter:** Versalien-Headlines dürfen nicht mitten im Wort brechen (z. B. „BARRIEREFREIHEIT“ auf schmalen Displays). Entweder Trennstelle vorgeben (`&shy;`), kürzer formulieren oder `font.tracking.display-tight` verwenden – siehe 4.3.
7. **Fehler- und Leertexte** sagen, was ist, und was als Nächstes geht: „Keine Daten für diesen Zeitraum. Zeitraum ändern.“ Keine Schuldzuweisung, kein „Ups“.
8. **Sicherheit schlägt Eleganz.** Warntexte werden nicht gekürzt, nicht versalisiert, nicht eingeklappt.

Wortliste: „Überspringen“ (nicht „Skip“), „Zurücksetzen“, „Mehr anzeigen“, „Schließen“, „Laden …“ (mit Auslassungszeichen), „Stand 17.11.2026“.

---

## 3. Farbe

### 3.1 Rollen (dunkles Theme = Standard)

| Rolle | Token | Wert | Einsatz |
|---|---|---|---|
| Grund | `color.bg.base` | #000000 | Seite, Folie |
| Grund abgesetzt | `color.bg.subtle` | #0A0A0A | Signet-Karte, abgesetzte Sektion |
| Bühne | `color.bg.stage` | #050505 | 3D, Explosionszeichnung, Vollbild-Diagramm |
| Karte 1 | `color.surface.1` | #1C1C1E | Karte |
| Karte 2 | `color.surface.2` | #232325 | Karte in Karte, Hover |
| Karte 3 | `color.surface.3` | #2C2C2E | gedrückt, ausgewählte Zeile |
| Rand dekorativ | `color.border.subtle` | #2C2C2E | Kartenrand, Trennlinie |
| Rand betont | `color.border.strong` | #48484A | Label-Pille, Tabellenkopf-Linie |
| Rand Bedienelement | `color.border.control` | #7C7C80 | Formularfeld, Checkbox |
| Text 1–5 | `color.text.primary / body / secondary / muted / faint` | #FFFFFF / #E6E6E6 / #CCCCCC / #A1A1A6 / #8E8E93 | Headline · Fließtext · Eyebrow/Label · Zweitsatz · Fußnote |
| Text deaktiviert | `color.text.disabled` | #636366 | nie für Information |
| Akzent Fläche | `color.accent.fill` → `fill-end` | #FFE94D → #F5D400 | Primär-Button (Verlauf `gradient.action-primary`) |
| Akzent Hover / Pressed | `color.accent.hover / pressed` | #FFF07A / #E6C800 | Zustände |
| Akzent Text / Linie | `color.accent.text / line` | #FFE94D | Kennzahl, Icon, Marker |
| Auf Akzent | `color.accent.on` | #000000 | Schrift auf Gelb |
| Erfolg | `color.status.success.*` | #30D158 | abgehakt, „richtig“ |
| Warnung | `color.status.warning.*` | #FF9F0A | Vorsicht, Sicherheitshinweis |
| Fehler | `color.status.danger.*` | #FF453A (Text #FF6961) | „falsch“, Fehler, Alarm |
| Info | `color.status.info.*` | #64D2FF | neutraler Hinweis |
| Fokus | `color.focus.ring` | #FFE94D | Fokusring; um gelbe Flächen `ring-on-accent` (#FFFFFF) |
| Signet | `gradient.signet` | #EC3A78 → #EE6A2C → #F09A35 → #F3C340, Kern #FFE94D | nur Signet/Titelmoment |

Jeder Status hat fünf Stufen: `base` (Icon, Fläche), `text`, `subtle` (getönter Grund), `border`, `on` (Schrift auf `base`).

**Farbregeln**

- **Gelb** nur für: eine primäre Handlung, eine betonte Zahl, den aktiven Marker, Listenpunkte, die Hauptreihe im Diagramm. Gelbe Schrift erst ab 18 px oder fett.
- **Grün** nur „erledigt/richtig“, **Rot** nur „falsch/Fehler/Alarm“, **Orange** nur „Vorsicht“. Status nie allein über Farbe: immer Icon + Wort.
- **Der Signet-Verlauf** kommt je Produkt genau einmal groß vor (Hero, Titelfolie). Nie als Button, Text, Diagrammfarbe oder Hintergrund.
- **Text steht in Textfarben**, nicht in Akzent- oder Reihenfarben (Ausnahme: betonte Kennzahl).
- Textstufen sind deckende Werte, keine transparenten Weißstufen. Grund: PowerPoint, Diagramm-Bibliotheken und Druck brauchen feste Farben; auf Karten bleibt der Kontrast berechenbar.

### 3.2 Helles Theme (`[data-theme="light"]`) und Druck

Ergänzung für Druck und helle Umgebungen, nicht der Normalfall.

| Rolle | Wert hell | Anmerkung |
|---|---|---|
| Grund / Karte 1 / 2 / 3 | #FFFFFF / #F5F5F7 / #EBEBF0 / #E5E5EA | |
| Rand dekorativ / betont / Bedienelement | #D2D2D7 / #A1A1A6 / #808085 | |
| Text 1–5 | #000000 / #1D1D1F / #3A3A3C / #58585C / #68686D | |
| Akzent Fläche | #FFE94D | bleibt; Primär-Button bekommt 1-px-Rand `color.action.primary.border` (#8A7200) |
| Akzent Text / Linie | #6B5800 / #8A7200 | **Gelb auf Weiß hat 1,23:1 und ist verboten** |
| Sekundär-Button | #1D1D1F mit weißer Schrift | kehrt sich um |
| Status Erfolg / Warnung / Fehler / Info | #146C2E / #804900 / #C8102E / #1F5FC4 | dunkle Stufen, weiße Schrift auf `base` |
| Fokusring | #000000 | Gelb trägt auf Weiß nicht |

**Druck** (`@media print`) schaltet unabhängig vom gesetzten Theme auf Hell und zusätzlich: alle Karten weiß mit Rand #86868B, keine Schatten, Fließtext schwarz, Schriftgrößen in pt (17 px → 11 pt). Top-Bar, Bottom-Sheets, 3D-Bühnen und Bedienelemente werden ausgeblendet; Akkordeons gedruckt geöffnet; Link-Ziele hinter dem Linktext ausgeschrieben.

### 3.3 Kontrastwerte (WCAG 2.2, nachgerechnet)

Berechnet mit `tools/check_tokens.py` (relative Leuchtdichte nach WCAG, transparente Farben vorher auf den Grund gerechnet). Werte je Fläche: Grund / Karte 1 / Karte 2.

| Vordergrund | Dunkel | Hell | Soll |
|---|---|---|---|
| `text.primary` | 21,00 / 17,01 / 15,69 | 21,00 / 19,29 / 17,67 | ≥ 4,5 |
| `text.body` | 16,83 / 13,63 / 12,57 | 16,83 / 15,46 / 14,16 | ≥ 4,5 |
| `text.secondary` | 13,08 / 10,59 / 9,77 | 11,35 / 10,42 / 9,55 | ≥ 4,5 |
| `text.muted` | 8,16 / 6,61 / 6,10 | 7,08 / 6,50 / 5,96 | ≥ 4,5 |
| `text.faint` | 6,44 / 5,22 / 4,81 | 5,54 / 5,09 / 4,66 | ≥ 4,5 |
| `accent.text` | 17,01 / 13,79 / 12,71 | 6,95 / 6,38 / 5,85 | ≥ 4,5 |
| `accent.line` | 17,01 / 13,79 / 12,71 | 4,68 / 4,30 / 3,94 | ≥ 3 |
| `status.success.text` | 10,39 / 8,42 / 7,76 | 6,53 / 6,00 / 5,50 | ≥ 4,5 |
| `status.warning.text` | 10,22 / 8,28 / 7,63 | 6,22 / 5,71 / 5,24 | ≥ 4,5 |
| `status.danger.text` | 7,45 / 6,03 / 5,56 | 5,88 / 5,40 / 4,95 | ≥ 4,5 |
| `status.danger.base` (Icon, Rand) | 6,16 / 4,99 / 4,61 | 5,88 / 5,40 / 4,95 | ≥ 3 |
| `status.info.text` | 12,20 / 9,89 / 9,12 | 6,01 / 5,52 / 5,06 | ≥ 4,5 |
| `border.control` (zusätzlich Karte 3) | 5,05 / 4,09 / 3,77 / 3,35 | 3,93 / 3,61 / 3,31 / 3,13 | ≥ 3 |
| `lineart.dim` | 6,44 / 5,22 / 4,81 | 5,07 / 4,66 / 4,27 | ≥ 3 |

| Paar | Dunkel | Hell | Soll |
|---|---|---|---|
| Schwarz auf Primär-Button (Verlaufsanfang / -ende / Hover / Pressed) | 17,01 / 14,30 / 18,00 / 12,63 | 17,01 / 14,30 / 18,00 / 14,30 | ≥ 4,5 |
| Schrift auf Sekundär-Button | 18,82 | 16,83 | ≥ 4,5 |
| Schrift auf Ghost-Button | 17,56 | 21,00 | ≥ 4,5 |
| Schrift auf deaktiviertem Button | 4,27 | 4,41 | (befreit; freiwillig ≥ 3) |
| Icon auf gelber Kachel (Anfang / Ende) | 13,19 / 8,49 | gleich | ≥ 3 |
| Schrift auf Statusfläche Erfolg / Warnung / Fehler / Info | 8,45 / 10,22 / 6,16 / 12,20 | 6,53 / 6,22 / 5,88 / 6,01 | ≥ 4,5 |
| Fließtext im Callout (getönter Grund auf Karte 1), schwächster Wert | 10,02 | 13,03 | ≥ 4,5 |
| Statuswort im Callout, schwächster Wert (Fehler) | 5,02 | 4,56 | ≥ 4,5 |
| Fortschritt: offenes Segment auf Grund | 3,39 | 3,59 | ≥ 3 |
| Fortschritt: Füllung auf Spur des aktiven Segments | 4,29 | 3,66 | ≥ 3 |
| Druck: Fließtext / Fußnote / Kartenrand auf Weiß | – | 21,00 / 11,35 / 3,62 | ≥ 7 / ≥ 7 / ≥ 3 |

**Bewusst unter 3:1 – und warum das zulässig ist**

- `border.subtle` auf Grund 1,51:1, auf Karte 1,22:1; Karte 1 gegen Grund 1,23:1. Kartenränder sind Dekor. Folge: **Eine Karte darf nie der einzige Träger einer Information sein** („diese Gruppe gehört zusammen“ muss auch aus Überschrift und Abstand hervorgehen). Bedienelemente nutzen `border.control`.
- `text.disabled` 3,51 / 2,84:1 – deaktivierte Elemente sind von WCAG ausgenommen; trotzdem nie Information darin ablegen.
- Gelb auf Weiß 1,23:1 – deshalb gibt es im hellen Theme `accent.text` und `accent.line`.

**Kontrastregel:** Ein Grau unter 4,5:1 (z. B. Weiß 45 % ≙ #737373: 4,43:1 auf Schwarz, 3,59:1 auf Karten) ist für kleine Schrift unzulässig. Die blasseste Textstufe ist deshalb `text.faint` #8E8E93. Die Spur der Fortschrittsleiste erreicht mindestens 3:1.

---

## 4. Typografie

### 4.1 Schriften

| Rolle | Token | Stapel |
|---|---|---|
| Display | `font.family.display` | "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Inter, "Segoe UI", Roboto, Arial, sans-serif |
| Text | `font.family.text` | "SF Pro Text", -apple-system, …, Arial, sans-serif |
| Mono | `font.family.mono` | ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace |

Es wird **keine Schrift ausgeliefert**. Der Stapel nimmt die Systemschrift: SF Pro auf Apple-Geräten, Segoe UI auf Windows, Roboto auf Android; Inter greift, wenn installiert. Wer überall dasselbe Schriftbild braucht, bindet Inter (OFL) selbst ein und setzt es an die erste Stelle. PowerPoint: Arial, Begründung in 9.1.

### 4.2 Größen, Gewichte, Zeilenhöhen

Feste Stufen `font.size.*` (px): 11 · 12 · 13 · 14 · 15 · 16 · 17 · 20 · 22 · 24 · 28 · 32 · 40 · 48 · 64 · 80. Gewichte: 400 · 500 · 600 · 700. Zeilenhöhen: 1,1 (Zahlen) · 1,25 (Headlines) · 1,4 (kleine Texte) · 1,5 (Fließtext).

| Stil (`text.*`) | Größe | Gewicht | Laufweite | Zeilenhöhe | Versalien | Farbe | Einsatz |
|---|---|---|---|---|---|---|---|
| `display` | fluid 28 → 64 px | 600 | 0,2 em | 1,25 | ja | primary | H1, Hero |
| `headline` | fluid 22 → 40 px | 600 | 0,2 em | 1,25 | ja | primary | H2 je Sektion |
| `title` | fluid 20 → 24 px | 700 | −0,005 em | 1,25 | – | primary | Karten-Headline (H3) |
| `subtitle` | fluid 17 → 20 px | 400 | 0 | 1,4 | – | muted | grauer Zweitsatz |
| `body` | 17 px | 400 | 0 | 1,5 | – | body | Fließtext, höchstens 640 px breit |
| `body-small` | 15 px | 400 | 0 | 1,4 | – | muted/body | Erklärtext in Karten, Tabellen |
| `small` | 14 px | 400 | 0 | 1,4 | – | muted/faint | Fußnote, Hinweiszeile |
| `caption` | 12 px | 400 | 0 | 1,4 | – | faint | Achsen, Zeitstempel – kleinste Größe |
| `eyebrow` | 11,5 px | 500 | 0,2 em | 1,4 | ja | secondary | über jeder Headline |
| `label` | 13 px | 500 | 0,15 em | 1,4 | ja | primary/secondary | Formular-/Checklisten-Label, Tabellenkopf |
| `chip` | 11 px | 600 | 0,12 em | 1,1 | ja | primary | Pille, 3D-/Diagramm-Label, KPI-Label |
| `kpi` | fluid 36 → 64 px | 600 | 0 | 1,1 | – | primary/accent | große Kennzahl |
| `kpi-small` | 24 px (ab lg 32–36) | 600 | 0 | 1,1 | – | primary | Kennzahl in kleiner Kachel |
| `number` | fluid 40 → 48 px | 600 | 0 | 1,1 | – | primary | Schrittnummer |
| `button` / `button-small` | 17 / 15 px | 600 | 0 | 1,25 | – | – | Buttons |
| `wordmark` | 15 px (md 18, lg 20) | 600 | 0,14 em | 1,4 | ja | primary 92 % | Wortmarke |
| `code` | 14 px | 400 | 0 | 1,5 | – | body | Code, IDs |

### 4.3 Regeln für gesperrte Versalien

- Höchstens **drei Wörter / 24 Zeichen**, höchstens zwei Zeilen. Sperrung frisst Breite: ein Zeichen braucht rund 0,9 em.
- `text-wrap: balance; hyphens: manual; overflow-wrap: normal`. Lange Wörter bekommen `&shy;` an der Wortfuge. Notanker: `font.tracking.display-tight` (0,12 em). Ohne Trennstelle übernimmt `odsv.js` (`ODSV.fit`): Passt das längste Wort nicht, setzt es zuerst die enge Laufweite und verkleinert dann die Schrift auf höchstens 72 %. Das Wort bricht nie mitten im Wort.
- Die Sperrung hängt auch hinter dem letzten Buchstaben. Bei zentrierten Zeilen `margin-right: -0.2em` (bzw. minus Laufweite) setzen, sonst steht die Zeile optisch links.
- Versalien nie für Fließtext, Fehlermeldungen, Warnungen, Tabellenzellen. Erklärungen stehen immer in normaler Schreibweise daneben.
- Zahlen: `font-variant-numeric: tabular-nums` überall, wo Zahlen untereinander stehen oder sich ändern.
- Überschriftenstruktur: ein `h1`, je Sektion `h2`, Karten `h3`. Eyebrows sind `p`, keine Überschriften.

---

## 5. Raster und Layout

Abstände folgen dem **4er-Raster** `space.*` (4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80 · 96 · 128 · 152 px). Radien: Segment 2 · Checkbox 7 · klein 10 · Bedienelement innen 12 · Bedienelement 14 · Einsatz 16 · Karte klein 20 · Kachel 22 · Karte 28 · Pille.

### 5.1 Website (mobile-first)

| Breakpoint | ab | Spalten | Verhalten |
|---|---|---|---|
| (Basis) | 0 | 2 (Kachelraster), sonst 1 | Buttons volle Breite; Bühne im Schritt; Tabellen als Akkordeon |
| `xs` | 380 px | – | darunter engere Buttons, kleinere Wortmarke |
| `md` | 768 px | 4 | Karten zweispaltig; Buttons Inhaltsbreite (min. 240 px) |
| `lg` | 1024 px | 12 | Bühne neben Text (5 + 7), Tabellen als Tabelle, Top-Bar 76 px |
| `xl` | 1280 px | 12 | größere Abstände unter Sektionsköpfen |

- Inhaltsbreite `layout.maxw` 1120 px, Lesebreite `layout.maxw-text` 640 px, Seitenrand `layout.gutter` 20 → 40 px, Sektionsabstand `layout.section-y` 72 → 152 px.
- Kachelraster („Bento“): Lücke 12 px, ab `lg` 14 px. Kachelbreiten ab `lg`: 3, 4, 6 oder 12 Spalten.
- Kapitel werden durch eine Haarlinie getrennt, nicht durch Flächenwechsel.
- Sticky-Strecken (Scroll-Storytelling) nur ab ausreichender Höhe; mit reduzierter Bewegung entfallen sie (siehe 11).
- Zoom 200 % und 320 px Breite ohne waagrechtes Scrollen. Trefferflächen mindestens 44 × 44 px.

### 5.2 Dashboard (12 Spalten, dicht)

- Aufbau: Seitenleiste `layout.sidebar-width` 264 px (eingeklappt 72 px) + Inhaltsbereich bis `layout.maxw-wide` 1600 px. Unter `lg` wird die Seitenleiste zur Top-Bar mit Menü.
- Raster 12 Spalten, Lücke `layout.grid-gap-dashboard` 16 px, Seitenrand 24 px (mobil 16 px).
- **Dashboard-Karten nutzen `radius.card-sm` (20 px) und `layout.card-padding-compact` (16 px)**, nicht 28/24 – große Radien verschwenden bei kleinen Kacheln Fläche.
- Übliche Spannen: KPI 3 Spalten (md: 6, mobil: 12) · Diagramm 6 oder 8 · Tabelle 12 · Filterzeile 12.
- Reihenfolge von oben: Seitenkopf (Dreiklang, kompakt) → Filterzeile → KPI-Reihe → Diagramme → Tabelle. Eine Seite, eine Frage.
- Dichte siehe 7.4.

### 5.3 Folie 16:9

13,333 × 7,5 in, 12 Spalten, Rand links/rechts 0,667 in, Lücke 0,2 in, Spalte 0,817 in. Details in 9.

---

## 6. Komponenten-Katalog

Dieses Kapitel regelt Gestaltung und Verhalten. Die **Klassen-API** (Wurzelklasse, Elemente `__x`, Modifier `--y`, Zustände `is-*`, data-Attribute) und das Referenz-Markup je Komponente stehen in `catalog/COMPONENTS.md` bzw. `catalog/components.json`; beide werden aus `web/odsv.css` und `web/index.html` erzeugt und können daher nicht veralten.

Für alle Komponenten gilt, wenn nichts anderes steht:

- **Zustände:** Ruhe · Hover (nur bei `@media (hover: hover)`) · Fokus (`:focus-visible`: 2 px `color.focus.ring`, 3 px Abstand) · Gedrückt (`scale(0.98)`, 100–200 ms) · Deaktiviert (`aria-disabled`/`disabled`, kein Hover, Farben `color.action.disabled.*`) · Laden.
- **Übergänge:** `motion.duration.fast` mit `motion.easing.standard`.
- **Trefferfläche:** mindestens 44 × 44 px auf Touch-Geräten (`@media (pointer: coarse)` hebt kleine Buttons, Umschalter, Legenden, Tabs und leise Links auf 44 px); mit Maus mindestens 24 × 24 px (WCAG 2.5.8). Dichte Dashboard-Bedienelemente nur für Zeigergeräte.
- **Semantik zuerst:** echte `button`, `a`, `input`, `details`, `table`. ARIA nur, wo HTML nicht reicht.

### 6.1 Button

| | Primär | Sekundär | Ghost |
|---|---|---|---|
| Fläche | `gradient.action-primary` (Gelb) | `color.action.secondary.bg` (#F2F2F7; hell: #1D1D1F) | `color.action.ghost.bg` + 1 px `border.subtle` |
| Schrift | Schwarz | Schwarz (hell: Weiß) | `text.primary` |
| Hover | `accent.hover` (flächig) | `secondary.hover` | `surface.2` |
| Gedrückt | `accent.pressed` + Skalierung 0,98 | `secondary.pressed` | `surface.3` |
| Fokus | Ring **weiß** (`focus.ring-on-accent`) | Ring gelb | Ring gelb |
| Einsatz | die eine Haupthandlung | Alternative gleichen Rangs | Werkzeug auf Bühne/Diagramm, Nebenhandlung |

- **Anatomie:** Fläche · Text (`text.button`) · optional Icon 18 px links, 8 px Abstand. Höhe `size.control-lg` 52 px, Innenabstand 24 px, Radius `radius.control` 14 px.
- **Größen:** L 52 px/17 px (Standard) · M 44 px/15 px · S 36 px/15 px (nur Dashboard). Mobil volle Breite, ab `md` Inhaltsbreite, Primär mindestens 240 px.
- **Weitere Varianten:** Icon-Button 44 × 44, Radius 12, Ghost-Optik, immer mit `aria-label` · Gefährlich: Ghost mit `status.danger.text` und Rand `status.danger.border`; nie gelb.
- **Laden:** Text bleibt, Ladekreis 14 px links, `aria-busy="true"`, Klicks gesperrt, Breite unverändert.
- **Regeln:** ein Primär-Button je Ansicht. Reihenfolge: Primär links/oben, Textlink daneben. Kein Button nur mit Icon ohne Namen.

### 6.2 Link

- **Varianten:** Textlink im Fließtext (`text.link`, unterstrichen, `text-underline-offset: 3px`) · leiser Link (`text.muted`, 14 px, z. B. „Überspringen“; Hover weiß) · Leistenlink in der Top-Bar (ohne Unterstreichung).
- **Zustände:** Hover `text.link-hover`; besucht wird nicht gefärbt. Fokusring wie überall.
- **Barrierefreiheit:** Links im Fließtext sind immer unterstrichen (Farbe allein reicht nicht). Linktext nennt das Ziel; Dateityp und Größe in Klammern: „Bedienungsanleitung (PDF, 1,2 MB)“. Leise Links behalten 44 px Zeilenhöhe als Trefferfläche.

### 6.3 Eyebrow

- **Anatomie:** eine Zeile `text.eyebrow` in `text.secondary`. Optional Mittelpunkt als Trenner: `BERICHT · Q3 2026`.
- **Regeln:** steht über jeder Headline, 12 px Abstand. Ist ein `p`, keine Überschrift. Nie länger als eine Zeile, nie klickbar.

### 6.4 Headline-Gruppe

- **Anatomie:** optional Icon-Kachel → Eyebrow → Headline (`text.display` oder `text.headline`) → Zweitsatz (`text.subtitle`, `text.muted`) → optional Fließtext. Abstände 12 px, zum Inhalt 32 → 56 px (ab `xl` 64 px).
- **Varianten:** linksbündig (Standard, Dashboard immer) · zentriert (Sektionsauftakt auf Websites) · kompakt (Dashboard-Seitenkopf: Headline 22 px, Laufweite 0,12 em, Zweitsatz 15 px).
- **Barrierefreiheit:** genau eine Überschrift je Gruppe; Reihenfolge im DOM = Lesereihenfolge.

### 6.5 Karte

- **Anatomie:** Fläche `surface.1` · Rand 1 px `border.subtle` · Radius 28 px · Innenabstand 24 px · kein Schatten. Inhalt: optional Label → Titel (`text.title`) → Text.
- **Varianten:** Standard · eingesetzt (`surface.2`, Radius 16, in einer Karte) · Medien-/Bühnenkarte (`bg.stage`) · klickbar (ganze Karte ist Link; Hover `surface.2`, Rand `border.strong`) · aktiv (Rand `border.active`) · Status (Rand `status.*.border`) · kompakt (Dashboard: Radius 20, Innenabstand 16).
- **Zustände:** nicht klickbare Karten haben keinen Hover.
- **Barrierefreiheit:** klickbare Karte = ein Link um den Titel mit gedehnter Trefferfläche, keine verschachtelten Links. Siehe 3.3: Rand ist Dekor.

### 6.6 Spec-Kachel / KPI

- **Anatomie:** Label (`text.chip`-Laufweite, 11,5 px, `text.secondary`) → Wert (`text.kpi` oder `text.kpi-small`, `tabular-nums`) → optional Erklärzeile (15 px, `text.muted`) → optional Veränderung und Sparkline (Dashboard).
- **Varianten:** groß (6 Spalten, Wert bis 64 px) · klein (3 Spalten, Wert 24–36 px) · Text-Kachel (Satz statt Zahl) · KPI-Gruppe (2 × 2 mit Haarlinien statt Einzelkarten, Radius 20, Wert 17 px/600).
- **Akzent:** höchstens ein gelber Wert je Kachel und ein bis zwei gelbe Kacheln je Gruppe. Vorsätze („bis zu“, „ca.“) bleiben weiß.
- **Veränderung:** Pfeil-Icon + Vorzeichen + Wert + Bezug („▲ +4,2 % ggü. Vormonat“). Farbe `status.success.text`/`status.danger.text` nur, wenn die Richtung wirklich gut/schlecht ist, sonst `text.muted`.
- **Barrierefreiheit:** als `dl` (`dt` Label, `dd` Wert) oder Karte mit `h3`. Einheit gehört in den Text, nicht nur ins Label.

### 6.7 Schritt-Karte mit Nummer

- **Anatomie:** Karte · Schrittnummer oben rechts (`text.number`) · optional Illustration/Medienfläche (16:11, Radius 16) · Titel (`text.title`) · Erklärsatz (16 px) · optional aufklappbare Punkte · leiser Link „Überspringen“.
- **Zustände:** aktiv (volle Deckkraft, Rand `border.active`) · inaktiv (`opacity.inactive` 0,6; hell 0,7) · Fokus innerhalb = aktiv. Ohne JavaScript sind alle Karten voll sichtbar.
- **Barrierefreiheit:** Liste `ol`; die Nummer ist Teil der Überschrift („Schritt 2: …“, visuell getrennt). Inaktive Karten bleiben lesbar und bedienbar – die Abdunklung ist nur Führung. Nachgerechnet: Titel 7,22:1, Fließtext 5,99:1 (hell 8,22 / 6,00). Grauer Erklärtext (`text.muted`) fiele darunter und wird in inaktiven Karten auf `text.body` gesetzt. Die Website nutzte 0,45 – damit lag Text unter 4,5:1.

### 6.8 Segmentierte Fortschrittsleiste

- **Anatomie:** n Segmente, Höhe 3 px, Lücke 6 px, Radius 2 px. Offen `progress.track`, erledigt `progress.fill`, aktiv: Spur `progress.track-current` mit Füllung von links. Darunter optional Zeile: links Name des aktiven Kapitels (Eyebrow), rechts Leistenlink.
- **Varianten:** Kapitelleiste (klebt oben, Segmente sind Links, Trefferhöhe 44 px) · Mini-Leiste (in Sticky-Strecken, ohne Links) · Zähl-Leiste (Checkliste: ein Segment je Punkt, Füllung `progress.fill-success`, daneben „7 von 23“) · Folie (ein Segment je Kapitel).
- **Bewegung:** Füllung läuft linear mit dem Scroll, ohne Easing.
- **Barrierefreiheit:** Kapitelleiste = `nav aria-label="Kapitel"` mit Liste von Links, `aria-current="step"` am aktiven; jeder Link hat den Kapitelnamen als `aria-label`. Zähl-Leiste = `role="progressbar"` mit `aria-valuenow/max` oder sichtbarer Zähler mit `aria-live="polite"`. Zustand nie nur über Helligkeit: der Name des aktiven Kapitels steht daneben. Höchstens 12 Segmente als Links (darunter werden sie zu schmal); mehr → Zähl-Leiste.

### 6.9 Segment-Umschalter

- **Anatomie:** Behälter `surface.1`, Rand, Radius 16, Innenabstand 4 px · 2–4 gleich breite Segmente, Höhe 48 px, Radius 12, Text 17 px/600, optional Icon 18 px.
- **Zustände:** gewählt: Fläche `gradient.action-primary` mit schwarzer Schrift (neutrale/positive Wahl) oder `surface.inverse` mit schwarzer Schrift (Gegenwahl) · nicht gewählt: transparent, `text.secondary`.
- **Barrierefreiheit:** `role="radiogroup"` mit `role="radio"`/`aria-checked` und Pfeiltasten, oder echte `input type="radio"`. Wechsel wirkt sofort; der geänderte Inhalt folgt im DOM direkt danach. Für Ansichtswechsel mit eigenem Inhalt → Tabs (6.17).

### 6.10 Checkliste

- **Anatomie:** Gruppe als Karte mit `fieldset`/`legend` (Eyebrow-Stil) · Zeile: Kästchen 26 px (Radius 7, Rand 1,5 px `border.control`; im dunklen Theme weiß zulässig) · Label in gesperrten Versalien (`text.label`) · grauer Erklärtext (15 px). Zeilenhöhe mindestens 56 px, ganze Zeile klickbar.
- **Zustände:** abgehakt: Fläche und Rand `status.success.base`, Haken `status.success.on`, zeichnet sich in 200 ms · Fokus: Ring um die ganze Zeile · deaktiviert · Fehler (Pflichtpunkt offen): Rand `status.danger.base` + Text.
- **Kopf:** Zähl-Leiste + „0 von 23“ + leiser Link „Zurücksetzen“ (fragt nach). Hinweis, wo der Stand gespeichert wird.
- **Barrierefreiheit:** echtes `input type="checkbox"`, visuell überlagert; Label und Erklärtext sind beide mit dem Feld verknüpft (`label` + `aria-describedby`). Der Erklärtext trägt den vollständigen Wortlaut – das Versalien-Label ist nur Kurzform. Abgehakt ist an Haken **und** Farbe erkennbar.

### 6.11 Akkordeon

- **Anatomie:** `details`/`summary` · Kopfzeile mindestens 52 px (in Listen 60 px), Titel 17 px/700, rechts Plus-Icon 16 px, das sich beim Öffnen um 45° zum Kreuz dreht · Inhalt mit 12 px Abständen · Trennlinien zwischen Einträgen.
- **Varianten:** in Karte (Liste von Einträgen) · eingesetzt (`surface.2`, Radius 16, „Darauf achten“ in Schritt-Karten).
- **Regeln:** nie Warnungen oder Pflichtinformation einklappen. Mobil ersetzt das Akkordeon breite Tabellen (ein Eintrag je Zeile, Spaltenköpfe als Labels).
- **Barrierefreiheit:** natives `details` liefert Tastatur und Zustand. Im Druck geöffnet.

### 6.12 Tabelle

- **Anatomie:** Kopfzeile (`text.label` in `text.secondary`, keine Füllung) · Zeilen mit waagrechter Haarlinie `border.subtle` · erste Spalte als Zeilenkopf (`th scope="row"`, fett, weiß) · keine senkrechten Linien, keine Zebrastreifen.
- **Dichten:** bequem 52 px/15 px (Website) · kompakt 40 px/14 px (Dashboard-Standard) · dicht 32 px/13 px (Dashboard, viele Zeilen, nur Zeigergerät).
- **Ausrichtung:** Text links, Zahlen rechts mit `tabular-nums`, Einheit im Spaltenkopf, Status als Badge.
- **Zustände:** Zeilen-Hover `surface.2` (nur wenn Zeilen klickbar) · ausgewählt `surface.3` + Kästchen · sortiert: Pfeil-Icon im Kopf + `aria-sort` · klebender Kopf (`z.sticky`, Fläche der Karte).
- **Varianten:** in Karte (Innenabstand 8/24) · responsiv: unter `lg` Akkordeon oder waagrecht scrollbar mit fixierter erster Spalte.
- **Barrierefreiheit:** `caption` (darf visuell versteckt sein), `th scope`. Scrollbarer Behälter ist fokussierbar und benannt. Sortierköpfe sind `button`.

### 6.13 Hinweis / Callout

| Variante | Rand | Icon + Wort | Einsatz |
|---|---|---|---|
| Neutral | `border.subtle` | – | Merksatz, „Gut zu wissen“ |
| Info | `status.info.border` | Kreis-i + „Hinweis“ | Zusatzinformation |
| Erfolg | `status.success.border` | Haken + „Richtig“ | bestätigtes Ergebnis |
| **Warnung** | `status.warning.base`, 1 px umlaufend | Warndreieck + „Vorsicht“/„Achtung“ | Risiko für Person, Daten oder Gerät |
| Fehler | `status.danger.border` | Kreuz + „Falsch“/„Fehler“ | falsche Ausführung, Systemfehler |

- **Anatomie:** Karte · Kopfzeile mit Icon 20 px (gefüllt in Statusfarbe) und Label (`text.label`, weiß) · Titel optional · Text 16–17 px in `text.body` · optional Liste mit Punkten in Statusfarbe. Fläche bleibt `surface.1`; `status.*.subtle` nur für kompakte Banner und Badges.
- **Warnung, Zusatzregeln:** steht **vor** dem Schritt, den sie betrifft; volle Textlänge; nie einklappbar, nie in Versalien, nie nur als Icon; höchstens drei Regeln je Karte, das Wichtigste zuerst.
- **Barrierefreiheit:** Statuswort als Text. Statische Hinweise brauchen keine Rolle; nachträglich erscheinende Fehler `role="alert"`, Bestätigungen `role="status"`.

### 6.14 Bottom-Sheet

- **Anatomie:** Fläche `surface.1`, Rand, Radius 28 px oben · Grabber 36 × 5 px (`text.faint`) · zentrierte fette Aufforderung (22 px/700, `text-wrap: balance`) · Primär-Button volle Breite · optional leiser Link. Höchstbreite 520 px.
- **Varianten:** **im Fluss** (Standard: Inhaltsblock am Ende eines Abschnitts, gleitet 40 px ein) · klebend (am unteren Rand, `z.sheet`) · **modal** (über `surface.scrim`, `shadow.sheet`).
- **Barrierefreiheit:** im Fluss und klebend: normaler Inhalt, kein Fokusfang. Modal: `dialog` mit `aria-labelledby`, Fokus hinein und zurück, Escape schließt, Hintergrund inert; der Grabber ist dann Dekor, Schließen braucht einen Button. Klebende Sheets dürfen Inhalte und Fokus nicht verdecken (`scroll-padding-bottom`).

### 6.15 Navigation / Top-Bar

- **Anatomie:** klebend, Höhe 72 px (ab `lg` 76 px), Fläche `surface.bar` mit `blur.bar` 20 px, `z.topbar` · Website: Kapitelleiste + Zeile (Kapitelname, Leistenlink) · Dashboard: Wortmarke links, Bereichs-Tabs mittig, Werkzeuge rechts (Suche, Zeitraum, Konto).
- **Varianten:** Seitenleiste (Dashboard ab `lg`): Einträge 44 px, Icon 22 px + Text 15 px; aktiv: `surface.2`, weißer Text, 3 px gelber Strich links; eingeklappt nur Icons mit Tooltip.
- **Barrierefreiheit:** `header` + `nav` mit Namen; Sprunglink „Zum Inhalt“ als erstes Element (`z.skip`, gelbe Fläche). `aria-current="page"` am aktiven Eintrag. `scroll-padding-top` = Leistenhöhe + 12 px. Ohne `backdrop-filter` deckende Fläche.

### 6.16 Formularfelder

- **Anatomie:** Label oben (`text.label`, `text.secondary`) · Feld: Höhe 52 px (Dashboard 44/36), Fläche `surface.1` (auf Karte `surface.2`), Rand 1,5 px `border.control`, Radius 14 px, Text 17 px, Innenabstand 16 px · Hilfetext unten (14 px, `text.muted`) · Fehlertext unten (14 px, `status.danger.text`, mit Icon).
- **Typen:** Text, Zahl, Textbereich (mind. 3 Zeilen), Auswahl (natives `select` mit Pfeil-Icon), Suche (Lupen-Icon links), Datum/Zeitraum, Checkbox (6.10), Radio (26 px rund, Punkt 10 px), Schalter (52 × 32 px, an = `status.success.base`, mit sichtbarem Wort), Regler (Spur 3 px, Griff 26 px weiß).
- **Zustände:** Ruhe · Hover: Rand `text.muted` · Fokus: Rand `accent.line` + Fokusring · gefüllt · Fehler: Rand `status.danger.base` + Text · deaktiviert: Fläche `action.disabled.bg`, Text `action.disabled.fg` · nur lesen: ohne Rand, Text weiß.
- **Regeln:** Platzhalter ist kein Label (Farbe `text.faint`). Pflichtfelder: Wort „Pflichtfeld“ oder „(optional)“ am selteneren Fall, kein Sternchen allein. Prüfung beim Verlassen des Feldes, nicht beim Tippen. Einspaltig; Breite deutet die erwartete Länge an.
- **Barrierefreiheit:** `label for`, Fehler per `aria-describedby` + `aria-invalid`, `autocomplete`-Attribute, Fehlerübersicht oben bei Absenden mit Sprunglinks.

### 6.17 Tabs

- **Anatomie:** Zeile aus Reitern, Text 15 px/600 (Website 17 px), Höhe 44 px, Abstand 24 px · aktiv: weißer Text + 2 px Strich `accent.line` unten · inaktiv: `text.muted` · Haarlinie unter der ganzen Zeile.
- **Varianten:** Unterstrich (Standard, Dashboard-Bereiche) · Pillen/Chips (Filter: Höhe 44 px, Rand, gewählt weiß mit schwarzer Schrift, `aria-pressed`) · bei Platzmangel waagrecht scrollbar mit Ausblendung am Rand.
- **Abgrenzung:** Tabs wechseln **Ansichten**; der Segment-Umschalter wechselt **einen Wert**; Chips **filtern**.
- **Barrierefreiheit:** `role="tablist"/"tab"/"tabpanel"`, Pfeiltasten wechseln, `aria-selected`, Panel fokussierbar. Aktiv ist an Strich **und** Helligkeit erkennbar.

### 6.18 Tooltip

- **Anatomie:** Fläche `surface.overlay` (deckend genug: 90 %), Rand `border.strong`, Radius 10 px, Innenabstand 8/12 px, Text 13 px `text.primary`, `shadow.overlay`, Höchstbreite 260 px, Abstand 8 px, `z.tooltip`.
- **Varianten:** Text-Tooltip (benennt Icon-Buttons) · Daten-Tooltip (Diagramm: Datum als Label, je Reihe Farbmarke 8 px + Name + Wert rechtsbündig).
- **Verhalten:** erscheint nach 300 ms bei Hover und sofort bei Fokus; bleibt, solange Zeiger auf Auslöser oder Tooltip; Escape schließt.
- **Barrierefreiheit:** nie für nötige Information und nie als einziger Name. `role="tooltip"` + `aria-describedby`. Auf Touch gibt es keinen Hover: Inhalt muss anders erreichbar sein.

### 6.19 Badge / Pill

- **Anatomie:** Höhe 24 px (Chip-Größe 28 px), Radius Pille, Innenabstand 0/10 px, Text `text.chip` (11 px, Versalien, 0,12 em).
- **Varianten:** neutral (`surface.overlay` + Rand `border.strong`, Text weiß) · Akzent (Fläche Gelb, Text Schwarz) · Status (Fläche `status.*.subtle`, Rand `status.*.border`, Text `status.*.text`, mit Punkt oder Icon) · gefüllt (Fläche `status.*.base`, Text `status.*.on`) · Zähler (rund, mind. 20 px).
- **Regeln:** ein bis zwei Wörter. Badges sind nicht klickbar (klickbar = Chip mit 44 px).
- **Barrierefreiheit:** Statuswort immer als Text; Zähler bekommen Kontext („3 neue Meldungen“).

### 6.20 Label für 3D und Diagramme

- **Anatomie:** Pille wie Badge neutral (11 px, 600, 0,12 em, Versalien, Innenabstand 6/11 px) · Hinweislinie 1 px in `lineart.dim`, 8–44 px lang, vom Label zum Ankerpunkt · optional Ankerpunkt 3 px in `accent.fill`.
- **Varianten:** neutral · betont (Fläche Gelb, Schrift Schwarz – genau ein Label je Ansicht) · Problem (Text `status.danger.text`, Rand `status.danger.base`) · falsch (Fläche `status.danger.base`, Schrift Schwarz) · nummerierte Marke (Kreis 19 px Gelb mit schwarzer Ziffer 11,5 px/700; Legende als Liste darunter – Pflicht auf schmalen Flächen).
- **Regeln:** Labels überdecken das Objekt nicht und einander nicht; bei Platzmangel Marken + Legende. Höchstens sieben Labels gleichzeitig. Ein- und Ausblenden 250 ms.
- **Barrierefreiheit:** Labels im Overlay sind `aria-hidden`; dieselbe Information steht als Text oder versteckte Liste daneben.

### 6.21 Diagramm-Rahmen

- **Anatomie:** Karte · Kopf: Label (Eyebrow-Stil) + Titel als Aussage (`text.title` oder 17 px/600) + optional Zweitsatz · Werkzeugzeile rechts (Zeitraum, Ansicht „Diagramm | Tabelle“) · Legende · Zeichenfläche · Fußzeile: Quelle und Stand (`text.caption`, `text.faint`).
- **Größen:** Zeichenfläche mindestens 200 px hoch; Seitenverhältnis 16:9 bis 2:1, Sparklines 4:1.
- **Zustände:** laden (6.24) · leer (6.23) · Fehler (Callout Fehler in der Zeichenfläche, mit „Erneut laden“).
- **Barrierefreiheit:** `figure` + `figcaption`; Zeichenfläche `role="img"` mit `aria-label`, das die Aussage nennt; Tabellenansicht für jedes Diagramm. Regeln für das Innere in 8.

### 6.22 Icon-Kachel

- **Anatomie:** Quadrat 72 px (ab `md` 88 px, Hero/Folie 96 px), Radius 20–22 px, Icon 44–52 px als Line-Art, Strich 2,4 px, runde Enden.
- **Varianten:** dunkel (`gradient.tile-dark`, Rand, Icon in `accent.line`) · gelb (`gradient.tile-accent`, Icon in `accent.on-tile`, ohne Rand) · klein 44 px (Listen, Dashboard; Radius 12, Icon 22 px, Strich 2 px).
- **Regeln:** höchstens eine Kachel je Abschnitt, über dem Eyebrow. Gelbe Variante für den Hauptmoment, dunkle für alles andere.
- **Barrierefreiheit:** dekorativ (`aria-hidden`), wenn der Text daneben dasselbe sagt.

### 6.23 Leerzustand

- **Anatomie:** zentriert in der Fläche, die sonst den Inhalt trägt · dunkle Icon-Kachel oder kleine Line-Art (höchstens 120 px) · Titel in normaler Schreibweise (20 px/700) · ein Satz in `text.muted` · höchstens ein Button (Sekundär oder Ghost; Primär nur, wenn dies die Haupthandlung der Seite ist).
- **Varianten:** noch nichts angelegt · Filter ohne Treffer („Filter zurücksetzen“) · keine Berechtigung · Fehler beim Laden (→ Callout Fehler).
- **Regeln:** sagt, was fehlt, und den nächsten Schritt. Keine Versalien-Headline, keine Witze.

### 6.24 Ladezustand

- **Varianten:** Ladekreis 14 px (Rand 2 px, Spur Weiß 25 %, Bogen `accent.line`, 900 ms linear) in einer Pille mit Text „Lädt …“ – für Bühnen und Buttons · Skelett: Flächen in `surface.2` mit den Radien des späteren Inhalts, Textzeilen 12 px hoch mit Radius 6 px, Puls der Deckkraft 1 → 0,6 in 1200 ms – für Karten, Tabellen, Diagramme · Fortschritt mit Zähl-Leiste, wenn die Dauer bekannt ist.
- **Regeln:** unter 300 ms nichts zeigen; ab 1 s Skelett; ab 10 s Text mit Erklärung und Abbruch. Skelett hat die Maße des Inhalts – kein Springen. Schwere Inhalte (3D) erst auf Wunsch laden: Standbild + Button „3D laden (12 MB)“.
- **Barrierefreiheit:** Behälter `aria-busy="true"`; eine Meldung über `role="status"`. Mit reduzierter Bewegung: Ladekreis langsam (3 s), Skelett ohne Puls.

### 6.25 Weitere Bausteine

- **Listen-Karte:** Punkte 7 px in `accent.fill`, Zeilen durch Haarlinien getrennt. Nummerierte Liste: Ziffer 20 px/600 weiß in 32-px-Spalte.
- **Fakten-Liste:** `dl` mit Label oben und Wert darunter, Haarlinie je Eintrag; ab `lg` zweispaltig.
- **Chips:** siehe 6.17. **Wortmarke:** `text.wordmark`, unten links auf der Signet-Karte und im Fuß.
- **Fußbereich:** Haarlinie oben, 13 px in `text.muted`, Quellenliste mit weißen Links, nummerierte Anmerkungen.
- **Toast** (neu): unten mittig, `surface.overlay`, Radius 14, 15 px, höchstens zwei Zeilen, verschwindet nach 5 s, `role="status"`; für Fehler stattdessen Callout an Ort und Stelle.
- **Dialog** (neu): wie modales Bottom-Sheet; ab `md` zentriert, Breite 520 px, Radius 28 px rundum.

---

## 7. Dashboards

### 7.1 Grundsätze

- Ein Dashboard beantwortet **eine Frage je Seite**. Die Headline nennt sie („UMSATZ“), der Zweitsatz den Stand („Stand 17.11.2026, 09:00 Uhr · alle Märkte“).
- Schwarz bleibt Grund, Karten tragen Inhalte. Gelb markiert **eine** Sache: die betonte Kennzahl oder die betonte Reihe.
- Status (gut/schlecht) ist selten. Die meisten Zahlen sind neutral weiß.
- Filter stehen in **einer Zeile** über den Diagrammen und wirken auf alles darunter. Reihenfolge: Zeitraum → Dimension → Vergleich.

### 7.2 KPI-Muster

| Muster | Aufbau | Wann |
|---|---|---|
| **KPI-Reihe** | 4 Kacheln à 3 Spalten: Label · Wert (28–36 px) · Veränderung | Standard-Kopf jeder Seite |
| **Leit-KPI** | 1 Kachel à 6 Spalten mit Wert 48–64 px in Gelb + Sparkline, daneben 2–3 kleine | wenn eine Zahl führt |
| **KPI mit Ziel** | Wert · Zähl-Leiste oder Balken zum Ziel · „82 % von 1.200“ | Fortschritt auf ein Ziel |
| **KPI mit Sparkline** | Wert · Linie 4:1, 2 px, ohne Achsen, letzter Punkt markiert | Verlauf ohne Details |
| **KPI-Gruppe** | 2 × 2 mit Haarlinien in einer Karte, Wert 17 px/600 | Eckdaten, nicht messend |

Regeln: höchstens **6 KPIs** je Seite sichtbar · jede Zahl mit Einheit, Zeitraum und Bezug der Veränderung · Vergleich immer benannt („ggü. Vormonat“) · große Zahlen kürzen (1,2 Mio.), exakter Wert im Tooltip und in der Tabelle · fehlender Wert: Halbgeviertstrich „–“ mit Erklärung, nie „0“.

### 7.3 Welches Diagramm wann

| Aufgabe der Daten | Form | Nicht |
|---|---|---|
| eine Zahl | KPI-Kachel | Tacho, Ring |
| Verlauf über Zeit | Linie (bis 4 Reihen); Fläche nur bei einer Reihe oder gestapelten Anteilen | Säulen für lange Zeitreihen |
| Vergleich von Kategorien | waagrechte Balken, sortiert | Kreis, senkrechte Säulen mit schrägen Beschriftungen |
| Vergleich über wenige Zeitpunkte | Säulen (bis 12) | – |
| Anteile an einem Ganzen | gestapelter Einzelbalken (bis 5 Teile) oder sortierte Balken | Kreis/Ring mit mehr als 3 Teilen, 3D |
| Verteilung | Histogramm, Boxplot als Strich + Punkt | – |
| Zusammenhang zweier Größen | Streudiagramm (höchstens 5 Farben, hell 3) | – |
| Abweichung von Ziel/Null | Balken ab Nulllinie in divergierenden Farben | Rot/Grün ohne Vorzeichen |
| Größe über zwei Dimensionen | Heatmap in der sequenziellen Palette | Regenbogen |
| Rang im Zeitverlauf | Steigungsdiagramm (zwei Zeitpunkte) | – |
| Ablauf/Trichter | Balken in abgestufter Einzelfarbe (ordinal) | bunte Stufen |
| viele Reihen | kleine Vielfache mit gleicher Achse | eine Linie je Farbe ab der 8. Reihe |

**Nie:** zwei y-Achsen, 3D, Verläufe in Datenflächen, Kreisdiagramme mit mehr als 3 Teilen, abgeschnittene Balkenachsen.

### 7.4 Dichte

| Stufe | Zeilenhöhe | Text | Karteninnenabstand | Bedienhöhe | Einsatz |
|---|---|---|---|---|---|
| bequem | 52 px | 15 px | 24 px | 52/44 px | Website, Touch, Vorführung |
| kompakt (Standard) | 40 px | 14 px | 16 px | 44/36 px | Dashboard am Schreibtisch |
| dicht | 32 px | 13 px | 12 px | 36/28 px | Tabellen mit vielen Zeilen, nur Zeigergerät |

Die Dichte ist eine Einstellung der Seite (`data-density="comfortable|compact|dense"`), nicht einzelner Karten. Auf Touch-Geräten gilt immer „bequem“. Unter 13 px Text wird nie gegangen; Achsentext 12 px ist die einzige Ausnahme.

---

## 8. Diagramme (alle Medien)

### 8.1 Farbe

| Aufgabe | Palette | Token |
|---|---|---|
| Zugehörigkeit (welche Reihe) | kategorial, 7 Farben in fester Reihenfolge | `dataviz.categorical.1–7` |
| Menge (wie viel) | sequenziell, eine Farbe, 6 Stufen | `dataviz.sequential.1–6` |
| Richtung (über/unter Basis) | divergierend, Blau ↔ Grau ↔ Orange | `dataviz.diverging.neg-3 … pos-3` |
| Zustand (gut/schlecht) | Statusfarben, mit Icon und Wort | `dataviz.positive/negative` |
| betonen | eine Reihe Gelb, Rest grau | `dataviz.highlight`, `dataviz.context` |

**Kategorial** (Kontrast auf Grund / Karte):

| Slot | Farbe | Dunkel | Kontrast | Hell | Kontrast |
|---|---|---|---|---|---|
| 1 | Gelb / Gold | #FFE94D | 17,01 / 13,79 | #A67C00 | 3,82 / 3,50 |
| 2 | Blau | #4797FF | 7,14 / 5,78 | #1F6FE0 | 4,76 / 4,37 |
| 3 | Pink | #EC3A78 | 5,44 / 4,41 | #C2185B | 5,87 / 5,39 |
| 4 | Türkis | #2FCFC2 | 10,83 / 8,77 | #0C968B | 3,65 / 3,35 |
| 5 | Orange | #F5893A | 8,52 / 6,90 | #D9641A | 3,63 / 3,33 |
| 6 | Violett | #B9A1FF | 9,60 / 7,78 | #7A5AE0 | 4,81 / 4,42 |
| 7 | Grün | #8FD46A | 11,79 / 9,56 | #3F8F1F | 4,07 / 3,74 |
| – | Sonstige | #8E8E93 | 6,44 / 5,22 | #86868B | 3,62 / 3,33 |

Einmalig geprüft mit dem Paletten-Validator der Datenvis-Skill (`validate_palette.js`: OKLab-ΔE × 100, Farbfehlsichtigkeit simuliert nach Machado 2009). Dieser Validator liegt nicht im Ordner; `check_tokens.py` prüft nur die Kontraste. Wer eine Diagrammfarbe ändert, muss die Unterscheidbarkeit neu prüfen. Ergebnis:

- **Dunkel:** benachbarte Slots Rot-Grün-Schwäche ΔE ≥ 13,7 (Ziel ≥ 8), Normalsicht ≥ 25,4 (Untergrenze 15). Alle Paare untereinander bestehen für die **ersten fünf** Slots; mit allen sieben fallen Blau↔Violett (6,1) und Türkis↔Grün (12,7) darunter.
- **Hell:** benachbart ΔE ≥ 8,1; alle Paare nur für die **ersten drei** Slots.
- **Bewusste Abweichung:** Der Validator verlangt ein gemeinsames Helligkeitsband; das Gelb (OKLCH-L 0,93) liegt darüber, die übrigen Slots liegen bei 0,62–0,79. Das ist gewollt: Slot 1 ist die betonte Reihe. Wer gleich gewichtete Reihen braucht, beginnt bei Slot 2.

Folgen daraus:

- Reihenfolge fest, **nie umsortieren, nie zyklisch wiederholen**. Farbe folgt der Sache, nicht dem Rang – ein Filter färbt die verbleibenden Reihen nicht um.
- Linien, Balken, Stapel (nur Nachbarn berühren sich): bis 7 Reihen. Streudiagramm, Karte, kleine Vielfache: dunkel höchstens 5, hell höchstens 3 Farben.
- Ab der 8. Reihe: „Sonstige“ in `dataviz.neutral` oder kleine Vielfache.
- Pink, Orange und Grün der Palette sind **keine** Statusfarben. Bedeutet eine Reihe gut/schlecht, trägt sie Statusfarben – nie beides in einem Diagramm.
- Sequenziell auf Dunkel: dunkel = wenig, hell (Gelb) = viel; auf Hell umgekehrt. Schwächste Stufe ≥ 2:1 zur Karte (2,17 / 2,05).
- Divergierend: Mitte ist neutrales Grau (2,22:1 zur Karte), nie eine Farbe. Blau/Orange statt Rot/Grün.
- Druck in Schwarzweiß und erzwungene Farben: zusätzlich Strichmuster (durchgezogen, gestrichelt 6/5, gepunktet) bzw. Schraffur 45°/135°.

### 8.2 Achsen, Gitter, Legende, Tooltip

- **Zeichenfläche:** Fläche der Karte, kein eigener Rahmen.
- **Gitter:** nur waagrecht (bei waagrechten Balken nur senkrecht), 1 px `dataviz.grid`, 3–5 Linien. Nulllinie 1 px `dataviz.axis`.
- **Achsen:** keine Achsenlinie außer der Basis, keine Teilstriche. Text `text.caption` in `dataviz.axis-text` (6,44:1), `tabular-nums`. Einheit einmal oben an der Achse, nicht an jedem Wert. Höchstens 6 Werte je Achse. Zeitachse: „Jan, Feb, …“ und Jahr nur beim Wechsel. Balken beginnen **immer bei null**.
- **Marken:** Linie 2 px, runde Enden und Ecken; Punkte ab 8 px mit 2-px-Ring in Flächenfarbe · Balken: Radius 4 px am Datenende, eckig an der Basis; zwischen Flächen 2 px Fuge in `dataviz.gap` · Balkenbreite höchstens 48 px · Flächen unter Linien 16 % Deckkraft, ohne Verlauf.
- **Beschriftung:** bis 4 Reihen direkt am Linienende beschriften (Name in `dataviz.label`, davor Farbmarke). Nicht jeder Punkt bekommt eine Zahl – nur Endwert, Höchst-/Tiefstwert oder der betonte Punkt. **Text trägt nie die Reihenfarbe.**
- **Legende:** ab 2 Reihen immer, oben links über der Zeichenfläche, eine Zeile, Farbmarke 8 px (Linie: Strich 12 × 2 px) + Name 13 px. Bei einer Reihe keine Legende – der Titel benennt sie. Legendeneinträge sind Schalter (`aria-pressed`), die Reihen aus- und einblenden.
- **Tooltip:** Linie/Fläche: senkrechtes Fadenkreuz 1 px `dataviz.cursor` + Daten-Tooltip mit allen Reihen am Zeitpunkt · Balken/Punkt/Zelle: Tooltip je Marke. Trefferfläche größer als die Marke (mindestens 24 px). Tooltip per Tastatur erreichbar (Pfeiltasten wandern durch die Punkte).
- **Anmerkungen:** Ereignisse als senkrechte gestrichelte Linie (`lineart.dim`) mit Label-Pille (6.20). Zielwert als waagrechte gestrichelte Linie mit Label rechts.
- **Barrierefreiheit:** Tabellenansicht für jedes Diagramm · `aria-label` nennt die Aussage, nicht „Diagramm“ · Farbe nie alleiniger Träger (Direktbeschriftung, Strichmuster, Reihenfolge der Legende = Reihenfolge im Diagramm).

---

## 9. Präsentationen (PowerPoint, 16:9)

Maschinenlesbar in `tokens/pptx.json` (Zoll und EMU). Diese Tabellen sind daraus erzeugt.

### 9.1 Grundlagen

- **Format:** 13,333 × 7,5 in (12192000 × 6858000 EMU). 96 px der Website entsprechen 1 in auf der Folie.
- **Raster:** 12 Spalten · Rand links/rechts 0,667 in · Lücke 0,2 in · Spalte 0,817 in · Inhaltsbreite 12,0 in. Positionen auf 0,05 in runden.

| Spalte beginnt bei (in) | 1: 0,667 | 2: 1,683 | 3: 2,7 | 4: 3,717 | 5: 4,733 | 6: 5,75 | 7: 6,767 | 8: 7,783 | 9: 8,8 | 10: 9,817 | 11: 10,833 | 12: 11,85 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Breite über n Spalten (in)** | 0,817 | 1,833 | 2,85 | 3,867 | 4,883 | 5,9 | 6,917 | 7,933 | 8,95 | 9,967 | 10,983 | 12,0 |

- **Zonen** (y / Höhe in Zoll, x 0,667, Breite 12,0):

| Zone | y | Höhe | Inhalt |
|---|---|---|---|
| Fortschrittsleiste | 0,30 | 0,04 | ein Segment je Kapitel, Lücke 0,08 in; erledigt/aktiv Weiß, offen #616161 |
| Eyebrow | 0,62 | 0,30 | 12 pt Versalien |
| Headline | 0,95 | 0,70 | 28 pt Versalien, eine Zeile, höchstens 34 Zeichen |
| Zweitsatz | 1,65 | 0,45 | 18 pt grau, Breite 9 Spalten |
| Inhalt | 2,35 | 4,30 | bis y 6,65 |
| Seitenfuß | 6,95 | 0,25 | Wortmarke links · Quelle mittig-rechts (optional) · Seitenzahl rechts; 10 pt |

- **Farben:** Thema „ODSV Dark“: `dk1` 000000 · `lt1` FFFFFF · `dk2` 1C1C1E · `lt2` A1A1A6 · `accent1–6` FFE94D, 4797FF, EC3A78, 2FCFC2, F5893A, B9A1FF · `hlink` FFE94D · `folHlink` CCCCCC. Im Folienmaster die Farbzuordnung umkehren: `bg1=dk1, tx1=lt1, bg2=dk2, tx2=lt2` – so ist „Hintergrund 1“ schwarz, „Text 1“ weiß, „Hintergrund 2“ die Karte und „Text 2“ der graue Zweitsatz. Thema „ODSV Light“ (Druck, helle Räume): `dk2` 58585C · `lt2` F5F5F7 · `accent1–6` A67C00, 1F6FE0, C2185B, 0C968B, D9641A, 7A5AE0 · `hlink` 6B5800 · `folHlink` 58585C; Zuordnung `bg1=lt1, tx1=dk1, bg2=lt2, tx2=dk2`.
- **Schriften:** Überschriften **Arial**, Text **Arial**, Mono Consolas (Ersatz Courier New). Begründung:
  1. Ein PowerPoint-Thema kennt je Rolle genau eine Schrift, keine Ersatzkette. Fehlt sie, ersetzt PowerPoint stillschweigend – gesperrte Versalien brechen dann anders um.
  2. SF Pro und Inter sind auf Windows nicht vorhanden; SF Pro darf nicht weitergegeben oder eingebettet werden. Helvetica Neue gibt es nur auf macOS.
  3. Arial ist die einzige neutrale Grotesk, die auf Windows und macOS ohne Installation da ist.
  4. Helvetica Neue ist zulässig, wenn das Deck nur auf dem Mac gezeigt oder als PDF verteilt wird.
  5. Arial hat kein Halbfett: Headlines stehen in Fett; die Sperrung nimmt die Schwere zurück.
- **Laufweite:** PowerPoint misst absolut in 1/100 pt: `spc = Größe in pt × Laufweite in em × 100`. Beispiele: 12 pt bei 0,2 em → 240 · 28 pt bei 0,15 em → 420 · 44 pt bei 0,2 em → 880 · 54 pt bei 0,2 em → 1080. Folien-Headlines laufen mit 0,15 em statt 0,2 em, damit 34 Zeichen in eine Zeile passen.
- **Formen:** Karten als abgerundetes Rechteck, Füllung Karte (1C1C1E), Linie 0,75 pt (2C2C2E), **kein Schatten**. Radius: Karte 0,28 in · kleine Karte 0,20 in · Kachel 0,23 in · Button 0,15 in. Einstellwert: `adj = Radius ÷ kürzere Seite × 100000`. Innenabstand 0,30 in, Abstand zwischen Karten 0,20 in. Linien: Haarlinie 0,75 pt · Line-Art 2,25 pt, runde Enden.
- **Textmenge:** Fließtext mindestens 16 pt, Beschriftungen mindestens 12 pt, Seitenfuß 10 pt (keine Pflichtinformation). Höchstens 5 Listenpunkte oder 80 Wörter je Folie.
- **Bewegung:** Folienübergang „Überblenden“ 0,3 s oder keiner. Einblenden nur „Verblassen“ 0,3 s, schrittweise bei Prozess-Folien. Keine Pfade, kein Zoom, kein Morph als Effekt.
- **Barrierefreiheit:** jede Folie hat einen eindeutigen Titel im Titelplatzhalter (bei der KPI-Folie ist das Label der Titel, bei der Bildfolie die Headline) · Lesereihenfolge im Auswahlbereich von oben nach unten prüfen · Alternativtext für Bilder, Diagramme und Line-Art; Dekor als „dekorativ“ markieren · Versalien über die Zeichenformatierung, nicht getippt.

### 9.2 Textstile

| Stil | Schrift | pt | Schnitt | Versalien | Laufweite | spc | Zeilenabstand | Farbe |
|---|---|---|---|---|---|---|---|---|
| display | major | 44 | fett | ja | 0,2 em | 880 | 1,15 | text.primary |
| chapter | major | 54 | fett | ja | 0,2 em | 1080 | 1,15 | text.primary |
| headline | major | 28 | fett | ja | 0,15 em | 420 | 1,2 | text.primary |
| eyebrow | minor | 12 | normal | ja | 0,2 em | 240 | 1,2 | text.secondary |
| sub | minor | 18 | normal | – | 0 | 0 | 1,3 | text.muted |
| sub-large | minor | 24 | normal | – | 0 | 0 | 1,3 | text.muted |
| body | minor | 18 | normal | – | 0 | 0 | 1,4 | text.body |
| body-small | minor | 16 | normal | – | 0 | 0 | 1,35 | text.body |
| body-small-muted | minor | 16 | normal | – | 0 | 0 | 1,35 | text.muted |
| card-title | major | 20 | fett | – | 0 | 0 | 1,2 | text.primary |
| label | minor | 11 | normal | ja | 0,15 em | 165 | 1,2 | text.secondary |
| kpi-hero | major | 120 | fett | – | 0 | 0 | 1 | accent.text |
| kpi | major | 54 | fett | – | 0 | 0 | 1 | text.primary |
| kpi-tile | major | 28 | fett | – | 0 | 0 | 1,1 | text.primary |
| number-large | major | 72 | fett | – | 0 | 0 | 1 | text.primary |
| number | major | 40 | fett | – | 0 | 0 | 1 | text.primary |
| quote | minor | 32 | normal | – | 0 | 0 | 1,3 | text.primary |
| prompt | major | 28 | fett | – | 0 | 0 | 1,2 | text.primary |
| agenda | minor | 24 | normal | – | 0 | 0 | 1,2 | text.primary |
| table | minor | 14 | normal | – | 0 | 0 | 1,2 | text.body |
| table-head | minor | 11 | normal | ja | 0,15 em | 165 | 1,2 | text.secondary |
| chart-axis | minor | 12 | normal | – | 0 | 0 | 1,2 | text.faint |
| chart-label | minor | 12 | normal | – | 0 | 0 | 1,2 | text.secondary |
| chip | minor | 10 | fett | ja | 0,12 em | 120 | 1,2 | text.primary |
| button | minor | 18 | fett | – | 0 | 0 | 1,2 | accent.on |
| caption | minor | 12 | normal | – | 0 | 0 | 1,2 | text.faint |
| footer | minor | 10 | normal | ja | 0,14 em | 140 | 1,2 | text.faint |
| code | mono | 14 | normal | – | 0 | 0 | 1,2 | text.body |

`major`/`minor` = Überschriften-/Textschrift des Themas. Farben sind Rollen aus `pptx.json → themes.*.roles`.

### 9.3 Layout-Katalog

Alle Maße in Zoll, Ursprung oben links. Wo „Fortschrittsleiste: ja“ steht, liegt sie in der Zone aus 9.1; Eyebrow, Headline und Zweitsatz stehen dann an den Standardpositionen.

#### 9.3.1 Titel (`title`)

Erste Folie. Signet-Moment. Fortschrittsleiste: nein · Seitenfuß: nein

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 2,25 | 6,917 | 0,3 | eyebrow · 12 pt | – |
| title | 0,667 | 2,65 | 6,917 | 1,75 | display · 44 pt | max. 12 Zeichen/Zeile; 2 Zeile(n) |
| sub | 0,667 | 4,55 | 5,9 | 0,9 | sub-large · 24 pt | – |
| meta | 0,667 | 6,35 | 5,9 | 0,3 | eyebrow · 12 pt | – |
| signet | 7,783 | 0,667 | 4,883 | 6,167 | card | Signet im Verlauf gradient.signet; Wortmarke unten links (0,3 in Innenabstand) |

- Einziger Ort für den Signet-Verlauf.
- Titel höchstens 2 Zeilen à 12 Zeichen; längere Titel: 36 pt / spc 720.
- Kein Seitenfuß, keine Fortschrittsleiste.

#### 9.3.2 Kapiteltrenner (`chapter`)

Beginn eines Kapitels. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| number | 9,817 | 0,62 | 2,85 | 1,2 | number-large · 72 pt | Ausrichtung right |
| eyebrow | 0,667 | 2,55 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 2,9 | 12 | 1,9 | chapter · 54 pt | max. 17 Zeichen/Zeile; 2 Zeile(n) |
| sub | 0,667 | 4,95 | 7,933 | 0,6 | sub-large · 24 pt | – |

- Kapitelnummer oben rechts wie bei der Schritt-Karte.
- Fortschrittsleiste zeigt das aktive Kapitel.
- Sonst leer – keine Bilder, keine Listen.

#### 9.3.3 Agenda (`agenda`)

Überblick, höchstens 6 Punkte. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| list | 0,667 | 2,35 | 7,933 | 4,2 | agenda · 24 pt | je Zeile: Nummer 24 pt (0,8 in breit, text.muted; aktiv accent.text) + Titel 24 pt; Haarlinie darunter |
| aside | 8,8 | 2,35 | 3,867 | 4,2 | card | Icon-Kachel oder Zeitangaben; optional |

- Mehr als 6 Punkte: Kapitel zusammenfassen.
- Als Zwischenstand wiederverwendbar: aktive Zeile weiß, übrige text.muted.

#### 9.3.4 Inhalt, eine Spalte (`content-1`)

Eine Aussage mit Begründung. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| body | 0,667 | 2,35 | 7,933 | 4,3 | body · 18 pt | höchstens 5 Punkte oder 80 Wörter |
| aside | 8,8 | 2,35 | 3,867 | 4,3 | card | Icon-Kachel, Hinweis-Karte oder leer; optional |

- Textspalte nie breiter als 8 Spalten (Lesebreite).
- Listenpunkte: gelber Punkt 0,08 in, Text 18 pt.

#### 9.3.5 Inhalt, zwei Spalten (`content-2`)

Zwei gleichrangige Gedanken. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| left | 0,667 | 2,35 | 5,9 | 4,3 | card | Label 11 pt · Karten-Headline 20 pt fett · Text 16 pt |
| right | 6,767 | 2,35 | 5,9 | 4,3 | card | – |

- Beide Karten gleich hoch.
- Variante 7 + 5 Spalten für Text + Bild/Illustration.

#### 9.3.6 KPI / Zahl groß (`kpi`)

Eine Zahl trägt die Folie. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| label | 0,667 | 1,95 | 12 | 0,3 | label · 11 pt | – |
| value | 0,667 | 2,3 | 12 | 2,1 | kpi-hero · 120 pt | Zahl in accent.text, Einheit/Vorsatz in text.primary |
| sentence | 0,667 | 4,5 | 7,933 | 0,7 | sub-large · 24 pt | – |
| tiles | 0,667 | 5,4 | 12 | 1,25 | kpi-tiles | 3 Kacheln à 4 Spalten: Label 11 pt, Wert 28 pt; optional |

- Keine Versalien-Headline – die Zahl ist die Headline.
- Zahl höchstens 9 Zeichen einschließlich Einheit bei 120 pt; sonst 96 pt.
- Quelle im Seitenfuß.

#### 9.3.7 Diagramm (`chart`)

Ein Diagramm, eine Kernaussage. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| chart | 0,667 | 2,35 | 7,933 | 4,3 | chart-frame | Diagramm-Rahmen: Karte, Plot innen 7,33 × 3,70 in |
| insight | 8,8 | 2,35 | 3,867 | 4,3 | insight | Label „KERNAUSSAGE“ 11 pt · Aussage 20 pt fett · Erläuterung 16 pt muted |

- Headline nennt die Aussage, nicht das Thema.
- Variante Vollbreite: Diagramm 12 Spalten, Aussage als Zweitsatz.
- Höchstens 4 Reihen direkt beschriftet; Legende oben links im Rahmen.

#### 9.3.8 Bild / Vollbild (`image`)

Foto, Rendering oder 3D-Standbild. Fortschrittsleiste: nein · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| image | 0 | 0 | 13,333 | 7,5 | image | randabfallend; darüber Verlauf gradient.fade-down gespiegelt (unten 45 % Höhe, Schwarz 0 → 85 %) |
| eyebrow | 0,667 | 5,3 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 5,63 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 6,3 | 8,95 | 0,45 | sub · 18 pt | – |

- Text steht nur auf dem abgedunkelten Bereich (Kontrast ≥ 4,5:1 prüfen).
- Variante „Bild in Karte“: Karte cx(6)…12, Text links 5 Spalten.
- Nur Seitenzahl im Fuß.

#### 9.3.9 Zitat (`quote`)

Eine Stimme, wörtlich. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| mark | 0,667 | 2,2 | 0,8 | 0,8 | lineart | Anführungszeichen als Line-Art in accent.line |
| quote | 1,683 | 2,1 | 9,967 | 2,9 | quote · 32 pt | max. 30 Wörter |
| name | 1,683 | 5,2 | 9,967 | 0,3 | eyebrow · 12 pt | – |
| role | 1,683 | 5,52 | 9,967 | 0,35 | body-small-muted · 16 pt | – |

- Normale Schreibweise, keine Versalien.
- Kein Porträt nötig; wenn doch: Kreis 1,0 in links neben dem Namen.

#### 9.3.10 Prozess / Schritte (`process`)

3 bis 5 Schritte in Reihenfolge. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| segments | 0,667 | 2,2 | 12 | 0,04 | segments | ein Segment je Schritt, Lücke 0,08 in |
| cards | 0,667 | 2,4 | 12 | 4,25 | step-cards | je Karte: Nummer 40 pt oben rechts · Line-Art 1,4 in hoch · Titel 20 pt fett · Satz 14 pt muted |

- 3 Schritte: je 4 Spalten (3,867 in); 4: je 3 Spalten (2,850 in); 5: je 2,240 in bei 0,2 in Lücke.
- Aktiver Schritt: Rand border.active, übrige Karten 45 % Deckkraft (nur beim schrittweisen Zeigen).

#### 9.3.11 Vergleich (`compare`)

Zwei Optionen, richtig/falsch, vorher/nachher. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| a | 0,667 | 2,35 | 5,9 | 4,3 | card | Kopf: Icon + Label · Titel 20 pt fett · bis zu 5 Zeilen 16 pt |
| b | 6,767 | 2,35 | 5,9 | 4,3 | card | – |

- Richtig/Falsch: Icon (Haken/Kreuz) + Wort, nie nur Grün/Rot.
- Empfohlene Option: Rand 1,5 pt accent.line.
- Zeilen beider Karten stehen auf gleicher Höhe.

#### 9.3.12 Tabelle (`table`)

Wenige, vergleichbare Werte. Fortschrittsleiste: ja · Seitenfuß: ja

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| eyebrow | 0,667 | 0,62 | 12 | 0,3 | eyebrow · 12 pt | – |
| headline | 0,667 | 0,95 | 12 | 0,7 | headline · 28 pt | max. 34 Zeichen/Zeile; 1 Zeile(n) |
| sub | 0,667 | 1,65 | 8,95 | 0,45 | sub · 18 pt | – |
| table | 0,667 | 2,35 | 12 | 4,3 | table · 14 pt | – |

- Nur waagrechte Haarlinien (0,75 pt, border.subtle); keine Zebrastreifen.
- Kopf: 11 pt Versalien, text.secondary. Erste Spalte fett weiß, Zahlen rechtsbündig.
- Mehr als 8 Zeilen: aufteilen oder in den Anhang.

#### 9.3.13 Abschluss (`closing`)

Nächster Schritt, Kontakt. Fortschrittsleiste: nein · Seitenfuß: nein

| Platzhalter | x | y | Breite | Höhe | Stil | Inhalt/Grenze |
|---|---|---|---|---|---|---|
| sheet | 3,717 | 1,75 | 5,9 | 4,2 | card | Bottom-Sheet-Motiv |
| grabber | 6,467 | 1,95 | 0,4 | 0,055 | grabber | – |
| prompt | 4,117 | 2,35 | 5,1 | 1,5 | prompt · 28 pt | Ausrichtung center |
| button | 5,067 | 4,05 | 3,2 | 0,6 | button · 18 pt | gelbe Fläche, Radius 0,15 in, Text 18 pt fett schwarz |
| contact | 4,117 | 4,95 | 5,1 | 0,6 | body-small-muted · 16 pt | Ausrichtung center |
| wordmark | 0,667 | 6,95 | 12 | 0,25 | footer · 10 pt | Ausrichtung center |

- Eine Aufforderung, ein Button.
- Kein „Danke für Ihre Aufmerksamkeit“ als einziger Inhalt.

#### 9.3.14 Bild in Karte (`image-card`)

Bild in einer Karte rechts, erklärender Text links. Fortschrittsleiste: ja · Seitenfuß: ja

- Bild mit Alternativtext, Radius 0,28 in, Rand 0,75 pt `border.subtle`.
- Text höchstens 3 Aufzählungspunkte.

#### 9.3.15 Nur Titel (`title-only`)

Eyebrow, Headline und Zweitsatz an den Standardpositionen; darunter freie Fläche im 12er-Raster. Fortschrittsleiste: ja · Seitenfuß: ja

- Eigene Formen nur in ODSV-Farben, -Radien und -Strichstärken.

#### 9.3.16 Leer (`blank`)

Nur Fortschrittsleiste und Seitenfuß. Für Sonderfälle (Vollbild-Grafik, Einbettung).

#### 9.3.17 Platzhalter-Rollen und Helfer

Jedes Layout hat benannte Platzhalter (Rollen wie `eyebrow`, `title`, `sub`, `body`, `chart`). Rolle → Platzhalter-idx, Stil und Zeichengrenze stehen in `catalog/pptx-layouts.json`. `pptx/odsv_pptx.py` befüllt Folien über diese Rollen, setzt Fortschrittsleiste, Quelle und Foliennummer, gestaltet Diagramme und Tabellen nach 8 und 9.2 und prüft die Grenzen (`Deck.check()`). Die Fortschrittsleiste hat fest 7 Segmente.


---

## 10. Illustration und Icons

### 10.1 Line-Art

- **Strich:** weiß bis hellgrau (`lineart.stroke` #F2F2F7), 2–3 px bei 1200 px Bildbreite (Token `border.stroke.illustration` 2,5 px), runde Enden und Ecken. Nebenlinien und Verdecktes: `lineart.dim`, dünner (ca. 60 % der Hauptstärke), gestrichelt 6/5.
- **Flächen:** sehr zurückhaltend. Körperflächen in drei dunklen Stufen (`lineart.face-dark/mid/top`), damit Vorder-, Seiten- und Deckfläche lesbar sind; Vertiefungen `lineart.recess`. Keine Texturen, keine Schatten, keine Verläufe außer dem leichten Seitenverlauf.
- **Akzent:** höchstens ein gelbes Element je Zeichnung – das, worum es geht (Wirkung, Marker, betontes Teil). Rot nur für „falsch“ oder eine echte Anzeige (LED).
- **Perspektive:** isometrisch-schräg und je Produkt einheitlich; technische Ansichten (Draufsicht, Schnitt) flach.
- **Beschriftung:** Labels nach 6.20; Hinweislinien 1 px, rechtwinklig oder in einem festen Winkel, nie gekreuzt.
- **Pfeile:** dünn (1–1,5 px), grau, kleine offene Spitze. Bewegungsrichtung gestrichelt.
- **Helles Theme:** Linien #1D1D1F, Flächen hell (Tokens unter `theme.light.color.lineart`); gelbe Marken bekommen einen 1-px-Ring.

### 10.2 Hand-Gesten

- Stilisierte Hand als **weiße Fläche** ohne Kontur und ohne Details (keine Fingernägel, keine Falten), rechte Hand, leicht schräg.
- Geste = Hand + dünner grauer Pfeil + ein kurzer Satz („Wischen zum Drehen“).
- Einsatz nur für Interaktionshinweise, einmal je Sitzung, 2 s, mittig über der Fläche auf abgedunkeltem Feld (Radius 22 px, Schwarz 60 %). Zeigerereignisse gehen hindurch.
- Mit reduzierter Bewegung steht die Hand still. Der Hinweis steht zusätzlich als Text an der Fläche.

### 10.3 Explosionszeichnung

- Teile fahren entlang **einer Achse** auseinander; Reihenfolge von außen nach innen, jedes Teil in seinem eigenen Zeitfenster. Gestrichelte Führungslinien zeigen den Weg.
- Fortschritt 0 → 1 ist von außen steuerbar (Scroll oder Schritt), das Modul glättet selbst (`motion.easing.in-out`) – nicht doppelt dämpfen.
- Labels erscheinen, sobald ihr Teil am Platz ist. Breit: Labels links und rechts mit Hinweislinien. Schmal: nummerierte gelbe Marken am Teil + Legende darunter.
- Wirkungsbereich (z. B. Abstrahlung, Signal, Reichweite) als 3 Bögen in Gelb mit fallender Deckkraft 1 / 0,7 / 0,4.
- Immer als SVG mit `role="img"`, `title`, `desc` und einer versteckten Teileliste. Ehrlichkeitsvermerk, wenn die Zeichnung schematisch ist.

### 10.4 Icons

- **Raster 24 px**, Strich 2 px, runde Enden und Ecken, keine Füllung, 2 px Schutzrand. In Kacheln 44–52 px mit 2,4 px Strich. Farbe `currentColor`.
- **Größen:** 18 px (in Buttons, Umschalter) · 22 px (Icon-Button, Navigation) · 44/52 px (Kachel).
- **Ausnahme gefüllt:** Status-Icons in Callouts (Warndreieck, Kreis-i) dürfen gefüllt sein, damit sie bei 20 px tragen.
- **Bestand v1.0:** `web/icons.svg` mit 33 Strich-Icons und 9 Signets (10.6) als SVG-Sprite. Fehlende Icons aus einem offenen Strich-Satz mit denselben Maßen ergänzen (z. B. Lucide: 24er-Raster, 2 px, runde Enden). Pflicht-Icons, die jedes Produkt braucht: Haken, Kreuz, Plus, Pfeil rechts/links/oben/unten, Chevron, Warnung, Info, Suche, Schließen, Menü, Vollbild, Drehen, Filter, Kalender, Herunterladen, Externer Link.
- Icons stehen nie allein für eine Handlung ohne Namen (sichtbar oder `aria-label`).

### 10.5 Signet und Bild

- **Signet:** ein abstraktes Zeichen je Produkt aus einfachen geometrischen Formen (Bögen, Kreise, Streifen) im Verlauf `gradient.signet`, Kern in `signet.dot`. Formen sind dick (10–12 % der Signetbreite) mit runden Enden, angeschnitten vom Kartenrand. Wortmarke klein unten links.
- Das Signet ist eine **eigene** Form – nie von fremden Marken abgeleitet.

### 10.6 Signet-Familie

Neben dem Basis-Signet (Signal/Wirkung) gibt es acht Themen-Signets und acht Situations-Signets. Alle entstehen aus derselben Grammatik und sind daher als Familie erkennbar.

| Gruppe | Signet | ID | Motiv | Für Themen wie |
|---|---|---|---|---|
| Basis | Signal | `odsv-signet` | vier Bögen um den Punkt | alles, Standard |
| Technik | KI | `odsv-signet-ai` | Vierstrahl-Funke, Kern als Punkt | KI, Assistenz, Generierung, Automatisierung |
| Technik | Netzwerk | `odsv-signet-network` | vier Verbindungen zu einem Knoten | Vernetzung, Plattform, Integration, IoT |
| Technik | Daten | `odsv-signet-data` | vier steigende Säulen, Punkt darüber | Analyse, Kennzahlen, Reporting, Wachstum |
| Technik | Code | `odsv-signet-code` | vier spitze Klammern, Cursor als Punkt | Entwicklung, Software, Engineering, APIs |
| Lifestyle | Berge | `odsv-signet-mountains` | Grat in vier Abschnitten, Sonne | Alpin, Wandern, Weitblick, Urlaub |
| Lifestyle | Fahrrad | `odsv-signet-bike` | Räder, Rahmen, Lenker; Tretlager als Punkt | Radfahren, Mobilität, Touren, Dienstrad |
| Lifestyle | Outdoor | `odsv-signet-outdoor` | Zelt mit gekreuzten Stangen, Sonne | Draußen, Camping, Abenteuer, Natur |
| Lifestyle | Route | `odsv-signet-route` | Serpentine in vier Abschnitten, Ziel als Punkt | Training, Strecke, Fortschritt, Reise |
| Situation | Erfolg | `odsv-signet-success` | Haken führt zum Punkt, drei Strahlen | Erfolg, Meilenstein, Abschluss |
| Situation | Fail | `odsv-signet-fail` | Kurve steigt und bricht zum Punkt ein | Misserfolg, Rückschlag, Learnings |
| Situation | Konflikt | `odsv-signet-conflict` | zwei Pfeile prallen am Punkt aufeinander | Konflikt, Zielkonflikt, Reibung |
| Situation | Einigung | `odsv-signet-agreement` | zwei Wege treffen sich und gehen weiter | Einigung, Lösung, Zusammenarbeit |
| Situation | Idee | `odsv-signet-idea` | Glühbirne, Glühfaden als Punkt | Idee, Innovation, Vorschlag |
| Situation | Frage | `odsv-signet-question` | Fragezeichen, sein Punkt als Punkt | offene Frage, Unklarheit, Diskussion |
| Situation | In Arbeit | `odsv-signet-progress` | Ring aus vier Bogenstücken | in Arbeit, läuft, Zwischenstand |
| Situation | Neustart | `odsv-signet-restart` | Kreispfeil im Uhrzeigersinn | Neustart, Iteration, Wiederholung |

**Grammatik** (geprüft von `tools/check_signets.js`):
1. viewBox 400 × 400; genau vier Striche mit 26 Einheiten Breite, runden Enden und runden Ecken; keine Füllflächen.
2. Die Farbfolge ist fest: Strich 1 `signet-1` (Pink) → 2 `signet-2` (Orange) → 3 `signet-3` (Hellorange) → 4 `signet-4` (Gelb). Die Folge läuft von außen, hinten oder Anfang nach innen, vorn oder Ziel.
3. Es gibt genau einen gefüllten Punkt in `signet-dot`, Radius 24–34. Er markiert den Fokus: Ziel, Gipfel, Knoten, Cursor oder Sonne.
4. Das Motiv liegt rechts und darf rechts angeschnitten sein. Es bleibt in der Sichtzone y 50–350 (so auch im Querformat 4:3 sichtbar) und links nicht unter x 107 (inklusive Strich).
5. Die Wortmarken-Zone (x < 240, y > 300) bleibt frei.
6. Parallele Striche liegen Mitte zu Mitte mindestens 40 auseinander.
7. Die Bedeutung entsteht über eine einfache, bekannte Form: keine Schrift, keine Marken, keine Personen.

**Einsatz**
- **Basis- und Themen-Signets:** Je Produkt, Website oder Präsentation steht ein Signet, groß höchstens einmal (Hero, Titelfolie). Auf Kapiteltrennern darf dieselbe Variante klein als Marke erscheinen.
- **Situations-Signets** sind Erzähl-Signets für Momente einer Geschichte (Retrospektive, Projektbericht, Lessons Learned). Sie zeigen keinen Status an; dafür gibt es Callout und Badge in Statusfarben. Mehrfach je Dokument erlaubt, aber höchstens eines je Ansicht oder Folie und nie zusammen mit einem Themen-Signet. In Folien: `Deck.mark(slide, 'success')` oder `signet='fail'` auf dem Kapiteltrenner.
- Varianten werden nicht gemischt, nicht umgefärbt und nicht neu angeordnet.
- Auswahl nach dem Kernthema des Ganzen, nicht einzelner Abschnitte. Im Zweifel nimm das Basis-Signet.
- Formate:
  - Karte quadratisch (`.odsv-signet-card`) oder 4:3 (`--landscape`)
  - Marke ohne Karte ab 48 px (`.odsv-signet-mark`); darunter nur das Basis-Signet
  - immer auf dunklem Grund, auch im hellen Theme in der dunklen Karte
- Barrierefreiheit: `role="img"` und ein `aria-label`, das das Motiv beschreibt.
- Dateien:
  - Sprite-Symbole in `web/icons.svg`
  - eigenständige SVGs mit festen Farben in `web/signets/`
  - Folienbilder in `pptx/signets/` (Karte und Marke); in Präsentationen über `Deck.slide('Titel', signet='ai')`
- Neue Varianten nur über `tools/build_signets.py` anlegen. Danach `tools/check_signets.js` und `tools/render_signets.js` ausführen und die Variante in die Tabelle oben eintragen.
- **Fotos und Renderings** stehen auf Schwarz oder in einer Karte. Helle Bilder auf dunkler Seite nur in einer hellen Karte (`#F5F5F7`, 10 px Innenabstand) – nie hart auf Schwarz.

---

## 11. Bewegung

Ruhig, genau, nichts Verspieltes.

| Zweck | Dauer | Easing | Token |
|---|---|---|---|
| Hover, Tastendruck | 100 ms | standard | `motion.duration.instant` |
| Button, Checkbox, Umschalter | 200 ms | standard | `fast` |
| Einblenden, Kartenwechsel, Sheet | 300 ms | standard | `base` |
| Linien zeichnen, große Flächen | 400 ms | in-out | `slow` |
| Bühne ein-/ausblenden | 500 ms | standard | `stage` |
| Kamerafahrt, Explosionsweg | 900–1000 ms | in-out | `camera` |
| Versatz zwischen Geschwistern | 50–80 ms | – | `stagger` |
| scrollgekoppelter Fortschritt | – | linear | – |

`standard` = cubic-bezier(0.2, 0.8, 0.2, 1) · `in-out` = cubic-bezier(0.65, 0, 0.35, 1) · `exit` = cubic-bezier(0.4, 0, 1, 1).

**Regeln**

1. **Eine Bewegung zur Zeit.** Erst das eine, dann das andere.
2. **Einblenden:** 12–16 px von unten + Deckkraft, einmalig. Nichts blendet beim Zurückscrollen wieder aus.
3. **Nur `transform` und `opacity`** animieren; Farben bei Zustandswechseln.
4. **Gedrückt:** Skalierung 0,98.

**Scroll-Storytelling**

- Der Scroll steuert, das Modul glättet. Werte je Bild aus dem Fortschritt der Strecke berechnen.
- Sticky-Strecke: Bühne klebt unter der Top-Bar, Texte wechseln als Karten; Länge 300–400 % der Fensterhöhe, höchstens 4–5 Stationen.
- Ein Scroll-Handler je Seite: passiv, Arbeit in `requestAnimationFrame`, Maße per `ResizeObserver` zwischenspeichern.
- **Kein Scroll-Hijacking**, kein `scroll-snap` auf der Hauptachse, keine Fokusfalle. Texte stehen in normaler DOM-Reihenfolge.
- 3D-/Canvas-Flächen fangen das Mausrad nicht ab; Drehen und Zoomen nur in einem ausdrücklich gestarteten Modus, der mit Escape endet.

**Reduzierte Bewegung** (`prefers-reduced-motion: reduce`)

- `tokens.css` setzt alle Dauern auf 0,01 ms und alle Wege auf 0 – wer nur Tokens nutzt, ist damit bereits ruhig.
- Zusätzlich im Produkt: Sticky-Strecken entfallen, Inhalte stehen als normale Abschnitte mit Standbildern · Kamerawechsel springen · Explosionszeichnung steht voll geöffnet · Signet zeichnet sich nicht · Hand steht still · Ladekreis 3 s, Skelett ohne Puls · nichts blinkt.
- Auf Umschalten während der Sitzung reagieren.
- Dashboards: Diagramme bauen sich nicht auf; neue Werte erscheinen ohne Zähl-Animation.

---

## 12. Barrierefreiheit

Ziel: **WCAG 2.2 AA** in beiden Themes; für Web-Produkte in Deutschland damit auch die Anforderungen aus BFSG/EN 301 549, soweit sie Gestaltung betreffen.

| Thema | Regel |
|---|---|
| Textkontrast | ≥ 4,5:1 für alle Textstufen bis `text.faint` auf Grund, Karte 1 und Karte 2 (3.3). `text.faint` nicht auf Karte 3 (4,27:1). |
| Nicht-Text-Kontrast | Bedienelemente, Fokus, Icons, Diagrammfarben ≥ 3:1. Kartenränder sind Dekor (3.3). |
| Farbe | nie alleiniger Träger: Status = Icon + Wort; Diagramm = Beschriftung/Muster; aktiv = Strich/Name + Helligkeit. |
| Fokus | immer sichtbar: 2 px, 3 px Abstand; Gelb (dunkel), Schwarz (hell), Weiß um gelbe Flächen. Fokus wird nie von klebenden Leisten verdeckt. |
| Tastatur | alles bedienbar, Reihenfolge = Lesereihenfolge, keine Falle; Escape schließt Überlagerungen und Sondermodi. |
| Zielgröße | 44 × 44 px bei Touch; mindestens 24 × 24 px in dichten Dashboards. |
| Struktur | ein `h1`, Landmarken, Sprunglink, `lang="de"`. Eyebrows sind keine Überschriften. |
| Versalien | per Stil, nie getippt; nie für Fließtext, Warnungen, Fehlermeldungen. |
| Zoom und Umbruch | 200 % Zoom und 320 px Breite ohne waagrechtes Scrollen; Textabstände dürfen vom Nutzer vergrößert werden. |
| Bewegung | `prefers-reduced-motion` wird geachtet; nichts blinkt öfter als dreimal je Sekunde; Bewegtes über 5 s ist anhaltbar. |
| Medien | 3D, Canvas, Diagramme sind Zusatz: jede Information steht auch als Text oder Tabelle. |
| Formulare | sichtbare Labels, Fehler als Text am Feld und in der Übersicht, keine Zeitgrenzen ohne Verlängerung. |
| Meldungen | `role="status"` für Bestätigungen und Zähler, `role="alert"` für Fehler. |
| Erzwungene Farben | Windows-Kontrastmodus: Ränder und Fokus bleiben sichtbar (Rahmen statt nur Flächenfarbe; `forced-color-adjust` nicht abschalten). |
| Präsentation | eindeutige Folientitel, Lesereihenfolge, Alternativtexte, mindestens 16 pt (9.1). |

Prüfen vor jeder Veröffentlichung: `python3 tools/check_tokens.py` · Tastaturdurchlauf · Screenreader-Stichprobe (VoiceOver, NVDA) · 200 % Zoom · reduzierte Bewegung · Druckvorschau.

---

## 13. Dateistruktur

```
odsv/
├── AGENTS.md                Einstieg für AI-Agents (Entscheidungsbaum, Muss-Regeln, Ablauf, Definition of Done)
├── llms.txt                 Kurzindex nach llms.txt-Konvention
├── README.md                Überblick
├── SPEC.md                  diese Spezifikation
├── GAPS.md                  Lückenanalyse, Prüfberichte
├── tokens/
│   ├── tokens.json          Quelle der Wahrheit (W3C-DTCG, jedes Token mit $description), dunkel + theme.light + theme.print
│   ├── tokens.css           erzeugt: CSS Custom Properties, Präfix --odsv-
│   └── pptx.json            PowerPoint: Format, Raster, Thema, Schriften, Textstile, 16 Layouts
├── catalog/                 erzeugt von tools/build_catalog.py – nie von Hand ändern
│   ├── src/components.meta.py   Quelle: Zweck, Abgrenzung, Varianten, Regeln, A11y, Inhaltsgrenzen je Komponente
│   ├── components.json / COMPONENTS.md   Komponenten mit Klassen-API und Referenz-Markup
│   ├── classes.json · icons.json · tokens.flat.json · pptx-layouts.json
│   └── js-api.md            odsv.js und odsv-charts.js
├── web/                     odsv.css, odsv.js, odsv-charts.js, icons.svg (33 Icons + Signet), tokens.css (Kopie),
│                            index.html (Referenz), examples/ (Website, Dashboard)
├── templates/               Startvorlagen: website.html, dashboard.html, deck_example.py
├── pptx/                    ODSV-Vorlage.potx (16 Layouts), ODSV-Vorlage.pptx (18 Beispielfolien), odsv_pptx.py (Helfer),
│                            _build/ (Erzeuger), _preview/
└── tools/                   build_tokens.py, check_tokens.py, build-web.js, check-css.js, build_catalog.py,
                             lint-html.js (Regelprüfung), audit.js (Playwright), qa.js, validate.sh (alles)
```

- **Geändert wird nur `tokens.json`.** Danach `bash tools/validate.sh` (erzeugt CSS, Sprite, Katalog und prüft alles). `tokens.css` nie von Hand ändern. `pptx.json` wird von Hand gepflegt und vom Prüfskript gegen `tokens.json` abgeglichen (Farben, Raster, Laufweiten).
- **Themes:** `:root` = dunkel · `[data-theme="light"]` an beliebigem Element = hell (auch für Teilbereiche; Alias-Variablen werden dort neu aufgelöst) · `@media print` = hell + Druck.
- **Namensregel:** `--odsv-<gruppe>-<rolle>-<stufe>`. Textstile haben Teil-Variablen `-family`, `-size`, `-weight`, `-tracking`, `-leading`, `-transform`.
- **`web/` und `pptx/`** sind parallel zu dieser Spezifikation entstanden. Abgeglichen ist: `web/tokens.css` ist identisch mit `tokens/tokens.css`, alle 395 in `web/` verwendeten Variablen sind definiert, das Farbthema und die Schriften der Vorlage stimmen mit `pptx.json` überein. **Nicht** abgeglichen ist, ob Komponenten und Folienlayouts dieser Spezifikation Punkt für Punkt folgen (siehe GAPS.md 3.1). `web/tokens.css` ist eine Kopie – nach jedem Build neu kopieren.
- Für den Aufruf per Skill gibt es den Skill `odsv`; er fasst die Kernregeln zusammen und verweist auf `AGENTS.md`.

---

## 14. Versionierung

Semantische Versionierung `MAJOR.MINOR.PATCH`, Stand in `tokens.json → $extensions.odsv.version` und `pptx.json → version`.

| Stufe | Wann | Beispiel |
|---|---|---|
| MAJOR | Token entfernt oder umbenannt; Rolle ändert Bedeutung; Folienraster ändert Maße | `color.text.faint` entfällt |
| MINOR | neues Token, neue Komponente, neues Layout, neues Theme | Icon-Satz, `components.css` |
| PATCH | Wert korrigiert ohne Rollenwechsel, Text in der Spezifikation | Kontrastkorrektur einer Farbe |

- Entfernte Tokens bleiben eine MINOR-Version lang als Alias mit `$deprecated` erhalten.
- Jede Änderung besteht `check_tokens.py`, bevor sie veröffentlicht wird.
- Produkte nennen die verwendete Version (Kommentar in der CSS-Datei, Notizfeld im Folienmaster).

**v1.0.0 (17.11.2026)** – Erste Fassung. Umfang: dunkles Theme als Standard, helles Theme und Druck, Status Info, deckende Textstufen, Rand für Bedienelemente, Datenvis-Paletten, Formulare, Tabs, Tooltip, Badge, Leer- und Ladezustand, Dashboard-Dichten, Folienraster mit 16 Layouts, Komponentenbibliothek fürs Web.

---

## 15. Agenten-Schnittstelle

ODSV ist so aufgebaut, dass Agents ohne Rückfragen korrekt bauen und sich selbst prüfen können.

| Bedarf | Antwort |
|---|---|
| Einstieg, Reihenfolge | `AGENTS.md` |
| gültige Klassen, Markup, Regeln | `catalog/components.json` (Felder `use`, `avoid`, `variants`, `states`, `rules`, `a11y`, `js`, `content_limits`, `examples`) |
| Werte mit Bedeutung | `catalog/tokens.flat.json` |
| Folien befüllen | `catalog/pptx-layouts.json` + `pptx/odsv_pptx.py` |
| Startpunkt | `templates/` |
| Selbstprüfung Web | `node tools/lint-html.js seite.html` (Regel-IDs entsprechen AGENTS.md Abschnitt 3; Exit-Code 1 bei Fehlern) |
| Selbstprüfung Folien | `Deck.check()` + `Deck.render_png()` |
| Gesamtprüfung | `bash tools/validate.sh [--full]` |

**Gleichlauf:** Der Katalog entsteht aus CSS, Referenzseite und `components.meta.py`. Eine neue CSS-Wurzel ohne Katalogeintrag lässt `validate.sh` scheitern. So können Beschreibung und Code nicht auseinanderlaufen.

