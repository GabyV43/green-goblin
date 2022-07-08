from interactable import Interactable
from objects.moveable import Moveable
from event import Event
from pygame import mixer

class Button(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 262)
        
    def interact(self, obj):
        if issubclass(type(obj), Moveable):
            return Event.BUTTON_PRESS

    def uninteract(self, obj):
        if issubclass(type(obj), Moveable):
            return Event.BUTTON_UNPRESS