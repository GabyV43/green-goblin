import math
import os
import xml.etree.ElementTree as ET
from tkinter import filedialog

import pygame

from . import cache
from .scalable import Scalable


class TileSet(Scalable):
    file: str
    tile_size: tuple[int, int]
    margin: int
    spacing: int
    image: pygame.Surface
    indexes: list[int]
    original_tiles: list[pygame.Surface]
    scaled_tiles: list[pygame.Surface]
    scale: float
    chain_original: pygame.Surface
    chain: pygame.Surface

    def __init__(self, tile_size: tuple[int, int] | int, margin: int, spacing: int, scale: float):
        tileset_path: str
        if has_path := cache.has("tileset-path"):
            tileset_path = cache.get("tileset-path")
        while not has_path or not os.path.exists(tileset_path):
            has_path = True
            tileset_path = filedialog.askopenfilename(
                title="Select the Tileset to be used",
                filetypes=[
                    ("Tiled TileSet XML", "*.tsx")
                ]
            )
            if tileset_path == '':
                exit()

            cache.set("tileset-path", tileset_path)
        self.file = tileset_path
        if type(tile_size) is int:
            self.tile_size = (tile_size, tile_size)
        else:
            self.tile_size = tile_size

        self.margin = margin
        self.spacing = spacing

        tree = ET.parse(self.file)
        image = tree.getroot()[0]
        assert image.tag == "image"

        img_path = os.path.join(os.path.dirname(
            self.file), image.attrib["source"])

        self.image = pygame.image.load(img_path)

        self.chain_original = pygame.image.load("images/chain.png")

        self.initial_load()
        self.rescale(scale)

    def initial_load(self):
        self.original_tiles = []
        self.indexes = []

        x0 = y0 = self.margin
        w, h = self.image.get_rect().size
        dx = self.tile_size[0] + self.spacing
        dy = self.tile_size[1] + self.spacing

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.tile_size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.tile_size))

                if not (pygame.surfarray.array_alpha(tile) == 0).all():
                    self.indexes.append(len(self.original_tiles))
                    self.original_tiles.append(tile)
                else:
                    self.indexes.append(-1)

    def rescale(self, scale: float):
        self.scale = scale
        self.scaled_tiles = []

        for tile in self.original_tiles:
            resized = pygame.transform.scale(
                tile,
                (
                    math.ceil(self.tile_size[0] * scale),
                    math.ceil(self.tile_size[1] * scale),
                )
            )
            self.scaled_tiles.append(resized)

        self.chain = pygame.transform.scale(
            self.chain_original,
            (
                (
                    math.ceil(self.chain_original.get_width() * scale),
                    math.ceil(self.chain_original.get_height() * scale),
                )
            )
        )

    def get_tile(self, index: int) -> pygame.Surface:
        return self.scaled_tiles[self.indexes[index]]

    def get_original_tile(self, index: int) -> pygame.Surface:
        return self.original_tiles[self.indexes[index]]
