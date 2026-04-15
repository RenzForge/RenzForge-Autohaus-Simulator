import random
from collections import Counter


def _clamp_percent(value):
    return max(0, min(100, int(value)))


class Auto:
    _id_counter = 1000

    def __init__(
        self,
        config,
        marke,
        farbe,
        km=0,
        ps=80,
        maxspeed=160,
        tank=50,
        besitzer="Niemand",
        preis=18_000,
        baujahr=2022,
        standort="Autohaus Schneider",
        premium=False,
        fahrzeug_id=None,
        zustand=100,
        sauberkeit=100,
        schaden=0,
    ):
        self.config = config
        self.fahrzeug_id = (
            Auto._generate_id()
            if fahrzeug_id is None
            else int(fahrzeug_id)
        )
        self.marke = marke
        self.farbe = farbe
        self.km = max(0, int(km))
        self.ps = max(1, int(ps))
        self.maxspeed = max(1, int(maxspeed))
        self.tank = max(0, min(self.config.MAX_TANK, int(tank)))
        self.elektrisch = False
        self._besitzer = besitzer
        self.preis = max(1_000, int(preis))
        self.baujahr = max(1980, int(baujahr))
        self.standort = standort
        self.premium = bool(premium)
        self.zustand = _clamp_percent(zustand)
        self.sauberkeit = _clamp_percent(sauberkeit)
        self.schaden = max(0, min(3, int(schaden)))
        self.letzte_fahrt = "Noch kein Tag gespielt"

    @staticmethod
    def _generate_id():
        value = Auto._id_counter
        Auto._id_counter += 1
        return value

    @property
    def besitzer(self):
        return self._besitzer

    @besitzer.setter
    def besitzer(self, name):
        self._besitzer = name or "Unbekannt"

    @property
    def typ(self):
        return "Elektro" if self.elektrisch else "Benzin"

    @property
    def haus_label(self):
        return "Premium" if self.premium else "Normal"

    @property
    def zustand_label(self):
        return f"{self.zustand}%"

    @property
    def sauberkeit_label(self):
        return f"{self.sauberkeit}%"

    @property
    def schaden_label(self):
        labels = {
            0: "Kein Schaden",
            1: "Leichter Schaden",
            2: "Mittlerer Schaden",
            3: "Schwerer Schaden",
        }
        return labels[self.schaden]

    @property
    def verbrauch_pro_100km(self):
        if self.elektrisch:
            basis = 13.5 + max(0, self.ps - 120) / 32
            return round(min(30.0, basis), 1)
        basis = 5.2 + max(0, self.ps - 75) / 45
        return round(min(15.0, basis), 1)

    @property
    def energie_label(self):
        if self.elektrisch:
            return f"{self.tank}%"
        return f"{self.tank} L"

    @property
    def preis_label(self):
        return f"{self.preis:,.0f} EUR".replace(",", ".")

    @property
    def verkaufswert(self):
        aktuelles_jahr = 2026
        alter = max(0, aktuelles_jahr - self.baujahr)
        alter_faktor = max(0.55, 1 - alter * 0.018)
        km_faktor = max(0.4, 1 - (self.km / 360_000))
        zustand_faktor = 0.35 + (self.zustand / 100) * 0.65
        sauberkeit_faktor = 0.82 + (self.sauberkeit / 100) * 0.18
        schaden_faktor = {
            0: 1.00,
            1: 0.88,
            2: 0.72,
            3: 0.5,
        }[self.schaden]
        wert = round(
            self.preis
            * alter_faktor
            * km_faktor
            * zustand_faktor
            * sauberkeit_faktor
            * schaden_faktor
        )
        return max(1_000, wert)

    @property
    def verkaufswert_label(self):
        return f"{self.verkaufswert:,.0f} EUR".replace(",", ".")

    @property
    def waschkosten(self):
        return self.config.WASH_COST + (30 if self.premium else 0)

    @property
    def wartungskosten(self):
        basis = self.config.SERVICE_COST + (180 if self.premium else 0)
        verschleiss = max(0, 75 - self.zustand) * 6
        return basis + verschleiss

    @property
    def reparaturkosten(self):
        if self.schaden == 3:
            return self.config.REPAIR_COST_HEAVY
        if self.schaden == 2:
            return self.config.REPAIR_COST_MEDIUM
        if self.schaden == 1:
            return self.config.REPAIR_COST_LIGHT
        return max(450, 250 + max(0, 70 - self.zustand) * 8)

    def auffuellen_kosten(self):
        if self.elektrisch:
            return round((self.config.MAX_BATTERIE - self.tank) * self.config.strompreis)
        return round((self.config.MAX_TANK - self.tank) * self.config.benzinpreis)

    def set_energie(self, wert):
        limit = self.config.MAX_BATTERIE if self.elektrisch else self.config.MAX_TANK
        self.tank = max(0, min(limit, int(wert)))

    def tanken(self, menge=None):
        if self.elektrisch:
            return 0
        start = self.tank
        if menge is None:
            self.tank = self.config.MAX_TANK
        else:
            self.tank = min(
                self.config.MAX_TANK,
                self.tank + max(0, int(menge)),
            )
        return self.tank - start

    def laden(self, menge=None):
        if not self.elektrisch:
            return 0
        start = self.tank
        if menge is None:
            self.tank = self.config.MAX_BATTERIE
        else:
            self.tank = min(
                self.config.MAX_BATTERIE,
                self.tank + max(0, int(menge)),
            )
        return self.tank - start

    def fahren(self, km):
        km = max(0, int(km))
        if km == 0:
            return 0
        verbrauch = max(1, round(km * self.verbrauch_pro_100km / 100))
        self.km += km
        self.tank = max(0, self.tank - verbrauch)
        return verbrauch

    def waschen(self):
        vorher = self.sauberkeit
        self.sauberkeit = min(100, self.sauberkeit + random.randint(30, 55))
        return self.sauberkeit - vorher

    def warten(self):
        vorher = self.zustand
        bonus = random.randint(10, 24)
        if self.schaden == 0:
            bonus += 4
        self.zustand = min(100, self.zustand + bonus)
        return self.zustand - vorher

    def reparieren(self):
        vorher = self.zustand
        vorheriger_schaden = self.schaden
        self.zustand = min(100, self.zustand + random.randint(12, 28))
        self.sauberkeit = min(100, self.sauberkeit + random.randint(4, 14))
        if self.schaden > 0:
            self.schaden -= 1
        return {
            "zustand_plus": self.zustand - vorher,
            "schaden_vorher": vorheriger_schaden,
            "schaden_nachher": self.schaden,
        }

    def update_daten(
        self,
        marke,
        farbe,
        km,
        ps,
        maxspeed,
        energie,
        besitzer,
        preis,
        baujahr,
        standort,
        premium,
        elektrisch,
        zustand=None,
        sauberkeit=None,
        schaden=None,
    ):
        self.marke = marke
        self.farbe = farbe
        self.km = max(0, int(km))
        self.ps = max(1, int(ps))
        self.maxspeed = max(1, int(maxspeed))
        self.besitzer = besitzer
        self.preis = max(1_000, int(preis))
        self.baujahr = max(1980, int(baujahr))
        self.standort = standort
        self.premium = bool(premium)
        self.elektrisch = bool(elektrisch)
        self.set_energie(energie)
        if zustand is not None:
            self.zustand = _clamp_percent(zustand)
        if sauberkeit is not None:
            self.sauberkeit = _clamp_percent(sauberkeit)
        if schaden is not None:
            self.schaden = max(0, min(3, int(schaden)))

    def simuliere_tag(self):
        fahrten = [
            ("Showroom-Runde", 0, 12, 0.003),
            ("Probefahrt", 12, 55, 0.012),
            ("Transfer", 22, 95, 0.018),
            ("Kundenfahrt", 35, 160, 0.026),
        ]
        fahrt, minimum, maximum, basis_risiko = random.choices(
            fahrten,
            weights=[16, 45, 24, 15],
            k=1,
        )[0]

        km = random.randint(minimum, maximum)
        if self.premium and fahrt == "Kundenfahrt":
            km = max(minimum, int(km * 0.85))

        wert_vorher = self.verkaufswert
        verbrauch = self.fahren(km)

        sauberkeitsverlust = min(24, 2 + km // 14 + random.randint(0, 5))
        zustandsverlust = min(16, 1 + km // 35 + random.randint(0, 4))

        if self.tank <= 15:
            zustandsverlust += 1

        self.sauberkeit = max(0, self.sauberkeit - sauberkeitsverlust)
        self.zustand = max(0, self.zustand - zustandsverlust)

        unfall = None
        risiko = basis_risiko + max(0, 70 - self.zustand) / 700 + self.schaden * 0.02
        if random.random() < min(0.22, risiko):
            staerke = random.choices([1, 2, 3], weights=[70, 22, 8], k=1)[0]
            self.schaden = max(self.schaden, staerke)
            self.zustand = max(0, self.zustand - {1: 4, 2: 12, 3: 22}[staerke])
            self.sauberkeit = max(0, self.sauberkeit - random.randint(8, 18))
            unfall = self.schaden_label

        wert_nachher = self.verkaufswert
        self.letzte_fahrt = f"{fahrt} mit {km} km"

        return {
            "fahrt": fahrt,
            "km": km,
            "verbrauch": verbrauch,
            "wertverlust": max(0, wert_vorher - wert_nachher),
            "unfall": unfall,
        }

    def status_text(self):
        return (
            f"#{self.fahrzeug_id} | {self.marke} | {self.typ} | {self.haus_label} | "
            f"{self.farbe} | {self.ps} PS | {self.maxspeed} km/h | {self.km} km | "
            f"{self.energie_label} | Wert: {self.verkaufswert_label} | "
            f"Zustand: {self.zustand_label} | Sauberkeit: {self.sauberkeit_label} | "
            f"Schaden: {self.schaden_label} | {self.standort} | Besitzer: {self.besitzer}"
        )


class ElektroAuto(Auto):
    def __init__(
        self,
        config,
        marke,
        farbe,
        km=0,
        ps=140,
        maxspeed=190,
        batterie=70,
        besitzer="Niemand",
        preis=35_000,
        baujahr=2022,
        standort="Imperial Motors",
        premium=False,
        fahrzeug_id=None,
        zustand=100,
        sauberkeit=100,
        schaden=0,
    ):
        super().__init__(
            config=config,
            marke=marke,
            farbe=farbe,
            km=km,
            ps=ps,
            maxspeed=maxspeed,
            tank=batterie,
            besitzer=besitzer,
            preis=preis,
            baujahr=baujahr,
            standort=standort,
            premium=premium,
            fahrzeug_id=fahrzeug_id,
            zustand=zustand,
            sauberkeit=sauberkeit,
            schaden=schaden,
        )
        self.elektrisch = True
        self.set_energie(batterie)


class Garage:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.fahrzeuge = []
        self.cash = config.START_KAPITAL
        self.day = 1
        self.sold_count = 0
        self.accident_count = 0
        self.target_cash = config.KAPITAL_ZIEL

    def start_new_game(self):
        self.clear()
        self.cash = self.config.START_KAPITAL
        self.day = 1
        self.sold_count = 0
        self.accident_count = 0

    def clear(self):
        self.fahrzeuge.clear()

    def add_auto(self, fahrzeug):
        self.fahrzeuge.append(fahrzeug)

    def alle_fahrzeuge(self):
        return list(self.fahrzeuge)

    def get_fahrzeug_by_id(self, fahrzeug_id):
        for fahrzeug in self.fahrzeuge:
            if fahrzeug.fahrzeug_id == int(fahrzeug_id):
                return fahrzeug
        return None

    def filter_elektro(self):
        return [fahrzeug for fahrzeug in self.fahrzeuge if fahrzeug.elektrisch]

    def filter_benzin(self):
        return [fahrzeug for fahrzeug in self.fahrzeuge if not fahrzeug.elektrisch]

    def filter_normal(self):
        return [fahrzeug for fahrzeug in self.fahrzeuge if not fahrzeug.premium]

    def filter_premium(self):
        return [fahrzeug for fahrzeug in self.fahrzeuge if fahrzeug.premium]

    def _bezahlen(self, kosten):
        if kosten <= 0:
            return True
        if self.cash < kosten:
            return False
        self.cash -= kosten
        return True

    def refill_vehicle(self, fahrzeug):
        kosten = fahrzeug.auffuellen_kosten()
        if kosten <= 0:
            return True, 0
        if not self._bezahlen(kosten):
            return False, kosten
        if fahrzeug.elektrisch:
            fahrzeug.laden()
        else:
            fahrzeug.tanken()
        return True, kosten

    def tanken_alle(self):
        count = 0
        kosten_gesamt = 0
        uebersprungen = 0
        for fahrzeug in self.filter_benzin():
            erfolgreich, kosten = self.refill_vehicle(fahrzeug)
            if erfolgreich:
                if kosten > 0:
                    count += 1
                    kosten_gesamt += kosten
            else:
                uebersprungen += 1
        return count, kosten_gesamt, uebersprungen

    def laden_alle(self):
        count = 0
        kosten_gesamt = 0
        uebersprungen = 0
        for fahrzeug in self.filter_elektro():
            erfolgreich, kosten = self.refill_vehicle(fahrzeug)
            if erfolgreich:
                if kosten > 0:
                    count += 1
                    kosten_gesamt += kosten
            else:
                uebersprungen += 1
        return count, kosten_gesamt, uebersprungen

    def wash_vehicle(self, fahrzeug):
        kosten = fahrzeug.waschkosten
        if not self._bezahlen(kosten):
            return False, kosten, 0
        gewinn = fahrzeug.waschen()
        return True, kosten, gewinn

    def service_vehicle(self, fahrzeug):
        kosten = fahrzeug.wartungskosten
        if not self._bezahlen(kosten):
            return False, kosten, 0
        gewinn = fahrzeug.warten()
        return True, kosten, gewinn

    def repair_vehicle(self, fahrzeug):
        kosten = fahrzeug.reparaturkosten
        if not self._bezahlen(kosten):
            return False, kosten, None
        report = fahrzeug.reparieren()
        return True, kosten, report

    def buy_vehicle(self, fahrzeug, ankaufspreis):
        preis = max(0, int(ankaufspreis))
        if not self._bezahlen(preis):
            return False, preis
        fahrzeug.besitzer = self.name
        self.fahrzeuge.append(fahrzeug)
        return True, preis

    def sell_vehicle(self, fahrzeug, verkaufspreis=None):
        if fahrzeug not in self.fahrzeuge:
            return None
        if verkaufspreis is None:
            verkaufspreis = fahrzeug.verkaufswert
        verkaufspreis = max(0, int(verkaufspreis))
        self.cash += verkaufspreis
        self.fahrzeuge.remove(fahrzeug)
        self.sold_count += 1
        return verkaufspreis

    def status_bericht(self):
        return [fahrzeug.status_text() for fahrzeug in self.fahrzeuge]

    def advance_day(self):
        report = {
            "day": self.day,
            "next_day": self.day + 1,
            "gesamt_km": 0,
            "wertverlust": 0,
            "unfaelle": 0,
            "events": [],
        }
        for fahrzeug in self.fahrzeuge:
            event = fahrzeug.simuliere_tag()
            report["gesamt_km"] += event["km"]
            report["wertverlust"] += event["wertverlust"]
            if event["unfall"] is not None:
                report["unfaelle"] += 1
                self.accident_count += 1
            report["events"].append(
                {
                    "fahrzeug": fahrzeug,
                    **event,
                }
            )

        report["events"].sort(
            key=lambda event: (
                event["unfall"] is not None,
                event["wertverlust"],
                event["km"],
            ),
            reverse=True,
        )
        self.day += 1
        return report

    def statistik(self):
        gesamt = len(self.fahrzeuge)
        elektro = len(self.filter_elektro())
        premium = len(self.filter_premium())
        normal = gesamt - premium
        benzin = gesamt - elektro
        durchschnitt_ps = round(
            sum(fahrzeug.ps for fahrzeug in self.fahrzeuge) / gesamt,
            1,
        ) if gesamt else 0
        durchschnitt_km = round(
            sum(fahrzeug.km for fahrzeug in self.fahrzeuge) / gesamt,
            1,
        ) if gesamt else 0
        durchschnitt_preis = round(
            sum(fahrzeug.verkaufswert for fahrzeug in self.fahrzeuge) / gesamt,
            1,
        ) if gesamt else 0
        durchschnitt_zustand = round(
            sum(fahrzeug.zustand for fahrzeug in self.fahrzeuge) / gesamt,
            1,
        ) if gesamt else 0
        durchschnitt_sauberkeit = round(
            sum(fahrzeug.sauberkeit for fahrzeug in self.fahrzeuge) / gesamt,
            1,
        ) if gesamt else 0
        bestandswert = sum(fahrzeug.verkaufswert for fahrzeug in self.fahrzeuge)
        schadensfaelle = len([fahrzeug for fahrzeug in self.fahrzeuge if fahrzeug.schaden > 0])
        marken_counter = Counter(fahrzeug.marke for fahrzeug in self.fahrzeuge)
        haeufigste_marke = (
            marken_counter.most_common(1)[0][0]
            if marken_counter
            else "-"
        )
        teuerstes = max(
            self.fahrzeuge,
            key=lambda fahrzeug: fahrzeug.verkaufswert,
            default=None,
        )

        return {
            "tag": self.day,
            "cash": self.cash,
            "target_cash": self.target_cash,
            "goal_left": max(0, self.target_cash - self.cash),
            "sold_count": self.sold_count,
            "accident_count": self.accident_count,
            "gesamt": gesamt,
            "elektro": elektro,
            "benzin": benzin,
            "premium": premium,
            "normal": normal,
            "schadensfaelle": schadensfaelle,
            "durchschnitt_ps": durchschnitt_ps,
            "durchschnitt_km": durchschnitt_km,
            "durchschnitt_preis": durchschnitt_preis,
            "durchschnitt_zustand": durchschnitt_zustand,
            "durchschnitt_sauberkeit": durchschnitt_sauberkeit,
            "bestandswert": bestandswert,
            "haeufigste_marke": haeufigste_marke,
            "teuerstes_auto": teuerstes,
        }
