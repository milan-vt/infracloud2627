import json

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