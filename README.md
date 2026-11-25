# Infrastructure & Cloud — 2026/2027

Oefeningen en labo's voor het vak **Infrastructure & Cloud** (Odisee).
Per lesweek staat er één map met de briefing van die week en de bijhorende oefeningen.

---

## Overzicht

| Week | Onderwerp | Briefing | Oefeningen |
|------|-----------|----------|------------|
| 1 | Werkomgeving opzetten | — | geen bestanden in deze repository |
| 2 | Kennismaking met Python | [Sep30-2026.md](Week%202%20-%20python%20experiments/Sep30-2026.md) | [notebook](Week%202%20-%20python%20experiments/python_experiments.ipynb) |
| 3 | System Information Scripting | [README](week%203%20-%20sysinfo/README.md) | oefening 1 – 7 |
| 4 | Netwerkautomatisatie met Netmiko en Ansible | [README](week%204/README.md) | oefening 1 – 9 |

---

## Week 3 — System Information Scripting

[Briefing](week%203%20-%20sysinfo/README.md) — systeeminformatie verzamelen, filteren en
exporteren naar JSON, CSV en een spreadsheet. De uitgewerkte versie in notebookvorm staat in
[week_3.ipynb](week%203%20-%20sysinfo/week_3.ipynb).

| # | Opdracht | Bestand |
|---|----------|---------|
| 1 | Basisscript uitvoeren en de structuur van de dictionary onderzoeken | [oefening1.py](week%203%20-%20sysinfo/oefening1.py) |
| 2 | Relevante informatie filteren naar een nieuwe dictionary | [oefening2.py](week%203%20-%20sysinfo/oefening2.py) |
| 3 | Dictionary omzetten naar JSON, bewaren en opnieuw inlezen | [oefening3.py](week%203%20-%20sysinfo/oefening3.py) |
| 4 | Informatie transformeren naar een CSV-bestand | [oefening4.py](week%203%20-%20sysinfo/oefening4.py) |
| 5 | Gegevens omzetten naar een spreadsheetbestand | [oefening5.py](week%203%20-%20sysinfo/oefening5.py) |
| 6 | CSV-bestanden van alle groepsleden samenvoegen tot één dataset | [oefening6.py](week%203%20-%20sysinfo/oefening6.py) |
| 7 | De samengevoegde dataset valideren | [oefening7.py](week%203%20-%20sysinfo/oefening7.py) |

De scripts bouwen op elkaar verder: oefening 2 importeert uit oefening 1, oefening 3 en 4 uit
oefening 1 en 2, en oefening 5 tot 7 uit oefening 4. Draai ze dus in volgorde.
Benodigde modules: `psutil` en, voor oefening 5, `openpyxl`.

---

## Week 4 — Netwerkautomatisatie met Netmiko en Ansible

[Briefing](week%204/README.md) — Cisco IOS-toestellen automatiseren, eerst met Netmiko (Python),
daarna met Ansible-playbooks.

| # | Opdracht | Bestand |
|---|----------|---------|
| 1 | Basisverbinding met Netmiko, `show ssh` uitvoeren | [oefening1.py](week%204/oefening1.py) |
| 2 | Verbindingsscript met variabelen | [oefening2.py](week%204/oefening2.py) |
| 3 | Informatie verzamelen van een Cisco-toestel | [oefening3.py](week%204/oefening3.py) |
| 4 | Uitvoer bewaren als tekst, JSON en spreadsheet | [oefening4.py](week%204/oefening4.py) |
| 5 | Toestellen configureren en verifiëren | [oefening5.py](week%204/oefening5.py) |
| 6 | Ansible: gegevens verzamelen met `ios_facts` | [oefening6_ios_facts.yaml](week%204/ansible/oefening6_ios_facts.yaml) |
| 7 | Ansible: show-commando's met `ios_command` | [oefening7_ios_command.yaml](week%204/ansible/oefening7_ios_command.yaml) |
| 8 | Ansible: compliance controleren | [oefening8_compliance.yaml](week%204/ansible/oefening8_compliance.yaml) |
| 9 | Ansible: configureren met `ios_config` | [oefening9_ios_config.yaml](week%204/ansible/oefening9_ios_config.yaml) |

Oefening 1 tot 5 draaien op Windows; de playbooks hebben een Linux-controlenode nodig.
De [briefing van week 4](week%204/README.md) beschrijft de volledige voorbereiding.

---

## Structuur

```
infracloud2627/
├── README.md                          # dit overzicht
├── Week 2 - python experiments/
│   ├── Sep30-2026.md                  # briefing van de week
│   └── python_experiments.ipynb
├── week 3 - sysinfo/
│   ├── README.md                      # briefing van de week
│   ├── oefening1.py … oefening7.py
│   └── week_3.ipynb                   # dezelfde oefeningen als notebook
└── week 4/
    ├── README.md                      # briefing van de week
    ├── devices.py                     # verbindingsparameters voor alle scripts
    ├── oefening1.py … oefening5.py    # Netmiko
    └── ansible/
        ├── ansible.cfg
        ├── hosts                      # inventaris van de toestellen
        └── oefening6 … oefening9 (.yaml)
```

Daarnaast staan er in de root nog enkele losse bestanden uit week 2:
`netmiko_connect_ios.ipynb`, `time.py` en `geopy_location.html`.

---

## Afspraken

- Eén map per lesweek, met het weeknummer in de mapnaam.
- De briefing van een week staat in de `README.md` van die map, of in het
  lesdocument met de datum als bestandsnaam.
- Eén bestand per opdracht: `oefening<nummer>.py`, genummerd zoals in de briefing.
- Datasets en exportbestanden worden door de scripts gegenereerd en horen niet
  thuis in de repository; mappen zoals `output/` en `backups/` maken de scripts
  zelf aan.
- Wachtwoorden horen niet in de repository. De scripts van week 4 lezen hun
  verbindingsgegevens bij voorkeur uit omgevingsvariabelen.
