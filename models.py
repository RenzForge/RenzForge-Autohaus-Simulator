from collections import Counter


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
        preis=18000,
        baujahr=2022,
        standort="Autohaus Schneider",
        premium=False,
        fahrzeug_id=None,
    ):
        self.config = config
        self.fahrzeug_id = Auto._generate_id() if fahrzeug_id is None else int(fahrzeug_id)
        self.marke = marke
        self.farbe = farbe
        self.km = max(0, int(km))
        self.ps = max(1, int(ps))
        self.maxspeed = max(1, int(maxspeed))
        self.tank = max(0, min(self.config.MAX_TANK, int(tank)))
        self.elektrisch = False
        self._besitzer = besitzer
        self.preis = max(1000, int(preis))
        self.baujahr = max(1980, int(baujahr))
        self.standort = standort
        self.premium = bool(premium)

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
            self.tank = min(self.config.MAX_TANK, self.tank + max(0, int(menge)))
        return self.tank - start

    def laden(self, menge=None):
        if not self.elektrisch:
            return 0
        start = self.tank
        if menge is None:
            self.tank = self.config.MAX_BATTERIE
        else:
            self.tank = min(self.config.MAX_BATTERIE, self.tank + max(0, int(menge)))
        return self.tank - start

    def fahren(self, km):
        km = max(0, int(km))
        if km == 0:
            return 0
        verbrauch = max(1, round(km * self.verbrauch_pro_100km / 100))
        self.km += km
        self.tank = max(0, self.tank - verbrauch)
        return verbrauch

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
    ):
        self.marke = marke
        self.farbe = farbe
        self.km = max(0, int(km))
        self.ps = max(1, int(ps))
        self.maxspeed = max(1, int(maxspeed))
        self.besitzer = besitzer
        self.preis = max(1000, int(preis))
        self.baujahr = max(1980, int(baujahr))
        self.standort = standort
        self.premium = bool(premium)
        self.elektrisch = bool(elektrisch)
        self.set_energie(energie)

    def status_text(self):
        return (
            f"#{self.fahrzeug_id} | {self.marke} | {self.typ} | {self.haus_label} | "
            f"{self.farbe} | {self.ps} PS | {self.maxspeed} km/h | {self.km} km | "
            f"{self.energie_label} | {self.preis_label} | {self.standort} | "
            f"Besitzer: {self.besitzer}"
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
        preis=35000,
        baujahr=2022,
        standort="Imperial Motors",
        premium=False,
        fahrzeug_id=None,
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
        )
        self.elektrisch = True
        self.set_energie(batterie)


class Garage:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.fahrzeuge = []

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

    def tanken_alle(self):
        count = 0
        for fahrzeug in self.filter_benzin():
            if fahrzeug.tank < self.config.MAX_TANK and fahrzeug.tanken() > 0:
                count += 1
        return count

    def laden_alle(self):
        count = 0
        for fahrzeug in self.filter_elektro():
            if fahrzeug.tank < self.config.MAX_BATTERIE and fahrzeug.laden() > 0:
                count += 1
        return count

    def status_bericht(self):
        return [fahrzeug.status_text() for fahrzeug in self.fahrzeuge]

    def statistik(self):
        gesamt = len(self.fahrzeuge)
        elektro = len(self.filter_elektro())
        premium = len(self.filter_premium())
        normal = gesamt - premium
        benzin = gesamt - elektro
        durchschnitt_ps = round(
            sum(fahrzeug.ps for fahrzeug in self.fahrzeuge) / gesamt, 1
        ) if gesamt else 0
        durchschnitt_km = round(
            sum(fahrzeug.km for fahrzeug in self.fahrzeuge) / gesamt, 1
        ) if gesamt else 0
        durchschnitt_preis = round(
            sum(fahrzeug.preis for fahrzeug in self.fahrzeuge) / gesamt, 1
        ) if gesamt else 0
        bestandswert = sum(fahrzeug.preis for fahrzeug in self.fahrzeuge)
        marken_counter = Counter(fahrzeug.marke for fahrzeug in self.fahrzeuge)
        haeufigste_marke = marken_counter.most_common(1)[0][0] if marken_counter else "-"
        teuerstes = max(self.fahrzeuge, key=lambda fahrzeug: fahrzeug.preis, default=None)

        return {
            "gesamt": gesamt,
            "elektro": elektro,
            "benzin": benzin,
            "premium": premium,
            "normal": normal,
            "durchschnitt_ps": durchschnitt_ps,
            "durchschnitt_km": durchschnitt_km,
            "durchschnitt_preis": durchschnitt_preis,
            "bestandswert": bestandswert,
            "haeufigste_marke": haeufigste_marke,
            "teuerstes_auto": teuerstes,
        }
