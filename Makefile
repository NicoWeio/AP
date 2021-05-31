all: protokolle

dirnames := $(wildcard [DV]*)
pdfs := $(patsubst %,%/build/main.pdf,$(dirnames))

protokolle: $(pdfs)

%/build/main.pdf &:
	$(MAKE) -C $(patsubst %/build/main.pdf,%,$@)

.PHONY: all
