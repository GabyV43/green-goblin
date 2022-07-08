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

    def render(self, surface, offset=(0,0)):
        if not self.inter:
            super().render(surface, offset=offset)
        else:
            super().render(surface, 206, offset)

    def get_state(self):
        return (
            self.x,
            self.y,
            self.inter,
        )

    def load_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.inter = state[2]

