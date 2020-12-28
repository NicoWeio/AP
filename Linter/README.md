## Benutzung

Der Linter nutzt das Arbeitsverzeichnis als Ausgangspunkt für die rekursive Suche nach passenden Dateien.
In der Regel sollte man daher in den Unterordner mit dem Protokoll von Interesse navigieren.
Dann kann der Linter mit `../Linter/linter.py` aufgerufen werden.
(Da es sich um einen relativen Pfad handelt, muss dieser gegebenenfalls angepasst werden.)

Verfügbare Optionen können durch Anhängen von `--help` an das Kommando eingesehen werden.

## Regeln

Im Moment werden alle Regeln als _reguläre Ausdrücke_ dargestellt.
Eine Auflistung ist in [rules.py](./rules.py) zu finden.
