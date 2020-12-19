all: build/main.pdf

build/table_einseitig_eckig.tex build/plot_einseitig_eckig.pdf: | build
	python3 einseitig_eckig.py

build/table_einseitig_rund.tex build/plot_einseitig_rund.pdf: | build
	python3 einseitig_rund.py

build/table_beidseitig_rund.tex build/plot_beidseitig_rund_*.pdf: | build
	python3 beidseitig_rund.py

tables: build/table_einseitig_eckig.tex build/table_einseitig_rund.tex build/table_beidseitig_rund.tex
	python3 tables.py

plots: build/plot_einseitig_eckig.pdf build/plot_einseitig_rund.pdf build/plot_beidseitig_rund_*.pdf

build/main.pdf: main.tex lit.bib tables plots | build
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

.PHONY: all clean

#NOTE: Vollständiges Rekompilieren lässt sich mit `make -B` erzwingen
