# Projects en packages: uitleg in het Nederlands

[← Profiel](README.md) · [Alle projecten](PROJECTS.md)

Naast de broncode staan er op dit profiel twee openbare **Projects** en drie openbare **packages**. Een repository toont de code. Een Project toont hoe het werk gepland en afgerond wordt. Een package is een versie van de software die je zelf kunt installeren of draaien.

## Probeer het samen: Shipment Desk

De drie packages werken samen in één **Shipment Desk**. Je maakt een synthetische zending aan, registreert aankomstbewijs en een hold, uploadt een PDF, geeft de hold vrij en bekijkt de KPI's. Dat loopt via de echte API en SQL Server; de gegevens zijn voorbeelden.

- **API:** gegevens zijn per klant afgeschermd, ook in de cache en bij herhaalde requests. Documenten en events van andere klanten blijven onzichtbaar. Een open hold blokkeert vertrek en levering.
- **NuGet:** alle publieke velden en typen zijn beschreven, enumwaarden liggen vast, een ouder JSON-voorbeeld blijft compatibel en een losse .NET 8-consumer gebruikt de package.
- **npm:** afgeronde, verwachte, achterstallige en ongeplande aankomsten op een expliciet tijdstip; de TypeScript-typen zijn gecontroleerd vanuit de installeerbare package.
- **Dashboard:** bronvensters, filtering, fout en herstel, documentupload en -download en een mobiele weergave. Uitloggen of van account wisselen wist eerdere gegevens.

[Volledige demonstratie en starten](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/DEMO.md) · [Bekijk de opname](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/assets/shipment-desk-walkthrough.mp4) · [Bewijs en beperkingen](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/VERIFICATION.md)

Zelf starten vanuit een clone, met Docker Desktop en Python 3: `python3 scripts/start-demo.py`. Het script maakt een lokale `.env` met eigen demo-wachtwoorden. Open daarna `localhost:5001` en log in als `demo-dispatcher`; het wachtwoord staat alleen in die lokale `.env`.

## De twee Projects

| Project | Inhoud | Items |
| --- | --- | --- |
| [Logistics Operations Roadmap](https://github.com/users/phlppgdfry/projects/6) | PortOps AI, Shipment Tracking, PortFlow en de KPI-library | 16 repository-issues |
| [Data Platform Delivery](https://github.com/users/phlppgdfry/projects/7) | Harbor Pulse, Belgische mobiliteits- en weerdata en sensordata | 9 repository-issues |

Elk bord heeft een beschrijving, een project-README, gekoppelde repositories, een statusbord, een tabel en een roadmapweergave. Elk issue heeft acceptatiecriteria, een workstream, een prioriteit en een relatieve inspanning. Er staan bewust geen kalenderdatums in: het bord legt geen verzonnen deadlines vast.

### Hoe lees je een bord?

- **Backlog:** een verbetering die nog niet geselecteerd is.
- **Ready:** de volgende stap en de acceptatiecriteria zijn duidelijk.
- **In progress:** er wordt effectief aan gewerkt.
- **Done:** er is controleerbaar bewijs dat het af is.

Gepubliceerde versies en afgeronde verbeteringen hebben gesloten issues met bewijs. De 15 open issues zijn gepland werk en worden niet als uitgevoerd voorgesteld. P1 is de volgende nuttige mijlpaal, P2 een latere verbetering. Inspanning 2/3/5 is relatief en geen aantal dagen.

Elk bord werkt naar drie mijlpalen:

1. **Try independently:** een bezoeker kan de gedocumenteerde demo zelf draaien.
2. **Operational reliability:** grenzen, onvolledige data, compatibiliteit en herstel zijn aantoonbaar behandeld.
3. **Connected demonstration:** de onderdelen ondersteunen één begrijpelijk scenario, met bewijs en opname.

De weergave **Next three tasks** toont wat als volgende gepland staat. Provider-evaluatie, echte terminaladapters, gedeeld klantlidmaatschap en een native ARM-databaseoptie zijn gepland, maar geen onderdeel van de huidige demo.

## De drie packages

Alle drie zijn **0.2.0-previewreleases**. De documentatie maakt onderscheid tussen wat werkt en wat nog toekomstig productiewerk is.

### 1. Shipment Tracking API — Docker

[Package](https://github.com/users/phlppgdfry/packages/container/package/shipment-tracking-api) · [Release](https://github.com/phlppgdfry/shipment-tracking-platform/releases/tag/package-v0.2.0) · [Startinstructies](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/PACKAGE.md)

Image: `ghcr.io/phlppgdfry/shipment-tracking-api:0.2.0`.

Hiermee draai je de .NET 10 API zonder ze zelf te compileren. De Compose-demo start SQL Server, maakt optioneel een synthetische dispatcher en voorbeeldzending aan en bewaart database- en documentdata in volumes. De API draait zonder rootrechten en is in de demo alleen bereikbaar op localhost.

Volg de startinstructies: kopieer `.env.package.example` naar `.env`, stel eigen demo-wachtwoorden en een JWT-secret in en start `docker compose -f docker-compose.package.yml up -d --wait --wait-timeout 300`. Open daarna `http://localhost:5001/swagger` en log in als `demo-dispatcher` met het ingestelde wachtwoord. Wie zich publiek registreert, krijgt alleen de Customer-rol; een klant kan geen zendingen aanmaken.

Het image is **linux/amd64**. SQL Server vraagt een passende Docker-omgeving; op Apple Silicon is emulatie nodig. Het is een lokale portfolio-demo, geen draaiende productiedienst.

### 2. PortOps.Contracts — NuGet

[Package](https://github.com/users/phlppgdfry/packages/nuget/package/PortOps.Contracts) · [Release en download](https://github.com/phlppgdfry/portops-ai/releases/tag/contracts-v0.2.0) · [Documentatie](https://github.com/phlppgdfry/portops-ai/blob/main/src/PortOps.Contracts/README.md)

Een library zonder externe dependencies, voor **.NET 8 en hoger**. Ze bevat gedeelde records voor bewijs, bookings, voertuigen, scheepsaanlopen, holds en gereedheidsbeoordelingen. De PortOps-applicatie gebruikt de library zelf; het is geen los pakket dat enkel het profiel opvult.

De C#-namespace blijft `PortOps.Domain` voor compatibiliteit met de bestaande applicatie; package en assembly heten `PortOps.Contracts`. Gereedheidsregels, AI-tools en autorisatie blijven in de applicatie. De DTO's beschrijven data en doen geen inputvalidatie of toegangscontrole.

Installeren via de GitHub NuGet-feed vraagt authenticatie met `read:packages`. Je kunt ook de `.nupkg` uit de release downloaden en vanuit een lokale feed installeren; de README legt beide routes uit.

### 3. Logistics KPI Utils — npm

[Package](https://github.com/users/phlppgdfry/packages/npm/package/logistics-kpi-utils) · [Repository](https://github.com/phlppgdfry/logistics-kpi-utils) · [Release en download](https://github.com/phlppgdfry/logistics-kpi-utils/releases/tag/v0.2.0)

Package: `@phlppgdfry/logistics-kpi-utils@0.2.0`. JavaScript ESM, Node.js 22+, TypeScript-typen en geen externe dependencies.

- `dwellHours`: verstreken uren tussen aankomst en vertrek.
- `delayMinutes`: verschil tussen geplande en werkelijke tijd; negatief betekent te vroeg.
- `onTimeRate`: aandeel op tijd binnen afgeronde, beoordeelbare aankomsten, met optionele tolerantie.
- `summarizeArrivalStatus`: afgeronde, verwachte, achterstallige en ongeplande aankomsten op een expliciet scenariotijdstip.
- `summarizeDwell`: gemiddelde, mediaan, p95, minimum en maximum voor afgeronde bezoeken.

De definities maken ontbrekende data zichtbaar. Een schip dat nog niet aangekomen is, telt niet automatisch als op tijd of te laat. Duplicaten en ongeldige tijdstempels geven een fout. Zonder geldige waarnemingen is het resultaat `null`, geen misleidende nul. Tijdstempels moeten een tijdzone hebben.

De package staat in GitHub Packages, niet op npmjs.org. De GitHub npm-feed vraagt authenticatie; de release bevat ook een `.tgz` die je zonder registry-login lokaal installeert.

## Wat is gecontroleerd?

| Onderdeel | Resultaat |
| --- | --- |
| PortOps-applicatie en contract-serialisatie | 132 tests geslaagd |
| Shipment Tracking | 31 unit-tests en 15 integratietests geslaagd op GitHub |
| Docker-demo met echte SQL Server | Gezondheid, echte JWT-klantgrenzen, seed, volledige statuscyclus, holds, documenten en herhaalde requests gecontroleerd |
| KPI-library | 23 tests geslaagd, inclusief tijdzones, ontbrekende waarden, dubbele ID's en percentielen |
| Gepubliceerde npm-artifact | Gedownload, geïnstalleerd en geïmporteerd in een aparte testapp |
| Gepubliceerde NuGet-artifact | Gedownload, geïnstalleerd en gebruikt voor een JSON round-trip in een aparte testapp |
| Dashboardmapping | 6 tests voor enveloppes, klok, holds, toekomstwaarden en conflicterende plannen |
| Browser | Desktop en mobiel, bronvenster, echte API-flow, fout en herstel, download, accountwissel en uitloggen gecontroleerd |
| GitHub-zichtbaarheid | Beide Projects en alle drie packages zijn openbaar |

Samen zijn dat 207 formele tests plus aanvullende browser-, consumer- en API-controles. Ze bewijzen de beschreven scenario's; ze maken het geheel geen gecertificeerd productieplatform. De analytische klok verandert berekeningen, geen reeds vastgelegde commando's. KPI's gaan over maximaal 100 geladen zendingen, en de zoekfunctie in de tabel verandert de KPI-noemer niet. Ontbrekende of conflicterende gegevens worden expliciet getoond.
