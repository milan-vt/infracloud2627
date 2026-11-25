from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.10.20.171",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

# Connecteer met de apperatuur via ssh
connection = ConnectHandler(**device)
connection.enable()

show_version = connection.send_command("show version")
show_interfaces = connection.send_command("show ip interface brief")

print(show_version)
print(show_interfaces)

connection.disconnect()

