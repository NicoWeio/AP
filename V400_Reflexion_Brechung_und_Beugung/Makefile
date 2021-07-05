all: build/main.pdf

plots: \
		build/plt/beugung.pdf \
		build/plt/reflexionsgesetz.pdf \
		build/plt/strahlversatz.pdf \

tables: \
		build/tab/mess_brechungsgesetz.tex \
		build/tab/mess_reflexionsgesetz.tex \
		build/tab/prisma.tex \
		build/tab/strahlversatz.tex \

build/plt/strahlversatz.pdf build/tab/strahlversatz.tex: 3_strahlversatz.py | build/plt build/tab
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 3_strahlversatz.py

build/plt/beugung.pdf: 5_gitter.py | build/plt
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 5_gitter.py

build/plt/reflexionsgesetz.pdf: 1_reflexionsgesetz.py | build/plt
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 1_reflexionsgesetz.py

build/tab/prisma.tex: 4_prisma.py | build/tab
		python3 4_prisma.py

build/tab/mess_%.tex &: 0_messwerte.py | build/tab
		python3 0_messwerte.py

build/main.pdf: main.tex lit.bib plots tables | build
	  TEXINPUTS=build: \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex

build build/plt build/tab &:
	mkdir -p build
	mkdir -p build/plt
	mkdir -p build/tab

clean:
	rm -rf build

.PHONY: all clean plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
