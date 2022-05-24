import csv
import numpy as np


class TileMap:
    def __init__(self, filename, tileset):
        self.filename = filename
        self.tileset = tileset

        self.load()

    def load(self):
        file = open(self.filename)
        self.data = np.array(list(csv.reader(file)), dtype=int)

    def render(self, surface):
        scale = self.tileset.scale
        tw, th = self.tileset.size

        h, w = self.data.shape
        for y in range(h):
            for x in range(w):
                tile = self.data[y, x]
                if tile != -1:
                    img = self.tileset.tiles[tile]
                    surface.blit(img, (x * tw * scale, y * th * scale))

    def resize(self, scale):
        self.tileset.resize(scale)
