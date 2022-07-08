from interactable import Interactable
from objects.moveable import Moveable
from objects.weight import Weight
from objects.player import Player
from event import Event
from pygame import mixer

class Slime(Interactable):
    def __init__(self, x, y, tileset, index, active = True):
        super().__init__(x, y, tileset, index)
        self.active = active

    def interact(self, obj):
        if not self.active:
            obj.unlock()
            return
        if issubclass(type(obj), Moveable):
            slimew_sound = mixer.Sound("sounds_effects/slime.mp3")
            slimew_sound.set_volume(0.2)
            slimew_sound.play()

            obj.lock()

    def render(self, surface, offset=(0, 0)):
        if not self.active:
            return
        return super().render(surface, offset=offset)

    def toggle(self):
        self.active = not self.active

    def get_state(self):
        return (
            self.x,
            self.y,
            self.active,
        )

    def load_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.active = state[2]

