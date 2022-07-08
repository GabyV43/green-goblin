import pygame
from pygame.locals import SRCALPHA
from math import ceil


class TileSet:
    def __init__(self, file, tile_size, margin, spacing, scale):
        self.file = file
        self.size = tile_size  # [largura, altura]
        self.margin = margin
        self.spacing = spacing

        self.image = pygame.image.load(file)
        self.original_tiles = []
        self.tiles = []

        self.load()
        self.resize(scale)

    def load(self):
        self.original_tiles = []
        x0 = self.margin
        y0 = self.margin
        w, h = self.image.get_rect().size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size, SRCALPHA)
                tile.blit(self.image, (0,0), (x, y, *self.size))

                self.original_tiles.append(tile)


    def resize(self, scale, offset = (0, 0)):
        self.scale = scale
        self.tiles = []
        for tile in self.original_tiles:
            resized = pygame.transform.scale(tile, (ceil(self.size[0] * scale + offset[0]), ceil(self.size[1] * scale + offset[1])))
            self.tiles.append(resized)
