all: protokolle

protokolle: \
	D206_Waermepumpe/build/main.pdf \
	D602_Roentgenemission_und_Absorption/build/main.pdf \
	D702_Aktivierung_mit_Neutronen/build/main.pdf \
	D703_Geiger_Mueller_Zaehlrohr/build/main.pdf \
	V103_Biegung_elastischer_Staebe/build/main.pdf \
	V204_Waermeleitung/build/main.pdf \
	V302_Brueckenschaltung/build/main.pdf \
	V353_Relaxationsverhalten_eines_RC_Kreises/build/main.pdf \
	V401_Michelson_Interferometer/build/main.pdf \
	V500_Photoeffekt/build/main.pdf \
	V606_Suszeptibilitaet_paramagnetischer_Substanzen/build/main.pdf \
	V901_Grundlagen_der_Ultraschalltechnik/build/main.pdf \

D206_Waermepumpe/build/main.pdf:
	$(MAKE) -C D206_Waermepumpe

D602_Roentgenemission_und_Absorption/build/main.pdf:
	$(MAKE) -C D602_Roentgenemission_und_Absorption

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

V353_Relaxationsverhalten_eines_RC_Kreises/build/main.pdf:
	$(MAKE) -C V353_Relaxationsverhalten_eines_RC_Kreises

V401_Michelson_Interferometer/build/main.pdf:
	$(MAKE) -C V401_Michelson_Interferometer

V500_Photoeffekt/build/main.pdf:
	$(MAKE) -C V500_Photoeffekt

V606_Suszeptibilitaet_paramagnetischer_Substanzen/build/main.pdf:
	$(MAKE) -C V606_Suszeptibilitaet_paramagnetischer_Substanzen

V901_Grundlagen_der_Ultraschalltechnik/build/main.pdf:
	$(MAKE) -C V901_Grundlagen_der_Ultraschalltechnik
