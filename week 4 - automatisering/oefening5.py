"""Oefening 5 - Toestellen configureren met Netmiko.

Doel: in plaats van configuratieregels manueel in te typen, stuurt het
script ze automatisch naar het toestel. Zo krijgen alle toestellen
dezelfde basisinstellingen.

Wat dit script doet:
  1. verbinden over SSH
  2. naar enable mode
  3. naar global configuration mode (Netmiko doet dit zelf via
     send_config_set)
  4. wachtwoordversleuteling aanzetten : service password-encryption
  5. een login-banner zetten           : banner motd
  6. de configuratie bewaren           : write memory
  7. controleren of alles effectief in de running-config staat

Opgelet: dit script WIJZIGT de configuratie van het toestel. Het vraagt
daarom eerst een bevestiging. Wil je enkel controleren zonder te wijzigen,
voer dan `python oefening5.py --controle` uit.

Uitvoeren:
    python oefening5.py
    python oefening5.py --controle
"""

import os
import sys

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

# Zorgt dat devices.py gevonden wordt, ook als je dit script vanuit een
# andere map start (zie de uitleg in oefening2.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())

from devices import get_device

# De configuratieregels die we willen doorvoeren
config_commands = [
    "service password-encryption",
    "banner motd #Unauthorized access is prohibited#",
]

# Waarop we nadien controleren in de running-config
verwachte_regels = [
    "service password-encryption",
    "banner motd",
]


def configureer(connection):
    """Stuur de configuratieregels naar het toestel en bewaar ze."""
    print("Configuratie doorsturen ...")
    output = connection.send_config_set(config_commands)
    print(output)

    print("Configuratie bewaren (write memory) ...")
    print(connection.save_config())


def controleer(connection):
    """Controleer of de regels in de running-config staan."""
    print("\nVerificatie")
    print("-----------")
    running_config = connection.send_command("show running-config")

    alles_ok = True
    for regel in verwachte_regels:
        if regel in running_config:
            print(f"  OK       : '{regel}' staat in de running-config")
        else:
            print(f"  ONTBREEKT: '{regel}' staat NIET in de running-config")
            alles_ok = False

    # De banner zelf tonen ter controle
    banner = connection.send_command("show running-config | begin banner")
    if banner.strip():
        print("\nBanner in de configuratie:")
        print(banner)

    return alles_ok


def main():
    enkel_controle = "--controle" in sys.argv
    device = get_device()

    if not enkel_controle:
        print("Dit script WIJZIGT de configuratie van het toestel:")
        for commando in config_commands:
            print(f"  - {commando}")
        antwoord = input(f"\nDoorgaan op {device['host']}? (ja/nee): ").strip().lower()
        if antwoord not in ("ja", "j", "yes", "y"):
            print("Afgebroken, er is niets gewijzigd.")
            return

    print(f"\nVerbinden met {device['host']} ...")
    try:
        with ConnectHandler(**device) as connection:
            connection.enable()

            if not enkel_controle:
                configureer(connection)

            alles_ok = controleer(connection)

    except NetmikoTimeoutException:
        print(f"FOUT: {device['host']} is niet bereikbaar. Staat de VPN aan?")
        return
    except NetmikoAuthenticationException:
        print("FOUT: aanmelden mislukt. Controleer gebruikersnaam en wachtwoord.")
        return

    print()
    if alles_ok:
        print("Resultaat: de configuratie is correct toegepast.")
    else:
        print("Resultaat: niet alle regels zijn teruggevonden, controleer manueel.")


if __name__ == "__main__":
    main()
