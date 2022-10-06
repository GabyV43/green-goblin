from interactable import Interactable
from event import Event
from objects.box import Box


class BoxEnd(Interactable):
    def __init__(self, x, y, tileset):
        super().__init__(x, y, tileset, 553)
        self.active = False

    def interact(self, obj):
        if type(obj) is Box:
            self.active = True
            return Event.LEVEL_END

    def uninteract(self, obj):
        if type(obj) is Box:
            self.active = False
            return Event.LEVEL_UNEND

    def render(self, surface, offset=(0, 0)):
        if self.active:
            super().render(surface, 495, offset)
        else:
            super().render(surface, offset=offset)

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
