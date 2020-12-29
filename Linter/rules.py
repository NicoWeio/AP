rules = [
{
'regex': r'\b(wir|uns[er]*|ich)\b',
'message': '"wir/uns/…" vermeiden',
'importance': 10,
}, {
'regex': r'\bman\b',
'message': '"man" vermeiden',
'importance': 10,
}, {
'regex': r'(?<!\\symup{)\\Delta',
'message': 'Delta wird aufrecht geschrieben → symup!',
'importance': 5,
}, {
# matcht auch "11.11.2020"
'regex': r'\d{5,}',
'message': 'lange Zahlen vermeiden',
'importance': 6,
}, {
# 'regex': r'0\.00',
'regex': r'0{3,}',
'message': 'Zahlen mit vielen Nullen vermeiden → wissenschaftliche Schreibweise?',
'importance': 4,
}, {
'regex': r'\+\/-|-\/\+',
'message': '+/- (bzw. -/+) in Textform → \\pm (bzw. \\mp) verwenden',
'importance': 5,
},
{
# https://de.wiktionary.org/wiki/Modul#Substantiv,_m
'regex': r'Elastizitätsmodule',
'message': 'Die E-Moduln (m.), nicht die E-Module (n.)',
'importance': 8,
}, {
#TODO: sollte *immer* Kommentar-Zeilen berücksichtigen
'regex': r'TODO',
'message': 'TODO-Notiz',
'importance': 7,
},
]
