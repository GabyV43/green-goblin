from interactable import Interactable
from objects.player import Player
from event import Event

class PlayerEnd(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 581)
        self.inter = False

    def interact(self, obj):
        if type(obj) is Player:
            self.inter = True
            return Event.LEVEL_END

    def render(self, surface):
        if self.inter:
            super().render(surface, 465)
        else:
            super().render(surface)


