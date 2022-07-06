from enum import Enum

class Event(Enum):
    LEVEL_UNEND = -1
    LEVEL_END = 0
    PLAYER_DIE = 1
    WEIGHT_DIE = 2
    BUTTON_PRESS = 3
    BUTTON_UNPRESS = 4
    PLAYER_LOCK = 5
    WEIGHT_LOCK = 6
    FREEZE = 7
    UNFREEZE = 8
