all: build/main.pdf

plots: \
		build/plot_gelb_full.pdf \
		build/plot_nu_ug.pdf \
		build/plot_sqrt_gelb.pdf \
		build/plot_sqrt_gruen.pdf \
		build/plot_sqrt_ultraviolett.pdf \
		build/plot_sqrt_violett.pdf \

tables: \
		build/table_fitdata.tex \
		build/table_gelb.tex \
		build/table_gruen.tex \
		build/table_ultraviolett.tex \
		build/table_violett.tex \

build/plot_gelb_full.pdf: | build
		python3 2_gelb_full.py

build/plot_%.pdf &: | build
		python3 1_auswertung.py

build/table_fitdata.tex: | build
		python3 1_auswertung.py

build/table_%.tex &: | build
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

build:
	mkdir -p build

clean:
	rm -rf build

.PHONY: all clean plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
