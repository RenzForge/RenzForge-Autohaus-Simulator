class Config:
    def __init__(self):
        self.PRINTSTATE = 1
        self.PRINT_NONE = 0
        self.PRINT_INFO = 1
        self.PRINT_DEBUG = 2
        self.SLEEP_TIME = 0.5
        self.MAX_BATTERIE = 100
        self.MAX_TANK = 100
    
    def set_debug(self, level):
        self.PRINTSTATE = level