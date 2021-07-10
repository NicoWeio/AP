all: build/main.pdf

plots: \
		build/plt/emissionsspektrum.pdf \
		build/plt/transmission.pdf \

tables: \
		build/tab/mess_emissionsspektrum_4col.tex \
		build/tab/mess_transmission.tex \

build/plt/emissionsspektrum.pdf: 1_emissionsspektrum.py | build/plt
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 1_emissionsspektrum.py

build/plt/transmission.pdf: 2_transmission.py | build/plt
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 2_transmission.py

build/tab/mess_transmission.tex: 0_messwerte.py | build/plt
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 0_messwerte.py

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

.PHONY: all clean contents plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
