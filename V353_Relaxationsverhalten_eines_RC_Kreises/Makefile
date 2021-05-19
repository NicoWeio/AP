all: build/main.pdf

plots: \
		build/plt/1_rc_via_t.pdf \
		build/plt/2_rc_via_freq.pdf \
		build/plt/3_rc_via_phi.pdf \
		build/plt/3_polar.pdf \

tables: \
		build/tab/mess_1.tex \
		build/tab/mess_2.tex \


build/tab/mess_%.tex &: | build/tab
		python3 0_messwerte.py

build/plt/1_rc_via_t.pdf &: | build/plt
		python3 1_rc_via_t.py

build/plt/2_rc_via_freq.pdf &: | build/plt
		python3 2_rc_via_freq.py

build/plt/3_rc_via_phi.pdf build/plt/3_polar.pdf &: | build/plt
		python3 3_rc_via_phi.py


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
