"""Oefening 3 - Informatie verzamelen van een Cisco-toestel.

Doel: automatisch dezelfde gegevens ophalen die een netwerkbeheerder
anders manueel via de CLI verzamelt:

    minimaal : hostname, model, serienummer, IOS-versie
    bonus    : interfacestatus, CDP-buren, routeringstabel

Gebruikte show-commando's
    show version              -> identiteit (hostname, model, serie, IOS)
    show ip interface brief   -> interfacestatus
    show cdp neighbors        -> aangesloten toestellen
    show ip route             -> routeringsinformatie

Er zijn drie manieren om de hostname uit `show version` te halen: met een
regex, met split, of met TextFSM. Alle drie staan hieronder uitgewerkt in
aparte functies, zodat je ze kan vergelijken. Voor de rest van het script
gebruiken we TextFSM, omdat dat meteen een nette dictionary oplevert.

Uitvoeren:
    python oefening3.py
"""

import os
import re
import sys

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

# Zorgt dat devices.py gevonden wordt, ook als je dit script vanuit een
# andere map start (zie de uitleg in oefening2.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())

from devices import get_device


# =======================================================================
#  Drie manieren om de hostname uit `show version` te halen
# =======================================================================

def hostname_via_regex(show_version_output):
    """Methode 1 - REGEX. Zoekt het patroon '<hostname> uptime is'."""
    match = re.search(r"(\S+) uptime is", show_version_output)
    return match.group(1) if match else "Onbekend"


def hostname_via_split(show_version_output):
    """Methode 2 - SPLIT. Eenvoudiger: eerste woord van de uptime-regel."""
    for line in show_version_output.splitlines():
        if "uptime is" in line:
            return line.split()[0]
    return "Onbekend"


def hostname_via_textfsm(connection):
    """Methode 3 - TextFSM. Netmiko parset de uitvoer naar een dict."""
    parsed = connection.send_command("show version", use_textfsm=True)
    if isinstance(parsed, list) and parsed:
        return parsed[0].get("hostname", "Onbekend")
    return "Onbekend"


# =======================================================================
#  Gegevens verzamelen
# =======================================================================

def _eerste(waarde, standaard="Onbekend"):
    """TextFSM geeft sommige velden als lijst terug (bv. serial, hardware)."""
    if isinstance(waarde, list):
        return waarde[0] if waarde else standaard
    return waarde or standaard


def verzamel_info(connection):
    """Haal alle gewenste informatie op en geef ze terug als dictionary."""
    info = {}

    # --- identiteit (show version, geparset met TextFSM) ----------------
    versie = connection.send_command("show version", use_textfsm=True)
    feiten = versie[0] if isinstance(versie, list) and versie else {}

    info["hostname"] = _eerste(feiten.get("hostname"))
    info["model"] = _eerste(feiten.get("hardware"))
    info["serienummer"] = _eerste(feiten.get("serial"))
    info["ios_versie"] = _eerste(feiten.get("version"))
    info["uptime"] = _eerste(feiten.get("uptime"))

    # --- interfaces (show ip interface brief) ---------------------------
    interfaces = connection.send_command(
        "show ip interface brief", use_textfsm=True
    )
    info["interfaces"] = []
    if isinstance(interfaces, list):
        for intf in interfaces:
            info["interfaces"].append(
                {
                    "naam": intf.get("interface", ""),
                    "ip": intf.get("ip_address", ""),
                    "status": intf.get("status", ""),
                    "protocol": intf.get("proto", intf.get("protocol", "")),
                }
            )

    # --- CDP-buren (show cdp neighbors) ---------------------------------
    buren = connection.send_command("show cdp neighbors", use_textfsm=True)
    info["buren"] = []
    if isinstance(buren, list):
        for buur in buren:
            info["buren"].append(
                {
                    "naam": buur.get("neighbor", buur.get("destination_host", "")),
                    "lokale_poort": buur.get("local_interface", ""),
                    "externe_poort": buur.get("neighbor_interface", ""),
                }
            )

    # --- routes (show ip route) -----------------------------------------
    routes = connection.send_command("show ip route", use_textfsm=True)
    info["routes"] = []
    if isinstance(routes, list):
        for route in routes:
            netwerk = route.get("network", "")
            masker = route.get("mask", "")
            info["routes"].append(
                {
                    "netwerk": f"{netwerk}/{masker}" if masker else netwerk,
                    "protocol": route.get("protocol", ""),
                    "via": _eerste(route.get("nexthop_ip"), "")
                    or _eerste(route.get("nexthop_if"), ""),
                }
            )

    return info


# =======================================================================
#  Afdrukken
# =======================================================================

def toon_info(info):
    """Druk de verzamelde gegevens gestructureerd af."""
    print("Device Information")
    print("------------------")
    print(f"Hostname      : {info['hostname']}")
    print(f"Model         : {info['model']}")
    print(f"Serienummer   : {info['serienummer']}")
    print()

    print("Software Information")
    print("--------------------")
    print(f"IOS-versie    : {info['ios_versie']}")
    print(f"Uptime        : {info['uptime']}")
    print()

    print("Interfaces")
    print("----------")
    print(f"Aantal interfaces: {len(info['interfaces'])}")
    for intf in info["interfaces"]:
        print(f"  {intf['naam']:<25} {intf['ip']:<18} {intf['status']}")
    print()

    print("Connected Devices (CDP Neighbors)")
    print("---------------------------------")
    if info["buren"]:
        for buur in info["buren"]:
            print(f"  {buur['naam']} via {buur['lokale_poort']}")
    else:
        print("  geen CDP-buren gevonden")
    print()

    print("Routing Table")
    print("-------------")
    if info["routes"]:
        for route in info["routes"]:
            via = f" via {route['via']}" if route["via"] else ""
            print(f"  [{route['protocol']}] {route['netwerk']}{via}")
    else:
        print("  geen routes gevonden")


def main():
    device = get_device()
    print(f"Verbinden met {device['host']} ...\n")

    try:
        with ConnectHandler(**device) as connection:
            connection.enable()

            # De drie parse-methodes naast elkaar, ter vergelijking
            show_version = connection.send_command("show version")
            print("Hostname volgens de drie methodes")
            print("---------------------------------")
            print(f"  regex   : {hostname_via_regex(show_version)}")
            print(f"  split   : {hostname_via_split(show_version)}")
            print(f"  textfsm : {hostname_via_textfsm(connection)}")
            print()

            info = verzamel_info(connection)
            toon_info(info)

    except NetmikoTimeoutException:
        print(f"FOUT: {device['host']} is niet bereikbaar. Staat de VPN aan?")
    except NetmikoAuthenticationException:
        print("FOUT: aanmelden mislukt. Controleer gebruikersnaam en wachtwoord.")


if __name__ == "__main__":
    main()
