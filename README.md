# THE LORD

**THE LORD** ist die geplante zentrale Plattform für KI, persönliche KI-Assistenten, kreative Welten, Game-Development und Cloud-Gaming.

## Produktvision

Eine Dream-inspirierte Kreativ- und Gaming-Plattform mit einer eigenen Orchestrierungs-Engine, in die die vorhandenen GAUSS-KI-Projekte als getrennte, auswählbare Assistenten und Dienste eingebunden werden.

### Geplante Hauptbereiche

- **THE LORD AI Engine:** zentraler Chat, Modell-Routing, KI-Agenten, Tool-Aufrufe und Verbindungen zu den bestehenden GAUSS-KIs.
- **THE LORD Worlds:** KI-gestützte Erstellung von Charakteren, Geschichten, Umgebungen und interaktiven Welten.
- **THE LORD Game Studio:** Spielprojekte, Engine-Adapter, Assets, Mods, DLCs und Build-Pipelines.
- **THE LORD Cloud Gaming:** Nutzerprofile, Spielebibliothek, Sitzungssteuerung und Anbindung externer GPU-/Streaming-Infrastruktur.
- **THE LORD Accounts:** Registrierung, Profile, Rollen, Berechtigungen und gespeicherte Projekte.
- **THE LORD Premium:** Abonnements, Nutzungskontingente, Abrechnung und Rechnungen.
- **THE LORD Admin:** zentrale Verwaltung, Monitoring, Audit-Protokolle und Dienstübersicht.

## Architekturprinzipien

1. Bestehende Projekte bleiben eigenständige Repositories und werden über dokumentierte APIs/Adapter integriert.
2. API-Schlüssel und Zahlungsgeheimnisse werden ausschließlich als geschützte Umgebungsvariablen verwaltet.
3. Nutzerkonten, Projekte, Spielstände und Abonnements benötigen persistente Datenhaltung.
4. Cloud-Gaming benötigt einen separaten GPU-Host und eine latenzarme Streaming-Lösung; ein normaler Render-Webservice ist dafür nur Steuerungs- und API-Ebene.
5. Premium-Zahlungen werden erst nach Einrichtung eines echten Zahlungsanbieters samt signaturgeprüften Webhooks aktiviert.
6. KI-Ausgaben und generierte Builds werden kontrolliert, protokolliert und vor Deployment getestet.

## Portfolio-Katalog

Die vollständige Bestandsaufnahme der verbundenen GitHub-Repositories und Render-Dienste steht in [docs/PORTFOLIO_CATALOG.md](docs/PORTFOLIO_CATALOG.md).

**Hinweis zum Status:** Der Katalog beschreibt den aus Repository-Dateien, README-Inhalten und Render-Konfigurationen erkennbaren Zweck. Eine vorhandene Render-URL bedeutet nicht automatisch, dass alle Funktionen produktionsreif sind. Im Katalog werden Prototypen, Legacy-Projekte, Platzhalter und doppelte Deployments ausdrücklich gekennzeichnet.


## Implemented agent network foundation

The repository now includes a Flask API, agent dashboard, configurable HTTPS provider adapters, task history, admin-protected update proposals, a website widget, Render Blueprint, scheduled CI quality/dependency audits and Dependabot update proposals.

See [docs/AGENT_NETWORK.md](docs/AGENT_NETWORK.md) for deployment and integration instructions. The adapters are intentionally shown as disconnected until real endpoint URLs and credentials are configured. Existing websites are not silently modified; the widget must be embedded after the central service is deployed and must respect the project exclusions.
