# RenzForge Autohaus Manager

Ein kleines `tkinter`-Projekt, das sich inzwischen eher wie ein Autohaus-Spiel anfühlt als wie ein reines Verwaltungs-Tool.

## Was gerade drin ist

- Markt mit einkaufbaren Fahrzeug-Angeboten
- Angebote können gekauft oder ausgeschlagen werden
- normales und Premium-Autohaus
- Tag für Tag Simulation
- automatische Fahrten für alle Fahrzeuge im Bestand
- Verschleiß, Dreck, Wertverlust und Unfallrisiko
- Kasse, Verkaufsziel und Verkäufe
- Kundenangebote und erste Preisverhandlungen
- einzelne Fahrzeuge waschen, warten, reparieren oder verkaufen
- Fahrzeuge direkt im GUI bearbeiten
- Statistiken und Log-Ausgabe

## Spiel-Loop

Die Idee ist simpel:

1. Neues Spiel starten
2. Im Tab `Einkaufen` gute Angebote suchen
3. Fahrzeuge einkaufen oder unsichere Deals ablehnen
4. `Nächster Tag` drücken
5. Autos fahren automatisch, sammeln Kilometer, werden schmutzig und verlieren Wert
6. Für gute Autos Kundenangebote holen und nachverhandeln
7. Schlechte Autos erst pflegen oder reparieren
8. Kasse Richtung Ziel treiben

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
- `Nachverhandeln`
- `Annehmen`
- `Ablehnen`
- `Nächster Tag`
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
- `data.py`: Marken, Farben, Besitzer und Standorte
- `branding.py`: Logo-Rendering
- `assets/logo.svg`: Logo-Datei

## Nächste sinnvolle Ausbaustufen

- Fahrzeuge gezielt einkaufen statt nur Markt-Refresh
- JSON-Speichern und Laden
- Werkstatt-Upgrades
- Events wie Sammler, Auktionen oder spontane Schäden
- mehrere Kunden gleichzeitig statt nur ein laufender Deal
