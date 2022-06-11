

class Box:
    def __init__(self, x, y, tileset, index, moveables, collision):
        self.x = x
        self.y = y
        self.tileset = tileset
        self.index = index
        self.moveables = moveables
        self.collision = collision

    def move(self, dx, dy):
        if self.can_move_to(dx, dy):
            self.push(dx, dy)

    def push(self, dx, dy):
        self.x += dx
        self.y += dy

        for box in self.moveables:
            if box is self:
                continue
            if box.x == self.x and box.y == self.y:
                box.push(dx, dy)
                break

    def can_move_to(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.collision[new_y, new_x]:
            return False

        for box in self.moveables:
            if box is self:
                continue
            if box.x == new_x and box.y == new_y:
                if not box.can_move_to(dx, dy):
                    return False

        return True

    def render(self, surface):
        scale = self.tileset.scale
        tw, th = self.tileset.size

        img = self.tileset.tiles[self.index]
        surface.blit(img, (self.x * tw * scale, self.y * th * scale))
