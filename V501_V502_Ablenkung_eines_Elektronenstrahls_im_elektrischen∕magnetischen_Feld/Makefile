all: build/main.pdf

contents: \
	lit.bib \
	main.tex \
	$(wildcard content/*) \

plots: \
		build/plt/V501_1.pdf \
		build/plt/V501_2.pdf \
		build/plt/V502_1.pdf \

tables: \
		build/tab/V502_tab_b.tex \


build/plt/V501_%.pdf &: | build/plt V501/1_todo.py
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 V501/1_todo.py

build/plt/V502_1.pdf build/tab/V502_tab_b.tex &: | build/plt build/tab V502/1_spezifische_elektronenladung.py
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 V502/1_spezifische_elektronenladung.py

build/main.pdf: contents plots tables | build
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
