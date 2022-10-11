import os
import random
import numpy
import pygame
from editor.tiles import SOUNDS, TILES

from loader import Loader
from .bar import Bar
from .event_handler import EventHandler
from .renderable import Renderable
from .scalable import Scalable
from .tilemap import TileMap
from .tileset import TileSet


class Screen(Renderable, EventHandler, Scalable):
    tileset: TileSet
    tilemap: TileMap
    tile_mouse_pos: tuple[int, int]
    mouse_pos: tuple[int, int]
    drag: int
    bar: Bar
    screen_size: tuple[int, int]
    loader: Loader | None
    set_sounds: list[pygame.mixer.Sound]

    def __init__(self, screen_size: tuple[int, int], bar_columns: int) -> None:
        pygame.display.set_caption('Green Goblin Editor - New file')
        map_size = [8, 10]
        tile_size = (32, 32)
        self.screen_size = screen_size
        scale = min(
            screen_size[0] / ((map_size[1] + bar_columns) * tile_size[0]),
            screen_size[1] / (map_size[0] * tile_size[1])
        )
        self.tileset = TileSet(tile_size, 0, 0, scale)
        self.loader = None

        matrix = numpy.ndarray(map_size[::-1], int)
        self.tilemap = TileMap(self.tileset, matrix, self)
        self.bar = Bar(self.tileset, bar_columns, screen_size, self.tilemap)
        self.drag = -1
        root = SOUNDS["root"]
        self.set_sounds = [
            None #pygame.mixer.Sound(os.path.join(root, file))
            for file in SOUNDS["set"]
        ]

    def handle_event(self, event: pygame.event.Event):
        if self.loader is not None:
            self.drag = -1
            self.loader.level.update(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.drag = 1
                    self.bar.clicked_at(self.mouse_pos)
                    self.handle_set()
                elif event.button == 3:
                    self.drag = 3
                    self.handle_remove()
            elif event.type == pygame.MOUSEMOTION:
                if self.drag == 1:
                    self.handle_set()
                elif self.drag == 3:
                    self.handle_remove()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drag = -1
        if event.type == pygame.KEYDOWN:
            if self.loader is None:
                if event.key == pygame.K_ESCAPE:
                    self.bar.selected = -1
                self.bar.handle_keydown(event.key)
            elif event.key == pygame.K_ESCAPE:
                self.finish_test()
        elif event.type in [pygame.WINDOWRESIZED, pygame.WINDOWSIZECHANGED]:
            self.rescale(-1)
            if self.loader is not None:
                self.loader.resize_tileset(*self.screen_size)

    def handle_set(self):
        pos = self.tile_mouse_pos
        if not (0 <= pos[0] < self.tilemap.shape[0]) or not (0 <= pos[1] < self.tilemap.shape[1]):
            return
        if self.bar.selected == -1:
            return
        tile = self.bar.selected_tile()
        type = tile["type"]
        sound = random.choice(self.set_sounds)
        if type == "ground":
            self.tilemap.set_ground(self.tile_mouse_pos, sound)
        elif type == "player":
            self.tilemap.set_player(self.tile_mouse_pos, sound)
        elif type == "weight":
            self.tilemap.set_weight(self.tile_mouse_pos, sound)
        elif type == "movable":
            self.tilemap.set_movable(self.tile_mouse_pos, tile["id"], sound)
        elif type == "interactable":
            self.tilemap.set_interactable(
                self.tile_mouse_pos, tile["id"], sound)
        elif type == "slime":
            self.tilemap.set_slime(self.tile_mouse_pos,
                                   tile["id"] == 527, sound)

    def handle_remove(self):
        pos = self.tile_mouse_pos
        if not (0 <= pos[0] < self.tilemap.shape[0]) or not (0 <= pos[1] < self.tilemap.shape[1]):
            return
        self.tilemap.remove(pos, self.bar.selected)

    def render(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        if self.loader is not None:
            self.loader.level.render(surface)
            return

        self.mouse_pos = mx, my = pygame.mouse.get_pos()
        sx = self.tileset.tile_size[0] * self.tileset.scale
        sy = self.tileset.tile_size[1] * self.tileset.scale
        mx //= sx
        my //= sy
        self.tile_mouse_pos = (int(mx), int(my))

        self.tilemap.render(surface, offset)

        if 0 <= mx < self.tilemap.shape[0] and 0 <= my < self.tilemap.shape[1]:
            sel = self.bar.selected_tile()
            if sel is not None:
                if self.tilemap.get(self.tile_mouse_pos) == -1:
                    img = self.tileset.get_tile(
                        sel["id"]).copy()
                    img.set_alpha(100)
                    surface.blit(img, (mx * sx, my * sy),
                                 self.tileset.scaled_tiles[0].get_rect())

            else:
                pygame.draw.rect(surface, (255, 0, 0), (
                    mx * sx, my * sy,
                    sx, sy
                ), 2)

        # Draw bar
        self.bar.render(surface, offset)

    def rescale(self, scale: float):
        self.screen_size = pygame.display.get_surface().get_size()

        if scale == -1:
            scale = min(
                (self.screen_size[0] - self.bar.width) / (self.tilemap.shape[0]
                                                          * self.tileset.tile_size[0]),
                self.screen_size[1] / (self.tilemap.shape[1]
                                       * self.tileset.tile_size[1])
            )

        self.bar.rescale(scale)
        self.tileset.rescale(scale)
        self.tilemap.rescale(scale)

    def finish_test(self):
        self.loader = None
