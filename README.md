# RenzForge Autohaus Manager

Ein kleines `tkinter`-Projekt, das sich inzwischen eher wie ein Autohaus-Spiel anfuehlt als wie ein reines Verwaltungs-Tool.

## Was gerade drin ist

- Markt mit einkaufbaren Fahrzeug-Angeboten
- Angebote koennen gekauft, abgelehnt oder per Tag neu eingepreist werden
- automatischer Tageswechsel per Timer alle 3 bis 4 Minuten
- normale und Premium-Fahrzeuge
- automatische Fahrten fuer alle Fahrzeuge im Bestand
- Verschleiss, Dreck, Wertverlust und Unfallrisiko
- Kasse, Verkaufsziel und Tagesdruck
- mehrere Kundenangebote gleichzeitig
- echte Gegenangebote als Zahl
- Fahrzeuge waschen, warten, reparieren, auffuellen und verkaufen
- Fahrzeuge direkt im GUI bearbeiten
- Statistiken und Log-Ausgabe

## Spiel-Loop

1. Neues Spiel starten
2. Im Tab `Einkaufen` gute Angebote suchen
3. Fahrzeuge einkaufen oder unsichere Deals ablehnen
4. Unter Zeitdruck den naechsten Tageswechsel im Blick behalten
5. Autos fahren automatisch, sammeln Kilometer, werden schmutzig und verlieren Wert
6. Fuer gute Autos mehrere Kundenangebote einsammeln
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
- `Ausgewaehltes Angebot kaufen`
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
- `gui.py`: Tkinter-Oberflaeche
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

Die Preise fuer Strom und Benzin werden jetzt bei jedem Zugriff zufaellig innerhalb der eingestellten Spanne gewuerfelt.

## Naechste sinnvolle Ausbaustufen

- Autos direkt ueber Auktionen oder Haendler einkaufen
- Ruf- oder Prestige-System
- Werkstatt-Upgrades
- Speichern und Laden per JSON oder SQLite
- Events wie Sammler, Auktionen oder spontane Schaeden
