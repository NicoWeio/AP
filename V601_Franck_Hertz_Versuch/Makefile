all: build/main.pdf

data: \
	build/dat/energieverteilung_148.csv \
	build/dat/energieverteilung_23_7.csv \
	build/dat/franck_hertz_166_6.csv \
	build/dat/franck_hertz_183_8.csv \

build/dat/%.csv &: | build/dat
	python3 0_prepare.py

plots: \
	build/plt/energieverteilung_int.pdf \
	build/plt/energieverteilung_diff.pdf \
	build/plt/franck_hertz_166_6.pdf \
	build/plt/franck_hertz_183_8.pdf \

tables: \
	build/tab/freie_weglaenge.tex

build/tab/freie_weglaenge.tex: | build/tab
	python3 1_freie_weglaenge.py

build/plt/energieverteilung_%.pdf &: 2_energieverteilung.py build/dat/energieverteilung_148.csv build/dat/energieverteilung_23_7.csv | build/plt
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 2_energieverteilung.py

build/plt/franck_hertz_%.pdf &: 3_franck_hertz_kurven.py build/dat/franck_hertz_166_6.csv build/dat/franck_hertz_183_8.csv | build/plt
	MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 3_franck_hertz_kurven.py

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

build build/dat build/plt build/tab &:
	mkdir -p build
	mkdir -p build/dat
	mkdir -p build/plt
	mkdir -p build/tab

clean:
	rm -rf build

.PHONY: all clean data plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
