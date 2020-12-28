# Anfängerpraktikum

[![Continuous Integration](https://github.com/NicoWeio/AP/workflows/Continuous%20Integration/badge.svg)](https://github.com/NicoWeio/AP/actions)
[![PDFs](https://img.shields.io/badge/PDFs-auf%20GitHub%20Pages-blue)](https://nicoweio.github.io/AP/)

In diesem Repository sammeln wir, Katharina Popp und Nicolai Weitkemper, den Quellcode für unsere Protokolle.
So weit, so unspektakulär…

Aber es gibt drei Dinge, die dieses Repository besonders attraktiv machen sollen:

## Ein Linter!

Um uns die Arbeit des Korrekturlesens zu vereinfachen,
habe ich (Nicolai) einen Linter programmiert,
der häufige Fehler, vor allem Formfehler,
erkennt.
Weiteres zum Linter findet sich in dessen [Unterordner](./Linter).

Da ihr, werte Leser, wahrscheinlich ähnliche Anforderungen wie wir erfüllen müsst
und ebenfalls die [Latex-Vorlage aus dem Toolbox-Workshop](https://github.com/pep-dortmund/toolbox-workshop/tree/master/latex-template) nutzt,
stehen die Chancen gut, dass auch ihr von diesem Linter profitieren könnt.

## Continuous Integration

Ein weiteres Goodie ist die automatische Generierung von PDFs,
die stets den aktuellen Stand des Repositorys wiederspiegeln.
Sie finden sich auf [GitHub Pages](https://nicoweio.github.io/AP/).

Der Docker-Container, in dem die eigentliche Erstellung läuft, ist in ein eigenes [Repository](https://github.com/NicoWeio/my-texlive) ausgelagert.

## All-inclusive

Soll heißen:
Dieses Repository enthält alles,
was man zum Erstellen der Protokolle braucht.
(Die funktionierende Continuous Integration ist der beste Beweis dafür.)

-   Messwerte
-   Python-Code zur Auswertung
-   .tex-Dateien
-   Grafiken
