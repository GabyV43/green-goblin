from interactable import Interactable
from objects.moveable import Moveable
from event import Event

from objects.weight import Weight


class HeavyButton(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 263)

    def interact(self, obj):
        if type(obj) is Weight:
            return Event.BUTTON_PRESS

    def uninteract(self, obj):
        if type(obj) is Weight:
            return Event.BUTTON_UNPRESS
