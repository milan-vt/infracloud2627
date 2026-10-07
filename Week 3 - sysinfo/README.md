# Week 3 — System Information Scripting (vervolg)

## Doelstellingen

- Python-scripts voor systeeminformatie manipuleren.
- Informatie uit een geneste Python dictionary selecteren.
- Python dictionaries en JSON van en naar elkaar converteren.
- Ruwe systeeminformatie filteren en transformeren.
- Gegevens exporteren naar verschillende gestructureerde bestandsformaten.
- Gegevens van verschillende computers samenvoegen tot één dataset.

---

## 1 — Basisscript uitvoeren

[oefening1.py](oefening1.py)

- Voer het script `collect_sysinfo.py` uit.
- Bekijk aandachtig de structuur van de dictionary `info`.
- Identificeer welke keys en geneste keys relevante informatie bevatten, bijvoorbeeld CPU,
  RAM-geheugen, opslag, netwerkinterfaces, computernaam en model.

## 2 — Informatie filteren

[oefening2.py](oefening2.py)

Schrijf een script dat uit de verzamelde systeeminformatie de volgende gegevens selecteert en in een
nieuwe Python dictionary opslaat:

- computernaam
- computermodel
- processor
- aantal fysieke CPU-cores
- maximale CPU-frequentie
- totale hoeveelheid RAM-geheugen
- bestandssysteem van de opslag
- opslagcapaciteit
- MAC-adres van de primaire netwerkinterface
- IPv4-adres van de primaire netwerkinterface
- IPv6-adres van de primaire netwerkinterface
- IPv6 link-local-adres van de primaire netwerkinterface

**Opslag** — Een computer kan meerdere disks, partities en bestandssystemen hebben. Bepaal welke
opslaginformatie relevant is voor je dataset en motiveer je keuze.

**Primaire netwerkinterface** — Een computer kan meerdere netwerkinterfaces hebben. Bepaal zelf criteria
waarmee je script de primaire netwerkinterface kan identificeren. Beschrijf en motiveer deze criteria
voordat je ze in je script implementeert.

**Eenheden** — Gebruik voor numerieke waarden duidelijke en consistente eenheden. Zorg ervoor dat dezelfde
eenheden worden gebruikt voor de computers van alle groepsleden.

Sommige gevraagde gegevens zijn mogelijk niet rechtstreeks aanwezig in de verzamelde informatie. Onderzoek
in dat geval hoe je het basisscript kunt uitbreiden om deze informatie op een betrouwbare manier te
verzamelen. Controleer of je criteria ook bruikbaar zijn op de computers van andere groepsleden.

## 3 — JSON

[oefening3.py](oefening3.py)

- Zet je gefilterde dictionary om naar JSON.
- Bewaar de gegevens in een `.json`-bestand.
- Lees het bestand opnieuw in als een Python dictionary.
- Controleer na het opnieuw inlezen of de belangrijkste gegevens overeenkomen met de oorspronkelijke dictionary.
- Leg in enkele zinnen concreet uit wat het verschil is tussen een Python dict en JSON.

## 4 — Transformeren van informatie naar CSV

[oefening4.py](oefening4.py)

De gefilterde informatie bevindt zich momenteel in een Python dict. Transformeer deze gegevens naar een
CSV-bestand dat in een spreadsheetprogramma kan worden geopend.

- Bepaal een geschikte bestandsnaam.
- Bepaal welke informatie je in de kolommen wilt opnemen en kies duidelijke kolomnamen.
- Bepaal hoe de informatie over één computer als één rij in het CSV-bestand kan worden voorgesteld.
- Transformeer de informatie uit de Python dictionary naar een tabelstructuur die geschikt is voor CSV.
- Schrijf de gegevens met Python naar een `.csv`-bestand.
- Open het CSV-bestand in een spreadsheetprogramma en controleer of de gegevens correct worden weergegeven.
- Zorg ervoor dat je script het CSV-bestand later opnieuw kan inlezen.

Denk hierbij na over:

- Welk scheidingsteken gebruik je in het CSV-bestand?
- Hoe ga je om met ontbrekende informatie?
- Hoe ga je om met informatie waarvan een computer meerdere exemplaren kan hebben, zoals disks of netwerkinterfaces?
- Hoe zorg je ervoor dat het CSV-bestand correct kan worden geopend in je spreadsheetprogramma?

## 5 — Transformeren naar een spreadsheetbestand

[oefening5.py](oefening5.py)

Zet de gegevens uit taak 4 met Python om naar een spreadsheetbestand.

- Kies een geschikt spreadsheetformaat.
- Zoek uit welke Python-module of library je hiervoor kunt gebruiken.
- Gebruik dezelfde gegevens en kolomnamen als in het CSV-bestand.
- Bewaar het resultaat in een spreadsheetbestand.
- Open het bestand in een spreadsheetprogramma en controleer het resultaat.
- Vergelijk deze werkwijze met het gebruik van CSV.

Denk hierbij na over:

- Wat is het verschil tussen een CSV-bestand en een echt spreadsheetbestand?
- Welke extra mogelijkheden biedt een spreadsheetformaat?
- Wanneer zou je CSV verkiezen en wanneer een spreadsheetbestand?

## 6 — Informatie van verschillende computers samenvoegen

[oefening6.py](oefening6.py)

Ieder groepslid heeft nu een gestructureerd bestand met de informatie over zijn of haar eigen computer.
Maak met Python één databestand waarin de informatie van de computers van alle groepsleden wordt samengevoegd.

- Bepaal samen welke kolommen in het gemeenschappelijke CSV-bestand worden gebruikt.
- Zorg ervoor dat alle groepsleden hun gegevens volgens dezelfde structuur opslaan.
- Lees met Python de afzonderlijke CSV-bestanden van de groepsleden in.
- Voeg de gegevens automatisch samen tot één dataset.
- Schrijf het resultaat naar een nieuw CSV-bestand.
- **Het is niet toegestaan om de gegevens manueel te kopiëren.**
- Open het uiteindelijke CSV-bestand in een spreadsheetprogramma en controleer het resultaat.

Denk hierbij na over:

- Hoe zorg je ervoor dat de kolomnamen bij iedereen hetzelfde zijn?
- Wat gebeurt er wanneer gegevens bij een groepslid ontbreken?
- Hoe kan je script bepalen welke CSV-bestanden moeten worden ingelezen?
- Hoe zorg je ervoor dat nieuwe computers later eenvoudig aan de dataset kunnen worden toegevoegd?

Spreek binnen het team af hoe en waar de afzonderlijke bestanden worden uitgewisseld en hoe de bestanden
worden benoemd.

## 7 — Valideren

[oefening7.py](oefening7.py)

Controleer of de gegevens in het uiteindelijke CSV- of spreadsheetbestand overeenkomen met de werkelijke
configuratie van de computers. Controleer minstens:

- computernaam
- hoeveelheid RAM
- processor
- IP-adres
- MAC-adres
- opslagcapaciteit

Noteer eventuele verschillen en probeer deze te verklaren.
Welke controles zou je met Python automatisch kunnen uitvoeren in plaats van manueel?
