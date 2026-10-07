# Voeg de CSV-bestanden van alle groepsleden samen tot één dataset.
# Uitvoeren in je notebook met:  %run -i samenvoegen.py
# (NA de cel van taak 4: gebruikt KOLOMMEN, SCHEIDINGSTEKEN, lees_csv en schrijf_csv)
import csv
import glob
import os

INVOERMAP = "groepsdata"                                 # gedeelde map met alle bestanden
PATROON = os.path.join(INVOERMAP, "sysinfo_*.csv")       # afgesproken bestandsnaam
UITVOER = "sysinfo_groep.csv"                            # staat BUITEN de invoermap


def lees_kopregel(bestand):
    with open(bestand, newline="", encoding="utf-8-sig") as f:
        return next(csv.reader(f, delimiter=SCHEIDINGSTEKEN), [])


samengevoegd = {}  # computernaam -> rij; zo komt elke computer maar één keer voor
bestanden = sorted(glob.glob(PATROON))
print(f"{len(bestanden)} bestanden gevonden in '{INVOERMAP}'")

for bestand in bestanden:
    kop = lees_kopregel(bestand)
    ontbrekend = [k for k in KOLOMMEN if k not in kop]
    extra = [k for k in kop if k not in KOLOMMEN]

    if "computernaam" not in kop:
        print(f"  OVERGESLAGEN {bestand}: kolommen niet herkend (verkeerd scheidingsteken?)")
        continue
    if ontbrekend:
        print(f"  LET OP {bestand}: kolommen ontbreken {ontbrekend} -> lege cellen")
    if extra:
        print(f"  LET OP {bestand}: onbekende kolommen {extra} -> genegeerd")

    for rij in lees_csv(bestand):
        naam = rij.get("computernaam")
        if not naam:
            print(f"  OVERGESLAGEN rij zonder computernaam in {bestand}")
            continue
        if naam in samengevoegd:
            print(f"  LET OP: '{naam}' staat in meerdere bestanden, versie uit {bestand} gebruikt")
        samengevoegd[naam] = rij

schrijf_csv(list(samengevoegd.values()), UITVOER)

# Controle: resultaat opnieuw inlezen en ontbrekende gegevens tonen
resultaat = lees_csv(UITVOER)
print(f"\n{len(resultaat)} computers samengevoegd in '{UITVOER}'")
for kolom in KOLOMMEN:
    leeg = [r["computernaam"] for r in resultaat if r.get(kolom) is None]
    if leeg:
        print(f"  {kolom} ontbreekt bij: {', '.join(leeg)}")