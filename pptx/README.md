# ODSV-Vorlage für PowerPoint

Dunkle 16:9-Vorlage (13,333 × 7,5 in) für das Design-System ODSV v1.0.0. Maße, Farben und Textstile stammen aus `tokens/pptx.json` und `SPEC.md` Abschnitt 9.

## Dateien

| Datei | Inhalt |
|---|---|
| `ODSV-Vorlage.pptx` | Vorlage mit 18 Beispielfolien (je Layout mindestens eine) |
| `ODSV-Vorlage.potx` | Dieselbe Vorlage ohne Folien, Content-Type `template.main+xml` |
| `_preview/` | `slide-01.png` bis `slide-18.png`, `overview.png`, `ODSV-Vorlage.pdf` (LibreOffice-Rendering) |
| `odsv_pptx.py` | Helfer zum Befüllen (siehe unten) |
| `_build/` | Erzeuger: `bash _build/build_all.sh` baut alles neu (`tpl.py` Theme/Master/Layouts, `deck.py` Beispielfolien, `assets.py` Signet und Platzhalterfoto) |

## Automatisch befüllen (für Skripte und AI-Agents)

`odsv_pptx.py` befüllt die Vorlage über Platzhalter-Rollen. Es setzt Fortschrittsleiste, Quelle und Foliennummer, gestaltet Diagramme und Tabellen im ODSV-Stil und prüft Zeichengrenzen (`Deck.check()`). Rollen je Layout: `../catalog/pptx-layouts.json`. Beispiel: `../templates/deck_example.py`.

```python
from odsv_pptx import Deck
d = Deck(); d.slide('Titel', eyebrow='Bericht', title='Kennzahlen', sub='Ein Satz.')
print(d.check()); d.save('out.pptx'); d.render_png('vorschau')
```

## Theme

- Name „ODSV Dark“. Farben: dk1 000000, lt1 FFFFFF, dk2 1C1C1E (Karte), lt2 A1A1A6 (Zweitsatz), accent1–6 FFE94D, 4797FF, EC3A78, 2FCFC2, F5893A, B9A1FF, hlink FFE94D, folHlink CCCCCC.
- Farbzuordnung umgekehrt: bg1=dk1, tx1=lt1, bg2=dk2, tx2=lt2. „Hintergrund 1“ ist Schwarz, „Text 1“ Weiß, „Hintergrund 2“ die Karte.
- Schriften: Überschriften und Text Arial.
- Die Zwischengrautöne (Fließtext E6E6E6, Eyebrow CCCCCC, Fußzeile 8E8E93, Rand 2C2C2E) sind feste RGB-Werte, weil das Farbschema nur 12 Slots hat.

## Layouts und Platzhalter

Alle Platzhalter erben Schrift, Größe, Laufweite, Versalien und Farbe vom Layout. Nichts davon auf der Folie überschreiben.

| Layout | Platzhalter | Hinweis |
|---|---|---|
| Titel | Eyebrow, Titel, Untertitel, Meta | Signet-Karte rechts. Titel höchstens 2 Zeilen à 12 Zeichen |
| Kapiteltrenner | Kapitelnummer, Eyebrow, Kapiteltitel, Zweitsatz | Signet-Marke unten rechts. Titel höchstens 17 Zeichen je Zeile |
| Agenda | Eyebrow, Headline, Zweitsatz, Agenda-Liste, Hinweis-Karte | Liste nummeriert automatisch, höchstens 6 Punkte |
| Inhalt einspaltig | Eyebrow, Headline, Zweitsatz, Text, Hinweis-Karte | Höchstens 5 Punkte oder 80 Wörter |
| Zwei Spalten | Eyebrow, Headline, Zweitsatz, je Spalte Label, Karten-Headline, Text | Beide Karten gleich hoch |
| KPI drei Zahlen | Eyebrow, Zahl-Label (Folientitel), Zahl, Aussage, je Kachel Label und Wert | Keine Headline, die Zahl trägt die Folie. Höchstens 9 Zeichen bei 120 pt |
| Diagramm | Eyebrow, Headline, Zweitsatz, Diagramm, Aussage-Label, Aussage, Erläuterung | Headline nennt die Aussage |
| Bild vollflächig | Bild, Eyebrow, Headline, Zweitsatz | Verlauf siehe unten |
| Bild in Karte | Eyebrow, Headline, Text, Bild | Bild mit 0,28 in Radius |
| Zitat | Zitat, Name, Rolle | Normale Schreibweise, höchstens 30 Wörter |
| Prozess vier Schritte | Eyebrow, Headline, Zweitsatz, je Karte Nummer, Titel, Text | Line-Art je Karte auf der Folie |
| Vergleich | Eyebrow, Headline, Zweitsatz, je Option Kopf, Titel, Zeilen | Icon und Empfehlungs-Rand auf der Folie |
| Tabelle | Eyebrow, Headline, Zweitsatz, Tabelle | Höchstens 8 Zeilen, 6 Spalten |
| Abschluss | Aufforderung (Folientitel), Button, Kontakt | Kein Seitenfuß, keine Fortschrittsleiste |
| Nur Titel | Eyebrow, Headline, Zweitsatz | Freie Gestaltung |
| Leer | keine | Nur Fortschrittsleiste und Seitenfuß |

Seitenfuß: kleine gesperrte Wortmarke „ODSV“ links (Master), Quelle (Fußzeilen-Platzhalter, 10 pt Versalien) und Foliennummer rechts. Abschluss und Titel haben keinen Fuß, Bild vollflächig nur die Foliennummer. Fußzeile und Foliennummer über „Einfügen > Kopf- und Fußzeile“ aktivieren.

## Regeln

- **Versalien-Titel:** Text normal tippen (inkl. „ß“ vermeiden). Versalien und Laufweite setzt das Layout per Zeichenformat (`cap="all"`, `spc`): Headline 28 pt / spc 420, Titel 44 pt / 880, Kapitel 54 pt / 1080, Eyebrow 12 pt / 240, Label 11 pt / 165. Eine Zeile, höchstens 34 Zeichen. Zentrierte Versalien-Zeilen vermeiden (Überhang der Sperrung).
- **Textmengen:** Fließtext mindestens 16 pt, Beschriftungen mindestens 12 pt, Fuß 10 pt. Höchstens 5 Listenpunkte oder 80 Wörter je Folie. Zitat höchstens 30 Wörter. Eine Aussage je Folie.
- **Fortschrittsleiste:** Die Layouts liefern die graue Spur (7 Segmente, #616161). Aktive und erledigte Kapitel legt man als weiße Segmente darüber (Beispiel: Folie 2, Form „Fortschritt aktiv“, einfach kopieren). Prozess-Folie: eigene Segmentleiste über den Karten.
- **Diagrammfarben, immer in dieser Reihenfolge:** 1 FFE94D, 2 4797FF, 3 EC3A78, 4 2FCFC2, 5 F5893A, 6 B9A1FF, 7 8FD46A. Nie umsortieren. Eine Reihe: Gelb. Vergleichsreihe: Grau 8E8E93. Fokus-Muster: betonte Reihe Gelb, alle anderen 636366. Gitter nur waagrecht 0,75 pt in 2C2C2E, Achsentext 12 pt in 8E8E93, Datenbeschriftung 12 pt in CCCCCC (auf gestapelten, hellen Flächen Schwarz), Säulen Abstand 60 %, Linien 2,25 pt mit Marker nur am letzten Punkt, Legende oben links, höchstens 4 Reihen direkt beschriftet.
- **Signet-Verlauf** (Pink, Orange, Gelb) nur auf Titelfolie und Kapiteltrenner, nie auf Flächen oder Text.
- **Bild vollflächig:** Layout-Shapes liegen immer hinter dem Bild, deshalb sitzt der Lesbarkeits-Verlauf („Verlauf unten“, Schwarz 0 auf 85 %, untere 45 %) als Shape auf der Folie direkt über dem Bild. Für neue Bildfolien von Folie 10 kopieren. Alternative ohne Verlauf: Layout „Bild in Karte“.
- **Barrierefreiheit:** Jede Folie hat einen Titel im Titelplatzhalter (KPI: das Label, Abschluss: die Aufforderung; Layout „Zitat“ hat keinen, dort Titel in der Gliederung ergänzen). Alternativtexte für Bilder und Diagramme setzen. Lesereihenfolge prüfen.

## Schrift-Fallbacks

Das Theme kennt je Rolle genau eine Schrift. Es steht Arial darin, weil Arial auf Windows und macOS vorhanden ist. Helvetica Neue ist nur für Decks zulässig, die nur auf dem Mac laufen oder als PDF gehen (Entwurf → Schriftart ersetzen, gesperrte Versalien brechen dann anders um). SF Pro und Inter dürfen nicht eingebettet oder weitergegeben werden. Mono (Code): Consolas, Ersatz Courier New.

## Bekannte Grenzen

- Die Vorschau stammt aus LibreOffice (Arial wird durch Liberation Sans ersetzt, gleiche Laufweiten). PowerPoint setzt Zeilenhöhen und Absatzabstände minimal anders. Besonders Agenda-Haarlinien und die 120-pt-KPI-Zahl in PowerPoint prüfen.
- Das Signet (Karte und Marke) und das Platzhalterfoto sind PNG-Bilder, keine Vektoren. Das Zitat-Zeichen ist ein Textzeichen in Akzentgelb statt Line-Art.
- Das Foto in den Beispielfolien ist ein erzeugtes Platzhalterbild. Die Diagrammwerte sind als „Beispieldaten“ gekennzeichnet und erfunden.
- Das Layout „Zitat“ hat keinen Titelplatzhalter. Es gibt nur das dunkle Theme (kein Light-Theme-Master).
- Tabellenformat ist als Tabellenstil „ODSV Tabelle“ hinterlegt. Schriftgrößen (Kopf 11 pt Versalien, Zellen 14 pt) und Haarlinien sind zusätzlich direkt in den Zellen gesetzt, weil Tabellenstile keine Größen kennen.
- Übergänge und Animationen sind nicht gesetzt (Spezifikation: Überblenden 0,3 s oder keiner).
