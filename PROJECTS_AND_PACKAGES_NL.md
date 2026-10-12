# Je GitHub Projects en Packages

Er zijn twee openbare Projects en drie openbare packages aan je profiel toegevoegd. Een repository laat de broncode zien, een Project laat zien hoe je het werk plant, en een Package is een versie van software die iemand kan installeren of uitvoeren.

## Wat is verbeterd in versie 0.2.0?

De packages werken nu samen in één **Shipment Desk**. Je kunt een synthetische zending maken, aankomstbewijs en een hold registreren, een PDF uploaden, de hold vrijgeven en de KPI’s bekijken. Dit gebruikt de echte API en SQL Server; de gegevens zijn voorbeelden.

- **API:** klantgebonden gegevens, cache en herhaalde requests; documenten/events van andere klanten zijn afgeschermd. Een open hold blokkeert vertrek en levering.
- **NuGet:** beschrijvingen van alle publieke velden/typen, vaste enumwaarden, een oud JSON-voorbeeld dat compatibel blijft en een onafhankelijke .NET 8-consumer.
- **npm:** afgeronde, verwachte, achterstallige en ongeplande aankomsten bij een expliciete tijd; TypeScript-typen gecontroleerd vanuit de installeerbare package.
- **Dashboard:** werkende bronvensters, filtering, fout/herstel, documentupload/download en mobiele weergave. Uitloggen en accountwisseling wissen eerdere gegevens.
- **Projects:** drie resultaatmijlpalen, gekoppelde repository-milestones en per bord een weergave met precies drie geselecteerde volgende taken.

[Volledige demonstratie en starten](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/DEMO.md) · [Bekijk de opname](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/assets/shipment-desk-walkthrough.mp4) · [Bewijs en beperkingen](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/VERIFICATION.md)

Starten vanuit een clone met Docker Desktop en Python 3: `python3 scripts/start-demo.py`. De helper maakt een private `.env` met eigen demo-wachtwoorden. Open daarna localhost:5001 en gebruik `demo-dispatcher`. Het wachtwoord staat alleen in je lokale `.env`; publiceer die niet.

## De twee Projects

| Project | Inhoud | Items |
| --- | --- | --- |
| [Logistics Operations Roadmap](https://github.com/users/phlppgdfry/projects/6) | PortOps AI, Shipment Tracking, PortFlow en KPI-library | 16 repository-issues |
| [Data Platform Delivery](https://github.com/users/phlppgdfry/projects/7) | Harbor Pulse, Belgische mobiliteit/weersdata en sensordata | 9 repository-issues |

Elk bord heeft een beschrijving, een project-README, gekoppelde repositories, een statusbord, een tabel en een roadmapweergave. De issues zijn aan jou toegewezen en hebben acceptatiecriteria, een workstream, prioriteit en relatieve inspanning. Kalenderdatums zijn nog niet ingevuld: het bord legt geen verzonnen deadlines vast.

### Wat betekenen de kolommen?

- **Backlog:** een verbetering die nog niet is geselecteerd.
- **Ready:** de volgende stap en acceptatiecriteria zijn duidelijk.
- **In progress:** je bent daadwerkelijk aan de taak begonnen.
- **Done:** er is controleerbaar bewijs dat de taak is afgerond.

De publicaties en afgeronde verbeteringen hebben gesloten issues met bewijs. Er blijven 15 toekomstige issues over; dat werk wordt niet als uitgevoerd voorgesteld. P1 betekent een volgende nuttige mijlpaal; P2 een latere verbetering. Inspanning 2/3/5 is relatief en betekent geen aantal dagen.

## De drie Packages

### 1. Shipment Tracking API — Docker

[Package](https://github.com/users/phlppgdfry/packages/container/package/shipment-tracking-api) · [Release](https://github.com/phlppgdfry/shipment-tracking-platform/releases/tag/package-v0.2.0) · [Startinstructies](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/PACKAGE.md)

Image: `ghcr.io/phlppgdfry/shipment-tracking-api:0.2.0`.

Hiermee kan iemand je bestaande .NET 10 API draaien zonder deze zelf te compileren. De Compose-demo start SQL Server, maakt optioneel een synthetische dispatcher en voorbeeldzending aan en bewaart database- en documentdata in volumes. De API draait onder een gebruiker zonder rootrechten en is in de demo alleen bereikbaar op localhost.

Volg de startinstructies: kopieer `.env.package.example` naar `.env`, stel eigen demo-wachtwoorden en een JWT-secret in, en start `docker compose -f docker-compose.package.yml up -d --wait --wait-timeout 300`. Open vervolgens `http://localhost:5001/swagger`. Log in als `demo-dispatcher` met het ingestelde wachtwoord. Publieke registratie geeft alleen de Customer-rol; een klant mag geen zendingen aanmaken.

Het image is **linux/amd64**. SQL Server vereist een passende Docker-omgeving; op Apple Silicon is emulatie nodig. Het is een lokale portfolio-demo, geen uitgerolde productiedienst. De toekomstige beoordeling van klantisolatie staat expliciet op het bord.

### 2. PortOps.Contracts — NuGet

[Package](https://github.com/users/phlppgdfry/packages/nuget/package/PortOps.Contracts) · [Release en download](https://github.com/phlppgdfry/portops-ai/releases/tag/contracts-v0.2.0) · [Documentatie](https://github.com/phlppgdfry/portops-ai/blob/main/src/PortOps.Contracts/README.md)

Versie 0.2.0 is een library zonder externe dependencies, geschikt voor **.NET 8 en hoger**. De package bevat gedeelde records voor bewijs, bookings, voertuigen, scheepsaanlopen, holds en gereedheidsbeoordelingen. De PortOps-applicatie gebruikt deze library zelf: het is dus geen los pakket dat alleen het profiel opvult.

De C# namespace blijft `PortOps.Domain` voor compatibiliteit met de bestaande applicatie. De package en assembly heten `PortOps.Contracts`. Gereedheidsregels, AI-tools en autorisatie blijven in de applicatie. DTOs beschrijven data en voeren geen inputvalidatie of toegangscontrole uit.

Installatie via de GitHub NuGet-feed vereist authenticatie met `read:packages`. Je kunt ook de `.nupkg` van de release downloaden en vanuit een lokale feed installeren. De README legt beide routes uit.

### 3. Logistics KPI Utils — npm

[Package](https://github.com/users/phlppgdfry/packages/npm/package/logistics-kpi-utils) · [Repository](https://github.com/phlppgdfry/logistics-kpi-utils) · [Release en download](https://github.com/phlppgdfry/logistics-kpi-utils/releases/tag/v0.2.0)

Package: `@phlppgdfry/logistics-kpi-utils@0.2.0`. JavaScript ESM, Node.js 22+, TypeScript-typen en geen externe dependencies.

- `dwellHours`: verstreken uren tussen aankomst en vertrek.
- `delayMinutes`: verschil tussen geplande en werkelijke tijd; negatief betekent te vroeg.
- `onTimeRate`: aandeel op tijd binnen afgeronde, beoordeelbare aankomsten, met optionele tolerantie.
- `summarizeArrivalStatus`: afgeronde, verwachte, achterstallige en ongeplande aankomsten bij een expliciete scenario-tijd.
- `summarizeDwell`: gemiddelde, mediaan, p95, minimum en maximum voor afgeronde bezoeken.

De definities maken ontbrekende data zichtbaar. Een nog niet aangekomen schip telt niet automatisch als op tijd of te laat. Duplicaten en ongeldige tijdstempels geven fouten. Zonder geldige waarnemingen is het resultaat `null`, niet een misleidende nul. Tijdstempels moeten een tijdzone hebben.

Dit staat in GitHub Packages, niet op npmjs.org. De GitHub npm-feed vereist authenticatie; de release biedt ook een `.tgz` die je lokaal zonder registry-login kunt installeren.

## Wat is gecontroleerd?

| Onderdeel | Resultaat |
| --- | --- |
| PortOps-applicatie en contract-serialisatie | 132 tests geslaagd |
| Shipment Tracking | 31 unit-tests en 15 integratietests geslaagd op GitHub |
| Docker-demo met echte SQL Server | Gezondheid, echte JWT-klantgrenzen, seed, volledige statuscyclus, holds, documenten en requestreplays gecontroleerd |
| KPI-library | 23 tests geslaagd, inclusief tijdzones, ontbrekende waarden, dubbele IDs en percentielen |
| Gepubliceerde npm-artifact | Gedownload, geïnstalleerd en geïmporteerd in een aparte testapp |
| Gepubliceerde NuGet-artifact | Gedownload, geïnstalleerd en gebruikt voor een JSON round-trip in een aparte testapp |
| Dashboardmapping | 6 tests voor enveloppes, klok, holds, toekomstwaarden en conflicterende plannen |
| Browser | Desktop/mobiel, bronvenster, echte API-flow, fout/herstel, download, accountwissel en logout gecontroleerd |
| GitHub-zichtbaarheid | Beide Projects en alle drie packages zijn openbaar |

Dit zijn **0.2.0-previewreleases**. De documentatie maakt onderscheid tussen werkende mogelijkheden en toekomstig productiewerk.

## Hoe houd je dit goed?

1. Kies één Ready-issue en zet deze pas op In progress wanneer je begint.
2. Werk in de gekoppelde repository en verwijs vanuit de wijziging naar het issue.
3. Controleer de acceptatiecriteria, tests en documentatie.
4. Voeg bewijs toe aan het issue, sluit het en zet het op Done.
5. Voeg bij nieuwe mogelijkheden een passend issue toe aan het betreffende Project. Dit wordt niet automatisch voor alle nieuwe repository-issues gedaan.

Voor een nieuwe packageversie pas je de versie en documentatie aan, laat je de tests slagen en publiceer je een GitHub-release. De workflows regelen de upload:

- NuGet: tag `contracts-vX.Y.Z`; versie moet overeenkomen met het projectbestand.
- npm: tag `vX.Y.Z`; versie moet overeenkomen met `package.json`.
- Container: tag `package-vX.Y.Z`; publicatie volgt na tests en de container-smokecheck.

Gebruik versietags voor reproduceerbare installatie; Docker `latest` schuift mee met een volgende package-release. Verander de tag van een al gepubliceerde versie niet om andere software onder hetzelfde versienummer uit te geven.

De eerdere privé-Projects zijn behouden. De nieuwe openbare borden maken je werk zichtbaar zonder die bestaande inhoud openbaar te maken.

## Drie mijlpalen en dagelijks gebruik

1. **Try independently:** een bezoeker kan de gedocumenteerde demo draaien.
2. **Operational reliability:** grenzen, onvolledige data, compatibiliteit en herstel zijn aantoonbaar behandeld.
3. **Connected demonstration:** de onderdelen ondersteunen één begrijpelijk scenario met bewijs en opname.

Gebruik **Next three tasks** om focus te houden. Deze taken zijn nog gepland; Provider-evaluatie, echte terminaladapters, gedeelde klantmembership en een native ARM-databaseoptie zijn geen stilzwijgende onderdelen van de huidige demo.

De 207 formele tests en aanvullende browser/consumer/API-controles bewijzen de beschreven scenario’s. Ze maken het geheel geen gecertificeerd productieplatform. De analytische klok verandert berekeningen, niet reeds vastgelegde commando’s. KPI’s gaan over maximaal 100 geladen zendingen; de tabelzoekfunctie verandert de KPI-noemer niet. Ontbrekende of conflicterende gegevens worden expliciet zichtbaar gemaakt.
