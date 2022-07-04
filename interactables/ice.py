from interactable import Interactable
from objects.weight import Weight
from objects.player import Player
from event import Event

class Ice(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 378)
    def interact(self, obj):
        if type(obj) is Weight or type(obj) is Player:
            return Event.FREEZE
