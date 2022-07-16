from interactable import Interactable
from event import Event
from objects.moveable import Moveable
from objects.player import Player
from objects.weight import Weight


class Hole(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 206)

    def interact(self, obj):
        if issubclass(type(obj), Moveable):
            obj.die()
            obj.disappear()
            if type(obj) is Player:
                return Event.PLAYER_DIE
            elif type(obj) is Weight:
                return Event.WEIGHT_DIE
