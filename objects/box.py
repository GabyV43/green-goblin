from objects.moveable import Moveable


class Box(Moveable):
    def __init__(self, x, y, tileset, moveables, collision):
        super().__init__(x, y, tileset, 146, moveables, collision)

