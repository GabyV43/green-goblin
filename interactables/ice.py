from event import Event
from interactable import Interactable
from objects.connection import Connected


class Ice(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 378)

    def interact(self, obj):
        if isinstance(obj, Connected):
            obj.freeze()
            return Event.FREEZE
