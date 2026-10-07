import ipaddress
import re
from collections import Counter
 
DATASET = "sysinfo_groep.csv"
MAC_PATROON = re.compile(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$")
 
 
def controleer_rij(r):
    """Geeft een lijst met problemen terug voor één computer."""
    fouten = []
    # Formaat
    if r["mac_adres"] and not MAC_PATROON.match(r["mac_adres"]):
        fouten.append(f"ongeldig MAC-adres {r['mac_adres']}")
    try:
        if r["ipv4_adres"] and ipaddress.IPv4Address(r["ipv4_adres"]).is_link_local:
            fouten.append("IPv4 is 169.254.x.x (geen DHCP-adres gekregen)")
    except ValueError:
        fouten.append(f"ongeldig IPv4-adres {r['ipv4_adres']}")
    if r["ipv6_link_local"] and not r["ipv6_link_local"].startswith("fe80"):
        fouten.append("link-local adres begint niet met fe80")
    # Plausibiliteit (vangt ook verkeerde eenheden, bv. bytes in plaats van GiB)
    if r["ram_totaal_gib"] is not None and not 1 <= r["ram_totaal_gib"] <= 512:
        fouten.append(f"onwaarschijnlijke RAM: {r['ram_totaal_gib']} GiB")
    if r["opslag_capaciteit_gib"] is not None and not 16 <= r["opslag_capaciteit_gib"] <= 20000:
        fouten.append(f"onwaarschijnlijke opslag: {r['opslag_capaciteit_gib']} GiB")
    if r["cpu_fysieke_cores"] is not None and not 1 <= r["cpu_fysieke_cores"] <= 128:
        fouten.append(f"onwaarschijnlijk aantal cores: {r['cpu_fysieke_cores']}")
    return fouten
 
 
dataset = lees_csv(DATASET)
 
# 1. Controles per computer
for r in dataset:
    for fout in controleer_rij(r):
        print(f"  {r['computernaam']}: {fout}")
 
# 2. Controles over de hele dataset: dingen die uniek moeten zijn
for kolom in ("computernaam", "mac_adres"):
    telling = Counter(r[kolom] for r in dataset if r[kolom])
    for waarde, aantal in telling.items():
        if aantal > 1:
            print(f"  {kolom} '{waarde}' komt {aantal} keer voor")
 
# 3. Eigen computer: opgeslagen gegevens vergelijken met een nieuwe meting
nu = filter_info(collect_system_info())
opgeslagen = next((r for r in dataset if r["computernaam"] == nu["computernaam"]), None)
if opgeslagen is None:
    print(f"  Deze computer ({nu['computernaam']}) staat niet in de dataset")
else:
    for kolom, waarde in nu.items():
        if opgeslagen.get(kolom) != waarde:
            print(f"  Verschil bij {kolom}: dataset={opgeslagen.get(kolom)}  nu={waarde}")
print("Controle klaar.")