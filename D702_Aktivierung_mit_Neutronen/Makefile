all: build/main.pdf

plots: \
		build/plot1_lin.pdf \
		build/plot1_log.pdf \
		build/plot2_lin.pdf \
		build/plot2_log.pdf \

build/plot1_%.pdf: 2_vanadium.py | build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 2_vanadium.py

build/plot2_%.pdf: 3_rhodium.py | build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 3_rhodium.py

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

.PHONY: all clean plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
