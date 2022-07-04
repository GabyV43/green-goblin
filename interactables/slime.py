from interactable import Interactable
from objects.weight import Weight
from objects.player import Player
from event import Event
from pygame import mixer

class Slime(Interactable):
    def __init__(self, x, y, tileset, index):
        super().__init__(x, y, tileset, index)
        self.active = True

    def interact(self, obj):
        if not self.active:
            return
        if type(obj) is Weight:
            slimew_sound = mixer.Sound("sounds_effects/slime.mp3")
            slimew_sound.set_volume(0.2)
            slimew_sound.play()
            return Event.WEIGHT_LOCK
        if type(obj) is Player:
            slimep_sound = mixer.Sound("sounds_effects/slime.mp3")
            slimep_sound.set_volume(0.5)
            slimep_sound.play()
            return Event.PLAYER_LOCK

    def render(self, surface):
        if not self.active:
            return
        return super().render(surface)

    def toggle(self):
        self.active = not self.active

