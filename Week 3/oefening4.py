import csv
import os
 
CSV_BESTAND = "sysinfo_computers.csv"
SCHEIDINGSTEKEN = ";" 
 
KOLOMMEN = [
    "computernaam", "computermodel", "processor", "cpu_fysieke_cores",
    "cpu_max_frequentie_mhz", "ram_totaal_gib", "opslag_bestandssysteem",
    "opslag_capaciteit_gib", "mac_adres", "ipv4_adres", "ipv6_adres",
    "ipv6_link_local",
]
# Kolommen die bij het inlezen terug een getal moeten worden (CSV bevat enkel tekst)
GETALLEN = {
    "cpu_fysieke_cores": int,
    "cpu_max_frequentie_mhz": float,
    "ram_totaal_gib": float,
    "opslag_capaciteit_gib": float,
}
 
 
def naar_cel(waarde):
    """Python-waarde -> tekst in de CSV."""
    if waarde is None:
        return ""    
    if isinstance(waarde, float):
        return str(waarde).replace(".", ",") # decimale komma Excel
    return str(waarde)
 
def van_cel(kolom, tekst):
    """Tekst uit de CSV -> Python-waarde."""
    if tekst == "":
        return None
    if kolom in GETALLEN:
        return GETALLEN[kolom](tekst.replace(",", "."))
    return tekst
 
 
def lees_csv(bestand=CSV_BESTAND):
    """Leest het CSV-bestand in als een lijst van dicts (één dict per computer)."""
    if not os.path.exists(bestand):
        return []
    with open(bestand, newline="", encoding="utf-8-sig") as f:
        lezer = csv.DictReader(f, delimiter=SCHEIDINGSTEKEN)
        return [{k: van_cel(k, v) for k, v in rij.items()} for rij in lezer]
 
 
def schrijf_csv(rijen, bestand=CSV_BESTAND):
    """Schrijft een lijst van dicts weg: één rij per computer."""
    with open(bestand, "w", newline="", encoding="utf-8-sig") as f:
        schrijver = csv.DictWriter(f, fieldnames=KOLOMMEN, delimiter=SCHEIDINGSTEKEN)
        schrijver.writeheader()
        for rij in rijen:
            schrijver.writerow({k: naar_cel(rij.get(k)) for k in KOLOMMEN})
 
 
# Deze computer toevoegen, staat hij er al in, dan wordt zijn rij vervangen.
gefilterd = filter_info(collect_system_info())
rijen = [r for r in lees_csv() if r["computernaam"] != gefilterd["computernaam"]]
rijen.append(gefilterd)
schrijf_csv(rijen)
 
# Controle: opnieuw inlezen en vergelijken met de oorspronkelijke dict
mijn_rij = next(r for r in lees_csv() if r["computernaam"] == gefilterd["computernaam"])
print("Rij gelijk aan oorspronkelijke dict:", mijn_rij == gefilterd)