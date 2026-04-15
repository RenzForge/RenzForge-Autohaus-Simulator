class Config:
    def __init__(self):
        self.PRINTSTATE = 1
        self.PRINT_NONE = 0
        self.PRINT_INFO = 1
        self.PRINT_DEBUG = 2
        self.SLEEP_TIME = 0.5
        self.MAX_BATTERIE = 100
        self.MAX_TANK = 100

        # Kleine Spielwerte fuer den Autohaus-Modus.
        self.START_CASH = 250_000
        self.TARGET_CASH = 1_000_000

        self.WASH_COST = 120
        self.SERVICE_COST = 650
        self.REPAIR_COST_LIGHT = 900
        self.REPAIR_COST_MEDIUM = 3_400
        self.REPAIR_COST_HEAVY = 8_900

        self.BENZIN_PREIS = 2.15
        self.STROM_PREIS = 0.35

    def set_debug(self, level):
        self.PRINTSTATE = level
