from netmiko import ConnectHandler

device = {
"device_type": "cisco_ios",
"host": "192.168.1.1",
"username": "admin",
"password": "Cisco123!",
"secret": "Cisco123!",
}

connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show ssh")
print(output)

connection.disconnect()