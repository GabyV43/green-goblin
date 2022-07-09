from interactable import Interactable
from event import Event
from objects.moveable import Moveable

class Hole(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 206)

    def interact(self, obj):
        if issubclass(type(obj), Moveable):
            obj.die()
            obj.disappear()
