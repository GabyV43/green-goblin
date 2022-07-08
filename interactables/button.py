from interactable import Interactable
from objects.moveable import Moveable
from event import Event
from pygame import mixer

class Button(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 262)
    def interact(self, obj):
        if issubclass(type(obj), Moveable):
            button_sound = mixer.Sound("sounds_effects/button_press.mp3")
            button_sound.set_volume(0.5)
            button_sound.play()
            return Event.BUTTON_PRESS

    def uninteract(self, obj):
        if issubclass(type(obj), Moveable):
            return Event.BUTTON_UNPRESS