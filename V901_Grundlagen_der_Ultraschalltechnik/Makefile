all: build/main.pdf

plots: \
		build/plt/visualization.pdf \
		build/plt/visualization_bars.pdf \
		build/plt/schallgeschwindigkeit.pdf \
		build/plt/absorptionskurve.pdf \

tables: \
		build/tab/mess_schieblehre.tex \
		build/tab/mess_ultraschall.tex \


build/tab/mess_schieblehre.tex: | build/tab
		python3 0_messwerte.py

build/plt/visualization.pdf: | build/plt
		python3 1_visualization.py

build/plt/visualization_bars.pdf: | build/plt
		python3 1b_visualization_bars.py

build/plt/schallgeschwindigkeit.pdf: | build/plt
		python3 2_schallgeschwindigkeit.py

build/plt/absorptionskurve.pdf: | build/plt
		python3 3_absorptionskoeffizient.py

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

.PHONY: all clean plots tables

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
