from objects.moveable import Moveable

class Weight(Moveable):
    def __init__(self, x, y, tileset, moveables, collision):
        super().__init__(x, y, tileset, 148, moveables, collision)
