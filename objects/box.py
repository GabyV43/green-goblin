from objects.connection import Connected


class Box(Connected):
    def __init__(self, x, y, tileset, moveables, collision):
        super().__init__(x, y, tileset, 146, moveables, collision)
