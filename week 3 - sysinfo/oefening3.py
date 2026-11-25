import json
import os
import sys

# Zorgt dat oefening1.py en oefening2.py gevonden worden, ook als je dit
# script vanuit een andere map start.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())

from oefening1 import collect_system_info
from oefening2 import filter_info

gefilterd = filter_info(collect_system_info())

# 1. dict -> JSON-tekst
json_tekst = json.dumps(gefilterd, indent=2)

# 2. JSON-tekst opslaan in een bestand
with open("sysinfo.json", "w", encoding="utf-8") as f:
    f.write(json_tekst)

# 3. Bestand opnieuw inlezen als dict
with open("sysinfo.json", encoding="utf-8") as f:
    ingelezen = json.load(f)

# 4. Controle per sleutel en in zijn geheel
for sleutel, waarde in gefilterd.items():
    status = "OK" if ingelezen.get(sleutel) == waarde else "VERSCHIL"
    print(f"{status:8} {sleutel}: {ingelezen.get(sleutel)}")
print("Volledig gelijk:", gefilterd == ingelezen)