# Week 4 — Netwerkautomatisatie met Netmiko en Ansible

Negen oefeningen rond het automatiseren van Cisco IOS-toestellen: vijf met
Netmiko (Python) en vier met Ansible. Telkens draait het om dezelfde taken
die een netwerkbeheerder anders manueel via de CLI doet — informatie
opvragen, documenteren en configureren — maar dan in een script.

---

## Overzicht

### Netmiko (Python)

| # | Opdracht | Bestand |
|---|----------|---------|
| 1 | Basisverbinding opzetten en `show ssh` uitvoeren | [oefening1.py](oefening1.py) |
| 2 | Hetzelfde script, maar met variabelen | [oefening2.py](oefening2.py) |
| 3 | Informatie verzamelen van een Cisco-toestel | [oefening3.py](oefening3.py) |
| 4 | Uitvoer bewaren als tekst, JSON en spreadsheet | [oefening4.py](oefening4.py) |
| 5 | Toestellen configureren en de wijziging verifiëren | [oefening5.py](oefening5.py) |

### Ansible

| # | Opdracht | Bestand |
|---|----------|---------|
| 6 | Gegevens verzamelen met `ios_facts` | [oefening6_ios_facts.yaml](ansible/oefening6_ios_facts.yaml) |
| 7 | Show-commando's en configvergelijking met `ios_command` | [oefening7_ios_command.yaml](ansible/oefening7_ios_command.yaml) |
| 8 | Compliance controleren | [oefening8_compliance.yaml](ansible/oefening8_compliance.yaml) |
| 9 | Configureren met `ios_config` | [oefening9_ios_config.yaml](ansible/oefening9_ios_config.yaml) |

---

## Structuur

```
week 4/
├── README.md               # deze briefing
├── .gitignore              # houdt gegenereerde bestanden uit de repository
├── devices.py              # verbindingsparameters, één bron voor alle scripts
├── oefening1.py … oefening5.py
└── ansible/
    ├── ansible.cfg         # Ansible-instellingen
    ├── hosts               # inventaris: welke toestellen beheren we
    └── oefening6_ios_facts.yaml … oefening9_ios_config.yaml
```

De scripts en playbooks maken zelf de mappen aan waarin ze wegschrijven:
`output/` voor de exports van oefening 4, `ansible/backups/` voor de facts uit
oefening 6 en `ansible/baselines/` voor de referentieconfiguratie van
oefening 7. Die staan in `.gitignore` en horen niet in de repository.

---

## Voorbereiding

### 1. Toestel bereikbaar maken

De oefeningen draaien tegen een Cisco IOS XE-toestel in de DevNet-sandbox
(CML). Zet eerst de **AnyConnect VPN** op met de gegevens uit het
sandbox-reservatiemailtje, en test daarna manueel:

```powershell
ping 10.110.177.102
ssh cisco@10.110.177.102
```

> Werkt SSH niet manueel, dan werkt Netmiko ook niet. Los dat eerst op.

Het toestel moet beschikken over een IP-adres op een bereikbare interface,
SSH versie 2, een lokale gebruiker en vty-lijnen met `transport input ssh`:

```
hostname R1
ip domain-name biasc.lab.local
username cisco secret cisco123!
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 15
 login local
 transport input ssh
```

### 2. Python-omgeving

```powershell
pip install netmiko ntc-templates openpyxl
```

- `netmiko` — SSH-verbindingen naar netwerktoestellen
- `ntc-templates` — TextFSM-sjablonen, nodig voor `use_textfsm=True` in oefening 3
- `openpyxl` — enkel voor de spreadsheet-export in oefening 4

### 3. Verbindingsparameters zetten

De scripts lezen hun parameters uit [devices.py](devices.py). Pas daar het
IP-adres aan, of zet omgevingsvariabelen (dan blijven de wachtwoorden uit
de repository):

```powershell
$env:IOS_HOST = "10.110.177.102"; $env:IOS_USERNAME = "cisco"; $env:IOS_PASSWORD = "Cisco123!"; $env:IOS_SECRET = "Cisco123!"
```

### 4. Ansible

Ansible draait **niet** als controlenode op Windows. `ansible-playbook`
bestaat daar niet, vandaar de foutmelding "term is not recognized" in
PowerShell. Je hebt dus een Linux-omgeving nodig: WSL (Ubuntu).

**Eenmalig: WSL werkend krijgen.** Open PowerShell *als administrator* en
zet de vereiste Windows-component aan, en herstart daarna de computer:

```powershell
wsl.exe --install --no-distribution
```

**Eenmalig: Ansible installeren.** Start Ubuntu (`wsl -d Ubuntu`) en voer
daarin uit:

```bash
sudo apt update && sudo apt install -y python3-pip
pip3 install --user ansible
ansible-galaxy collection install cisco.ios ansible.netcommon ansible.utils
```

**Je projectmap vanuit WSL.** De Windows-schijf hangt onder `/mnt/c`:

```bash
cd "/mnt/c/Users/<jouw-naam>/Documents/hogeschool/odisee/InfrastructureCloud/infracloud2627/week 4/ansible"
```

**Valkuil: ansible.cfg wordt genegeerd.** Ansible weigert een
`ansible.cfg` te lezen die in een voor iedereen schrijfbare map staat, en
dat is `/mnt/c` standaard. Je krijgt dan een waarschuwing en de
instellingen worden stilzwijgend overgeslagen. Wijs het configuratiebestand
daarom expliciet aan — dat omzeilt de controle:

```bash
export ANSIBLE_CONFIG="$(pwd)/ansible.cfg"
```

Zet die regel in `~/.bashrc` als je het niet elke sessie wil herhalen, of
kopieer de map naar je Linux-home (`cp -r . ~/ansible-week4`) en werk daar.

---

## De oefeningen uitvoeren

### Netmiko

```powershell
python oefening1.py
```

```powershell
python oefening2.py
```

```powershell
python oefening3.py
```

Uitvoer rechtstreeks naar een bestand schrijven, via omleiding in de shell:

```powershell
python oefening3.py > output/router_inventory.txt
```

Alles tegelijk bewaren als tekst, JSON en spreadsheet:

```powershell
python oefening4.py
```

Configuratie aanpassen (vraagt eerst bevestiging):

```powershell
python oefening5.py
```

Enkel controleren, zonder iets te wijzigen:

```powershell
python oefening5.py --controle
```

### Ansible (vanuit WSL, in de map `ansible/`)

Controleer eerst of een playbook klopt zonder iets naar een toestel te
sturen — dit heeft geen VPN of router nodig:

```bash
ansible-playbook oefening6_ios_facts.yaml --syntax-check
```

Daarna de playbooks zelf:

```bash
ansible-playbook -i hosts oefening6_ios_facts.yaml
```

```bash
ansible-playbook -i hosts oefening7_ios_command.yaml
```

```bash
ansible-playbook -i hosts oefening8_compliance.yaml
```

Eerst een dry run voor de configuratie-oefening:

```bash
ansible-playbook -i hosts oefening9_ios_config.yaml --check --diff
```

```bash
ansible-playbook -i hosts oefening9_ios_config.yaml
```

Achteraf de aangemaakte loopback weer verwijderen:

```bash
ansible-playbook -i hosts oefening9_ios_config.yaml --tags opruimen
```

---

## Aandachtspunten

**Drie manieren om tekst te parsen.** Oefening 3 toont ze alle drie naast
elkaar om de hostname uit `show version` te halen:

| Methode | Code | Opmerking |
|---------|------|-----------|
| regex | `re.search(r"(\S+) uptime is", output)` | krachtig en flexibel, maar minder leesbaar |
| split | `line.split()[0]` op de regel met `uptime is` | eenvoudigst om te begrijpen |
| TextFSM | `send_command("show version", use_textfsm=True)` | geeft meteen een dictionary terug |

**Netmiko versus Ansible.** Beide gebruiken SSH, maar verschillen in aanpak:

| | Netmiko | Ansible |
|---|---------|---------|
| Vorm | Python-script | YAML-playbook |
| Aanpak | procedureel: je beschrijft de stappen | declaratief: je beschrijft het gewenste resultaat |
| Idempotent | nee, het script voert altijd alles uit | ja, enkel wat nog niet klopt wordt aangepast |
| Schaal | lus over een lijst toestellen | inventaris met groepen |

**Wachtwoorden.** De labowachtwoorden staan nu als fallback in `devices.py`
en in `ansible/hosts`. Voor echt werk gebruik je omgevingsvariabelen of
`ansible-vault`.

**Configuratie wijzigen.** Oefening 5 en 9 passen het toestel effectief aan.
Oefening 5 vraagt bevestiging, oefening 9 kan je eerst met `--check` testen.
