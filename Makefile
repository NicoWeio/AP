all: protokolle

protokolle: \
	D206_Waermepumpe/build/main.pdf \
	D702_Aktivierung_mit_Neutronen/build/main.pdf \
	D703_Geiger_Mueller_Zaehlrohr/build/main.pdf \
	V103_Biegung_elastischer_Staebe/build/main.pdf \
	V204_Waermeleitung/build/main.pdf \
	V302_Brueckenschaltung/build/main.pdf

D206_Waermepumpe/build/main.pdf:
	$(MAKE) -C D206_Waermepumpe

D702_Aktivierung_mit_Neutronen/build/main.pdf:
	$(MAKE) -C D702_Aktivierung_mit_Neutronen

D703_Geiger_Mueller_Zaehlrohr/build/main.pdf:
	$(MAKE) -C D703_Geiger_Mueller_Zaehlrohr

V103_Biegung_elastischer_Staebe/build/main.pdf:
	$(MAKE) -C V103_Biegung_elastischer_Staebe

V204_Waermeleitung/build/main.pdf:
	$(MAKE) -C V204_Waermeleitung

V302_Brueckenschaltung/build/main.pdf:
	$(MAKE) -C V302_Brueckenschaltung
