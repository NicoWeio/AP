all: build/main.pdf

plots: \
		build/plot_bragg.pdf \
		build/plot_brom.pdf \
		build/plot_emissionsspektrum.pdf \
		build/plot_gallium.pdf \
		build/plot_moseley.pdf \
		build/plot_rubidium.pdf \
		build/plot_strontium.pdf \
		build/plot_zink.pdf \
		build/plot_zirkonium.pdf \

tables: \
		build/table_mess_absorptionsspektren.tex \
		build/table_mess_bragg.tex \
		build/table_mess_brom.tex \
		build/table_mess_emissionsspektrum_4col.tex \
		build/table_mess_gallium.tex \
		build/table_mess_rubidium.tex \
		build/table_mess_strontium.tex \
		build/table_mess_zink.tex \
		build/table_mess_zirkonium.tex \

build/table_%.tex &: | build
		python3 0_messwerte.py

build/plot_%.pdf &: | build
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 1_bragg.py
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 2_emissionsspektrum.py
		MATPLOTLIBRC=../matplotlibrc TEXINPUTS=$$(pwd)/..: python3 3_absorptionsspektren.py

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
