from interactable import Interactable
from objects.connection import Connected
from objects.weight import Weight
from objects.player import Player
from event import Event

class Fire(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 408)

    def interact(self, obj):
        if isinstance(obj, Connected):
            obj.unfreeze()
            return Event.UNFREEZE
