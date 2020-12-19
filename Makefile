all: protokolle

protokolle: \
	D206_Waermepumpe/build/main.pdf \
	V103_Biegung_elastischer_Staebe/build/main.pdf \
	V302_Brueckenschaltung/build/main.pdf

D206_Waermepumpe/build/main.pdf:
	$(MAKE) -C D206_Waermepumpe

V103_Biegung_elastischer_Staebe/build/main.pdf:
	$(MAKE) -C V103_Biegung_elastischer_Staebe

V302_Brueckenschaltung/build/main.pdf:
	$(MAKE) -C V302_Brueckenschaltung
