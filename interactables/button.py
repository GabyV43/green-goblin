from event import Event
from interactable import Interactable
from objects.moveable import Moveable


class Button(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 262)

    def interact(self, obj):
        if issubclass(type(obj), Moveable):
            return Event.BUTTON_PRESS

    def uninteract(self, obj):
        if issubclass(type(obj), Moveable):
            return Event.BUTTON_UNPRESS
