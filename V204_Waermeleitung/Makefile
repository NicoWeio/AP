all: build/main.pdf

plots: \
	build/plot_dynamisch_aluminium.pdf \
	build/plot_dynamisch_edelstahl.pdf \
	build/plot_dynamisch_messing_breit.pdf \
	build/plot_dynamisch_messing_schmal.pdf \
	build/plot_statisch_alle.pdf \
	build/plot_statisch_tdiff.pdf \

build/plot_%.pdf: build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 statisch.py
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 dynamisch.py

build/main.pdf: main.tex lit.bib plots | build
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

.PHONY: all clean plots

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
