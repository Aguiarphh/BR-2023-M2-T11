from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import SHIELD, SHIELD_TYPE, HAMMER, HAMMER_TYPE, TIME_DECREASE, TIME_DECREASE_TYPE

class Shield(PowerUp):
    def __init__(self):
        super().__init__(SHIELD, SHIELD_TYPE)

class Hammer(PowerUp):
    def __init__(self):
        super().__init__(HAMMER, HAMMER_TYPE)

class Time_decrease(PowerUp):
    def __init__(self):
        super().__init__(TIME_DECREASE, TIME_DECREASE_TYPE)
        
