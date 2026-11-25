"""Oefening 1 - Basisverbinding met Netmiko.

Doel: via SSH verbinden met een Cisco IOS-toestel, naar enable mode gaan,
het commando `show ssh` uitvoeren en de uitvoer tonen.

Dit is bewust het kale basisscript: alle parameters staan hard in de code,
zodat de vijf stappen van een Netmiko-sessie duidelijk zichtbaar blijven.
Oefening 2 maakt er variabelen van.

Uitvoeren:
    python oefening1.py
"""

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.110.177.102",
    "username": "cisco",
    "password": "Cisco123!",
    "secret": "Cisco123!",
}

# 1. verbinding opzetten over SSH
connection = ConnectHandler(**device)

# 2. naar privileged EXEC mode (enable)
connection.enable()

# 3. een show-commando versturen
output = connection.send_command("show ssh")

# 4. de uitvoer tonen
print(output)

# 5. de sessie netjes sluiten
connection.disconnect()
