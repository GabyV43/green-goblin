from interactable import Interactable
from objects.weight import Weight
from objects.player import Player
from event import Event

class Fire(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 408)

    def interact(self, obj):
        print("Fire interact")
        if (type(obj) is Weight) or (type(obj) is Player):
            print("Fire return event")
            return Event.UNFREEZE
