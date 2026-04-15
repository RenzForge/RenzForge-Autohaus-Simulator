
# RenzForge Autohaus Manager

Ein kleines `tkinter`-Projekt, das sich inzwischen eher wie ein Autohaus-Spiel anfühlt als wie ein reines Verwaltungs-Tool.

## Was gerade drin ist

- Markt mit einkaufbaren Fahrzeug-Angeboten
- Angebote können gekauft, abgelehnt oder per Tag neu eingepreist werden
- automatischer Tageswechsel per Timer alle 3 bis 4 Minuten
- normale und Premium-Fahrzeuge
- automatische Fahrten für alle Fahrzeuge im Bestand
- Verschleiss, Dreck, Wertverlust und Unfallrisiko
- Kasse, Verkaufsziel und Tagesdruck
- mehrere Kundenangebote gleichzeitig
- echte Gegenangebote als Zahl
- Fahrzeuge waschen, warten, reparieren, auffüllen und verkaufen
- Fahrzeuge direkt im GUI bearbeiten
- Statistiken und Log-Ausgabe

## Spiel-Loop

1. Neues Spiel starten
2. Im Tab `Einkaufen` gute Angebote suchen
3. Fahrzeuge einkaufen oder unsichere Deals ablehnen
4. Unter Zeitdruck den nächsten Tageswechsel im Blick behalten
5. Autos fahren automatisch, sammeln Kilometer, werden schmutzig und verlieren Wert
6. Für gute Autos mehrere Kundenangebote einsammeln
7. Mit eigenen Gegenangeboten verhandeln
8. Pflegen, reparieren, verkaufen und die Kasse Richtung Ziel treiben

## Wichtige Werte pro Auto

- `Kilometer`
- `Zustand`
- `Sauberkeit`
- `Schaden`
- `Energie`
- `Verkaufswert`

## Wichtige Aktionen

- `Neues Spiel`
- `Ausgewähltes Angebot kaufen`
- `Angebot ablehnen`
- `Markt auffrischen`
- `Angebot holen`
- `Gegenangebot senden`
- `Annehmen`
- `Ablehnen`
- `Alle tanken`
- `Alle laden`
- `Verkaufen`
- `Waschen`
- `Warten`
- `Reparieren`

## Starten

Voraussetzungen:

- Python 3.10 oder neuer
- `tkinter`
- `Pillow`

Installation:

```bash
pip install pillow
```

Start:

```bash
python main.py
```

## Projektstruktur

- `main.py`: Startpunkt der App
- `gui.py`: Tkinter-Oberfläche
- `models.py`: Fahrzeuglogik, Spielwerte und Tages-Simulation
- `config.py`: Spielwerte und Timer-Konfiguration
- `data.py`: Marken, Farben, Besitzer und Standorte
- `branding.py`: Logo-Rendering
- `assets/logo.svg`: Logo-Datei

## Wichtige Config-Werte

In `config.py` kannst du die wichtigsten Spielwerte direkt anpassen:

- `START_KAPITAL`
- `KAPITAL_ZIEL`
- `PREMIUM_RATE`
- `ELEKTRO_RATE`
- `STROM_MIN_PREIS`
- `STROM_MAX_PREIS`
- `BENZIN_MIN_PREIS`
- `BENZIN_MAX_PREIS`
- `DAY_TIMER_MIN_SEC`
- `DAY_TIMER_MAX_SEC`

Die Preise für Strom und Benzin werden jetzt bei jedem Zugriff zufällig innerhalb der eingestellten Spanne gewürfelt.

## Nächste sinnvolle Ausbaustufen

- Autos direkt über Auktionen oder Händler einkaufen
- Ruf- oder Prestige-System
- Werkstatt-Upgrades
- Speichern und Laden per JSON oder SQLite
- Events wie Sammler, Auktionen oder spontane Schäden

<img width="1919" height="1006" alt="StatistikTab" src="https://github.com/user-attachments/assets/b7088606-2590-4cb0-b7e2-97bf8a1dd9f0" />
<img width="1655" height="972" alt="PremiumAutosTab" src="https://github.com/user-attachments/assets/cbed85cc-c322-4208-ba43-ca2879c4df57" />
<img width="1654" height="976" alt="NormaleAutosTab" src="https://github.com/user-attachments/assets/c883f6da-53e3-417b-b428-a799f8efdbf5" />
<img width="1652" height="974" alt="KundenangeboteTab" src="https://github.com/user-attachments/assets/b4e456e1-aaac-4881-8ef8-47c4c2cb4d91" />
<img width="1655" height="975" alt="FahrzeugBearbeitenTab" src="https://github.com/user-attachments/assets/16c7d326-35ce-4198-be49-983c4321076b" />
<img width="1668" height="974" alt="EinkaufTab" src="https://github.com/user-attachments/assets/e4bf9c50-3015-43c5-aaa8-e5fb97295f52" />
<img width="1658" height="979" alt="AlleAutosTab" src="https://github.com/user-attachments/assets/d6f60c19-be8b-49f0-8e2a-cb14b8fcacbe" />
