#!/usr/bin/env python3
"""Startvorlage: Präsentation im ODSV-Stil mit pptx/odsv_pptx.py.
Aufruf: python3 templates/deck_example.py [ausgabe.pptx] [vorschau-ordner]
Rollen je Layout: catalog/pptx-layouts.json. Nach dem Bauen: check() lesen, PNGs ansehen."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'pptx'))
from odsv_pptx import Deck

out = sys.argv[1] if len(sys.argv) > 1 else 'beispiel.pptx'
d = Deck()
SRC = 'Quelle: Beispieldaten'

d.slide('Titel', section='Einstieg', eyebrow='Quartalsbericht · Q3 2026', title='Kennzahlen',
        sub='Was im dritten Quartal zählt.', meta='Stand 17.11.2026')
d.slide('Agenda', chapter=0, section='Überblick', eyebrow='Überblick', title='Agenda', sub='Vier Punkte, ein roter Faden.',
        body=['Ergebnis', 'Treiber', 'Risiken', 'Nächste Schritte'],
        aside=[[('Dauer', {'size': 11, 'caps': True, 'spc': 165, 'color': 'CCCCCC'})], [('30 Minuten', {'size': 20, 'bold': True})]])
d.slide('Kapiteltrenner', chapter=1, source=SRC, number='1', eyebrow='Kapitel 1 von 4', title='Ergebnis', sub='Das Quartal in einer Zahl.')
d.slide('KPI drei Zahlen', chapter=1, source=SRC, eyebrow='Kennzahl', label='Umsatz', value=[[('2,1', {}), (' Mio. €', {'color': 'FFFFFF'})]],
        sentence='im dritten Quartal, 12 % über Plan.', tl0='Kunden', tv0='1.284', tl1='Marge', tv1='18 %', tl2='Zeitraum', tv2='Q3 2026')
s = d.slide('Diagramm', chapter=2, source=SRC, eyebrow='Treiber', title='Q4 liegt vorn', sub='Umsatz je Quartal, in Mio. €.',
            ilabel='Kernaussage', itext='Das vierte Quartal wächst am stärksten.', inote='Fokus-Muster: eine Säule gelb, Rest grau.')
d.chart(s, 'bar', ['Q1', 'Q2', 'Q3', 'Q4'], {'Umsatz': [1.2, 1.4, 1.5, 2.1]}, highlight=3, alt='Säulendiagramm: Q4 mit 2,1 Mio. € am höchsten')
s = d.slide('Tabelle', chapter=2, source=SRC, eyebrow='Treiber', title='Regionen', sub='Umsatz und Anteil je Region.')
d.table(s, [('Region', 'Umsatz', 'Anteil'), ('Süd', '0,9 Mio. €', '43 %'), ('West', '0,7 Mio. €', '33 %'), ('Nord', '0,5 Mio. €', '24 %')], numeric_cols=(1, 2))
d.slide('Prozess vier Schritte', chapter=3, eyebrow='Nächste Schritte', title='In vier Schritten', sub='Vom Befund zur Maßnahme.',
        icons=['list', 'layout', 'chart', 'check'], n0='1', t0='Analysieren', x0='Ursachen je Region klären.', n1='2', t1='Planen', x1='Maßnahmen mit Termin festlegen.',
        n2='3', t2='Umsetzen', x2='Verantwortliche benennen.', n3='4', t3='Prüfen', x3='Wirkung im Q4 messen.')
d.slide('Vergleich', chapter=3, eyebrow='Risiken', title='Richtig / Falsch', sub='Wie wir Ziele formulieren.',
        head0='Richtig', title0='Messbar', text0=['Zahl, Einheit, Datum', 'Ein Verantwortlicher'],
        head1='Falsch', title1='Vage', text1=['„Deutlich mehr“', 'Kein Termin'])
d.slide('Abschluss', section='Abschluss', prompt='Fragen? Jetzt ist der Moment.', button='Zur Diskussion', contact='Kontakt: Team Controlling')

issues = d.check()
print('Befunde:', *issues, sep='\n  ') if issues else print('Befunde: keine')
d.save(out); print('gespeichert:', out)
if len(sys.argv) > 2:
    for p in d.render_png(sys.argv[2]): print(p)
