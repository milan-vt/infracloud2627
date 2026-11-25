"""Centrale verbindingsparameters voor de Netmiko-oefeningen van week 4.

De gegevens van het labotoestel staan hier op één plaats, zodat de
oefeningen zelf enkel nog over automatisatie gaan en niet over
configuratie.

Wachtwoorden horen niet in een git-repository. Zet daarom bij voorkeur
omgevingsvariabelen; de waarden hieronder zijn enkel een fallback om
lokaal te testen.

PowerShell (enkel geldig in het huidige venster):
    $env:IOS_HOST     = "10.110.177.102"
    $env:IOS_USERNAME = "cisco"
    $env:IOS_PASSWORD = "Cisco123!"
    $env:IOS_SECRET   = "Cisco123!"
"""

import os

# --- verbindingsparameters, als variabelen ------------------------------
v_device_type = "cisco_ios"
v_host = os.getenv("IOS_HOST", "10.110.177.102")
v_ssh_port = int(os.getenv("IOS_PORT", "22"))
v_username = os.getenv("IOS_USERNAME", "cisco")
v_password = os.getenv("IOS_PASSWORD", "Cisco123!")
v_secret = os.getenv("IOS_SECRET", "Cisco123!")

# Dictionary zoals Netmiko ze verwacht (** = uitpakken als argumenten).
device = {
    "device_type": v_device_type,
    "host": v_host,
    "port": v_ssh_port,
    "username": v_username,
    "password": v_password,
    "secret": v_secret,
}


def get_device():
    """Geef een kopie van de device-dictionary terug.

    Een kopie, zodat een oefening die er iets aan wijzigt (bv. een
    session_log toevoegen) de andere oefeningen niet beinvloedt.
    """
    return dict(device)
