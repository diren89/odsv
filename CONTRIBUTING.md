# Beitragen

Regeln für Änderungen an ODSV, für Menschen und Agents. Was Quelle ist und was erzeugt wird, steht in [`CLAUDE.md`](CLAUDE.md); wie das System geändert wird, in [`AGENTS.md`](AGENTS.md) Abschnitt 9.

## Ablauf

1. **Zweig anlegen**, nie direkt auf `main` arbeiten: `feat/<thema>` (neue Komponente, Token, Signet, Diagrammform), `fix/<thema>` (Korrektur), `docs/<thema>` (nur Text). Agents arbeiten in einem eigenen Git-Worktree; Worktree-Ordner liegen unter `.worktrees/` (in `.gitignore`).
2. **Nur Quellen ändern**, erzeugte Dateien nur über die Werkzeuge. Danach `bash tools/validate.sh` bis „✔ ODSV-Prüfung bestanden“. Folien-PNGs bestehender Signets, die sich nur bytegenau unterscheiden, mit `git checkout -- pptx/signets/<datei>` zurücksetzen.
3. **Version anheben** nach SPEC 14 (MAJOR/MINOR/PATCH), Dateien laut `CLAUDE.md` → „Version“:
   - Eintrag in `SPEC.md` Kapitel 14 (ausführlich) und
   - neue Zeile oben in der Tabelle **Releasenotes** der [`README.md`](README.md) (Version, Datum, ein Satz). Beide müssen zusammenpassen.
   - Reine Repo-Doku (`CONTRIBUTING.md`, `CLAUDE.md`, Werkzeug-Kommentare) ändert das Design-System nicht und braucht keine neue Version.
4. **Sichtprüfung:** Neue oder geänderte Grafiken (Signets, Folien, Website) gerendert ansehen, nicht nur die Prüfskripte laufen lassen.
5. **Pull Request** gegen `main` mit kurzer Begründung, Prüfausgaben und dem, was ungeprüft blieb. Ein Mensch prüft und merged. Modelle mergen nicht selbst in `main`, außer ein Mensch beauftragt sie ausdrücklich damit.
6. **Nach dem Merge** setzt, wer merged, den Tag `v<Version>` auf den Merge-Commit (oder beauftragt ausdrücklich ein Modell damit). Der Merge auf `main` baut die Website über `.github/workflows/pages.yml` neu.
7. Arbeitszweig und Worktree nach dem Merge entfernen.

## Was nicht hineingehört

- Fremde Marken, Logos, Produkt- oder Firmennamen (außer in `web/examples/`), Fotos realer Personen, Webfonts von CDNs (AGENTS.md 4).
- Persönliche Daten: Namen, E-Mail-Adressen, Pfade aus Benutzerverzeichnissen, Gerätekennungen.
- Geheimnisse jeder Art (Tokens, Schlüssel, Zugangsdaten).
- Erfundene Zahlen; Beispieldaten immer als „Quelle: Beispieldaten“ kennzeichnen.
