from objects.connection import Connected


class Weight(Connected):
    def __init__(self, x, y, tileset, moveables, collision):
        super().__init__(x, y, tileset, 148, moveables, collision)

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def render(self, surface, offset=(0, 0)):
        if self.frozen:
            super().render(surface, 149, offset)
        else:
            super().render(surface, offset=offset)

    def get_state(self):
        return (
            self.x,
            self.y,
            self.old_x,
            self.old_y,
            self.dead,
            self.disappeared,
            self.locked,
            self.frozen,
        )

    def load_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.old_x = state[2]
        self.old_y = state[3]
        self.dead = state[4]
        self.disappeared = state[5]
        self.locked = state[6]
        self.frozen = state[7]
