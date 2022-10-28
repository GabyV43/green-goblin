from objects.connection import Connected


class Box(Connected):
    def __init__(self, x, y, tileset, moveables, collision, uid: int):
        super().__init__(x, y, tileset, 146, moveables, collision, uid)

    def render(self, surface, index=-1, offset=(0, 0)):
        if self.frozen:
            super().render(surface, 31, offset)
        else:
            super().render(surface, index, offset)
