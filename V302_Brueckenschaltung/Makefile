all: build/main.pdf

build/plot1.pdf: main.py | build
	TEXINPUTS=$$(pwd): python3 main.py

build/main.pdf: build/plot1.pdf

build/main.pdf: main.tex lit.bib | build
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
