from interactable import Interactable
from objects.weight import Weight
from event import Event

class WeightEnd(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 523)
        self.inter = False

    def interact(self, obj):
        if type(obj) is Weight:
            self.inter = True
            return Event.LEVEL_END

    def uninteract(self, obj):
        if type(obj) is Weight:
            self.inter = False
            return Event.LEVEL_UNEND

    def render(self, surface):
        if self.inter:
            super().render(surface, 467)
        else:
            super().render(surface)

