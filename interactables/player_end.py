from interactable import Interactable
from objects.player import Player
from event import Event

class PlayerEnd(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 581)
        self.active = False

    def interact(self, obj):
        if type(obj) is Player:
            self.active = True
            return Event.LEVEL_END

    def uninteract(self, obj):
        if type(obj) is Player:
            self.active = False
            return Event.LEVEL_UNEND

    def render(self, surface):
        if self.active:
            super().render(surface, 465)
        else:
            super().render(surface)


