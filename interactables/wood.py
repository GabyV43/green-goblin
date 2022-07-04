from interactable import Interactable
from objects.weight import Weight
from event import Event


class Wood(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 204)
        self.inter = False

    def interact(self, obj):
        if type(obj) is Weight:
            self.inter = True
            return Event.WEIGHT_DIE

    def render(self, surface):
        if not self.inter:
            super().render(surface)
        else:
            super().render(surface, 206)

