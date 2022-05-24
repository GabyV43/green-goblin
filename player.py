

class Player:
    def __init__(self, tileset, index, x, y):
        self.tileset = tileset
        self.index = index
        self.x = x
        self.y = y

    def render(self, surface):
        scale = self.tileset.scale
        tw, th = self.tileset.size

        img = self.tileset.tiles[self.index]
        surface.blit(img, (self.x * tw * scale, self.y * th * scale))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
