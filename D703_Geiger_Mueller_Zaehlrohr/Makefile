all: build/main.pdf

plots: \
		build/plot1.pdf \
		build/plot2.pdf \

build/plot1.pdf: 1_kennlinie.py | build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 1_kennlinie.py

build/plot2.pdf: 3_zaehlrohrstrom.py | build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 3_zaehlrohrstrom.py

tables: \
		build/table_messwerte.tex \
		build/table_zaehlrohrstrom.tex \

build/table_messwerte.tex: | build
	python3 0_messwerte.py

build/table_zaehlrohrstrom.tex: | build
	python3 3_zaehlrohrstrom.py


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

build:
	mkdir -p build

clean:
	rm -rf build

.PHONY: all clean plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
