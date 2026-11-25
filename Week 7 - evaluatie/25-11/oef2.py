
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.10.20.171",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
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
