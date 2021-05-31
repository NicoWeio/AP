all: build/main.pdf

plots: \
		build/plt/led.pdf \
		build/plt/phasen.pdf \
		build/plt/phasen_noise.pdf \

tables: \
		build/tab/led.tex \


build/tab/led.tex: | build/tab
		python3 0_messwerte.py

build/plt/phasen.pdf build/plt/phasen_noise.pdf &: | build/plt
		python3 1_phasenabhaengigkeit.py

build/plt/led.pdf &: | build/plt
		python3 2_led.py


build/main.pdf: main.tex content lit.bib plots tables | build
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
