import random


class Config:
    def __init__(self):
        self.PRINTSTATE = 1
        self.PRINT_NONE = 0
        self.PRINT_INFO = 1
        self.PRINT_DEBUG = 2
        self.SLEEP_TIME = 0.5
        self.MAX_BATTERIE = 100
        self.MAX_TANK = 100

        # Spiel-Setup
        self.START_KAPITAL = 250_000
        self.KAPITAL_ZIEL = 1_000_000
        self.PREMIUM_RATE = 0.18
        self.ELEKTRO_RATE = 0.32

        # Laufende Kosten
        self.WASH_COST = 120
        self.SERVICE_COST = 650
        self.REPAIR_COST_LIGHT = 900
        self.REPAIR_COST_MEDIUM = 3_400
        self.REPAIR_COST_HEAVY = 8_900

        # Energiepreise
        self.STROM_MIN_PREIS = 0.48
        self.STROM_MAX_PREIS = 1.56
        self.BENZIN_MIN_PREIS = 1.44
        self.BENZIN_MAX_PREIS = 2.68

        # Tageszyklus
        self.DAY_TIMER_MIN_SEC = 180
        self.DAY_TIMER_MAX_SEC = 240

        # Kompatible Alias-Namen fuer bestehenden Code.
        self.START_CASH = self.START_KAPITAL
        self.TARGET_CASH = self.KAPITAL_ZIEL

    @property
    def strompreis(self):
        return round(random.uniform(self.STROM_MIN_PREIS, self.STROM_MAX_PREIS), 2)

    @property
    def benzinpreis(self):
        return round(random.uniform(self.BENZIN_MIN_PREIS, self.BENZIN_MAX_PREIS), 2)

    def set_debug(self, level):
        self.PRINTSTATE = level
