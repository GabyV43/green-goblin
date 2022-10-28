class TileMap:
    def __init__(self, tileset, matrix):
        self.tileset = tileset
        self.data = matrix

    def render(self, surface, offset=(0, 0)):
        scale = self.tileset.scale
        tw, th = self.tileset.size

        h, w = self.data.shape
        for y in range(h):
            for x in range(w):
                tile = self.data[y, x]
                if tile != -1:
                    img = self.tileset.tiles[tile]
                    surface.blit(img, (x * tw * scale + offset[0], y * th * scale + offset[1]))

    def resize(self, scale):
        self.tileset.resize(scale)
