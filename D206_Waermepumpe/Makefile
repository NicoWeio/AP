all: build/main.pdf

build/wärmepumpe_plot.pdf: main.py | build
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 main.py

plots: \
	build/wärmepumpe_plot.pdf \

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
