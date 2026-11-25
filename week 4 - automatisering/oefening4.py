"""Oefening 4 - Uitvoer bewaren.

Doel: de gegevens uit oefening 3 niet alleen op het scherm tonen, maar ook
wegschrijven, zodat je er documentatie of een inventaris mee kan maken.

Drie manieren, van eenvoudig naar gestructureerd:

  1. Tekst  - omleiding vanuit de shell (geen code nodig):
                 python oefening3.py > output/router_inventory.txt
             of in dit script: output/<hostname>-inventaris.txt
  2. JSON   - gestructureerd, makkelijk terug in te lezen door een script
  3. Excel  - leesbaar voor mensen, vereist `pip install openpyxl`

Uitbreiding: verbinden met meerdere toestellen. Vul daarvoor de lijst
TOESTELLEN hieronder aan; het script loopt ze één voor één af.

Uitvoeren:
    python oefening4.py
"""

import json
import os
import sys
from datetime import datetime

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

# Zorgt dat devices.py en oefening3.py gevonden worden, ook als je dit
# script vanuit een andere map start (zie de uitleg in oefening2.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())

from devices import get_device
from oefening3 import toon_info, verzamel_info

# Map waarin de exportbestanden terechtkomen
OUTPUT_MAP = "output"

# Meerdere toestellen: voeg hier extra dictionaries toe, bv.
#   TOESTELLEN = [get_device(), {**get_device(), "host": "10.110.177.103"}]
TOESTELLEN = [get_device()]


# =======================================================================
#  Bewaren
# =======================================================================

def bewaar_tekst(info, pad):
    """Schrijf een leesbaar tekstrapport weg."""
    regels = []
    regels.append("Device Information")
    regels.append("------------------")
    regels.append(f"Hostname      : {info['hostname']}")
    regels.append(f"Model         : {info['model']}")
    regels.append(f"Serienummer   : {info['serienummer']}")
    regels.append(f"IOS-versie    : {info['ios_versie']}")
    regels.append(f"Uptime        : {info['uptime']}")
    regels.append("")
    regels.append("Interfaces")
    regels.append("----------")
    for intf in info["interfaces"]:
        regels.append(f"  {intf['naam']:<25} {intf['ip']:<18} {intf['status']}")
    regels.append("")
    regels.append("CDP-buren")
    regels.append("---------")
    for buur in info["buren"]:
        regels.append(f"  {buur['naam']} via {buur['lokale_poort']}")
    regels.append("")
    regels.append("Routes")
    regels.append("------")
    for route in info["routes"]:
        regels.append(f"  [{route['protocol']}] {route['netwerk']} via {route['via']}")

    with open(pad, "w", encoding="utf-8") as bestand:
        bestand.write("\n".join(regels) + "\n")
    print(f"  tekst  -> {pad}")


def bewaar_json(info, pad):
    """Schrijf alle gegevens weg als JSON (gestructureerd formaat)."""
    with open(pad, "w", encoding="utf-8") as bestand:
        json.dump(info, bestand, indent=4, ensure_ascii=False)
    print(f"  json   -> {pad}")


def bewaar_excel(info, pad):
    """Schrijf de gegevens weg als spreadsheet (vereist openpyxl)."""
    try:
        from openpyxl import Workbook
    except ImportError:
        print("  excel  -> overgeslagen (voer eerst uit: pip install openpyxl)")
        return

    werkboek = Workbook()

    # Blad 1: algemene gegevens als sleutel/waarde
    blad = werkboek.active
    blad.title = "Toestel"
    blad.append(["Eigenschap", "Waarde"])
    for sleutel in ("hostname", "model", "serienummer", "ios_versie", "uptime"):
        blad.append([sleutel, info[sleutel]])

    # Blad 2: interfaces
    blad_intf = werkboek.create_sheet("Interfaces")
    blad_intf.append(["Interface", "IP-adres", "Status", "Protocol"])
    for intf in info["interfaces"]:
        blad_intf.append([intf["naam"], intf["ip"], intf["status"], intf["protocol"]])

    # Blad 3: CDP-buren
    blad_buren = werkboek.create_sheet("CDP-buren")
    blad_buren.append(["Buur", "Lokale poort", "Externe poort"])
    for buur in info["buren"]:
        blad_buren.append(
            [buur["naam"], buur["lokale_poort"], buur["externe_poort"]]
        )

    # Blad 4: routes
    blad_routes = werkboek.create_sheet("Routes")
    blad_routes.append(["Netwerk", "Protocol", "Via"])
    for route in info["routes"]:
        blad_routes.append([route["netwerk"], route["protocol"], route["via"]])

    werkboek.save(pad)
    print(f"  excel  -> {pad}")


# =======================================================================

def main():
    os.makedirs(OUTPUT_MAP, exist_ok=True)
    tijdstip = datetime.now().strftime("%Y%m%d-%H%M")

    for toestel in TOESTELLEN:
        print(f"\nVerbinden met {toestel['host']} ...")
        try:
            with ConnectHandler(**toestel) as connection:
                connection.enable()
                info = verzamel_info(connection)
        except NetmikoTimeoutException:
            print(f"FOUT: {toestel['host']} is niet bereikbaar. Staat de VPN aan?")
            continue
        except NetmikoAuthenticationException:
            print(f"FOUT: aanmelden op {toestel['host']} mislukt.")
            continue

        # tijdstip van de inventarisatie mee opslaan
        info["verzameld_op"] = datetime.now().isoformat(timespec="seconds")
        info["ip_adres"] = toestel["host"]

        toon_info(info)

        basis = os.path.join(OUTPUT_MAP, f"{info['hostname']}-{tijdstip}")
        print("\nBestanden:")
        bewaar_tekst(info, f"{basis}.txt")
        bewaar_json(info, f"{basis}.json")
        bewaar_excel(info, f"{basis}.xlsx")


if __name__ == "__main__":
    main()
