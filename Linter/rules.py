rules = [
{
'regex': r'\b(wir|uns[er]*|ich)\b',
'message': '"wir/uns/…" vermeiden',
}, {
'regex': r'\bman\b',
'message': '"man" vermeiden',
}, {
'regex': r'(?<!\\symup{)\\Delta',
'message': 'Delta wird aufrecht geschrieben → symup!',
}, {
# matcht auch "11.11.2020"
'regex': r'\d{5,}',
'message': 'lange Zahlen vermeiden',
}, {
# 'regex': r'0\.00',
'regex': r'0{3,}',
'message': 'Zahlen mit vielen Nullen vermeiden → wissenschaftliche Schreibweise?',
}, {
'regex': r'\+\/-|-\/\+',
'message': '+/- (bzw. -/+) in Textform → \\pm (bzw. \\mp) verwenden',
},
{
# https://de.wiktionary.org/wiki/Modul#Substantiv,_m
'regex': r'Elastizitätsmodule',
'message': 'DER E-Modul, nicht DAS E-Modul',
}, {
#TODO: sollte *immer* Kommentar-Zeilen berücksichtigen
'regex': r'TODO',
'message': 'TODO-Notiz',
},
]
