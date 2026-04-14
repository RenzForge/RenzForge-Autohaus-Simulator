# RenzForge Autohaus Manager

Ein kleines Python-Spielprojekt mit `tkinter`, in dem du dir einen Fahrzeugbestand zusammenklicken, ansehen und bearbeiten kannst.  
Die App hat sich mit der Zeit von einer einfachen Auto-Liste zu einem kleinen Autohaus-Dashboard entwickelt.

## Was die App kann

- zufällige Fahrzeuge generieren
- normale und Premium-Fahrzeuge trennen
- Benziner tanken und Elektroautos laden
- einzelne Fahrzeuge direkt im GUI bearbeiten
- Statistiken zum Bestand anzeigen
- ein eigenes Logo im Header anzeigen

## GUI-Aufbau

Die Oberfläche ist in mehrere Bereiche aufgeteilt:

- `Alle Autos`
- `Normale Ecke`
- `Premium Ecke`
- `Bearbeiten`
- `Statistiken`

Rechts gibt es außerdem einen kleinen Schnellbereich für das aktuell ausgewählte Fahrzeug.

## Voraussetzungen

- Python 3.10 oder neuer
- `tkinter`  
  Ist bei den meisten Windows-Python-Installationen schon dabei.
- `Pillow`

Installation:

```bash
pip install pillow
```

## Starten

```bash
python main.py
```

## Bearbeiten von Fahrzeugen

1. In einer Tabelle ein Auto anklicken.
2. Rechts auf `Groß bearbeiten` klicken.
3. Im Tab `Bearbeiten` Werte ändern.
4. Auf `Speichern` drücken.

Wichtig: Die Änderungen werden aktuell nur im laufenden Programm gehalten.  
Wenn du die App schließt, ist der Bestand wieder weg. Es gibt im Moment noch keine Speicherung per JSON oder Datenbank.

## Projektstruktur

- [main.py](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/main.py) startet die App
- [gui.py](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/gui.py) enthält das komplette Tkinter-GUI
- [models.py](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/models.py) enthält `Auto`, `ElektroAuto` und `Garage`
- [data.py](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/data.py) enthält Marken, Farben, Besitzer und Autohaus-Daten
- [branding.py](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/branding.py) rendert das Logo
- [assets/logo.svg](C:/Users/renzl/Documents/Coding%20Resourcen/Challanges%20Python/assets/logo.svg) ist das lokale Logo

## Nächste sinnvolle Ausbaustufen

- JSON-Speichern und Laden
- Fahrzeuge manuell neu anlegen oder löschen
- Suche und Filter
- Sortierung nach Preis, PS oder Baujahr
- Status wie `reserviert` oder `verkauft`

## Kleiner Hinweis

Der Code ist bewusst eher wie ein Spaßprojekt gehalten und nicht wie ein superstrenges Produktivsystem.  
Wenn du magst, kann man daraus als Nächstes noch eine sauberere Version mit Persistenz, besserer Struktur und vielleicht sogar einem kleinen Verkaufssystem machen.
