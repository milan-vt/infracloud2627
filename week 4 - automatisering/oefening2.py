"""Oefening 2 - Verbindingsscript met variabelen.

Doel: hetzelfde als oefening 1, maar de verbindingsparameters staan nu in
variabelen. Daardoor moet je maar op één plaats aanpassen als je naar een
ander toestel gaat, en kan je het script hergebruiken.

Extra tegenover oefening 1:
  - de parameters komen uit devices.py (één bron voor alle oefeningen)
  - de verbinding staat in een `with`-blok, zodat ze altijd gesloten wordt
  - foutafhandeling, zodat een onbereikbaar toestel een leesbare melding
    geeft in plaats van een stacktrace

Uitvoeren:
    python oefening2.py
"""

import os
import sys

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

# devices.py staat naast dit script. Python zoekt een eigen module enkel in
# de map van het script of in de huidige werkmap, dus starten we vanuit een
# andere map (of vanuit Jupyter) dan wordt devices.py niet gevonden. Deze
# twee regels zetten de map van dit bestand bij de zoekpaden.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())

from devices import get_device

# --- variabelen ---------------------------------------------------------
# Wil je de waarden liever in dit bestand zelf zien staan, dan kan je ze
# ook rechtstreeks invullen in plaats van devices.py te gebruiken:
#
#   v_device_type = "cisco_ios"
#   v_host        = "10.110.177.102"
#   v_ssh_port    = 22
#   v_username    = "cisco"
#   v_password    = "Cisco123!"
#   v_secret      = "Cisco123!"

device = get_device()
commando = "show ssh"


def main():
    print(f"Verbinden met {device['host']}:{device['port']} ...")

    try:
        # `with` sluit de SSH-sessie automatisch, ook bij een fout
        with ConnectHandler(**device) as connection:
            connection.enable()
            prompt = connection.find_prompt()
            print(f"Verbonden. Prompt van het toestel: {prompt}\n")

            output = connection.send_command(commando)
            print(f"--- {commando} ---")
            print(output)

    except NetmikoTimeoutException:
        print(f"FOUT: {device['host']} is niet bereikbaar op poort {device['port']}.")
        print("Controleer de VPN-verbinding, het IP-adres en of SSH openstaat.")
    except NetmikoAuthenticationException:
        print("FOUT: aanmelden mislukt. Controleer gebruikersnaam en wachtwoord.")


if __name__ == "__main__":
    main()
