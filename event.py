from enum import Enum

class Event(Enum):
    LEVEL_END = 0
    PLAYER_DIE = 1
    WEIGHT_DIE = 2
    BUTTON_PRESS = 3
    PLAYER_LOCK = 4
    WEIGHT_LOCK = 5
    FREEZE = 6
    UNFREEZE = 7
