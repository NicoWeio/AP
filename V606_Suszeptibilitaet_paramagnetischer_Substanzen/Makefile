all: build/main.pdf

plots: \
		build/plot_filterkurve.pdf \

tables: \
		build/table_Dy2O3_auswertung.tex \
		build/table_Nd2O3_auswertung.tex \

build/plot_filterkurve.pdf: 1_filterkurve.py | build
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 1_filterkurve.py

build/table_%_auswertung.tex: 3_suszeptibilitaet_auswertung.py | build
		python3 3_suszeptibilitaet_auswertung.py

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
