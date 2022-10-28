import math

import pygame

from .renderable import Renderable
from .scalable import Scalable
from .tilemap import TileMap
from .tiles import TILE_KEYS, TILES
from .tileset import TileSet
from .ui.button import Button
from .ui.text import Text


class Bar(Renderable, Scalable):
    scale: float
    width: int
    screen_size: tuple[int, int]
    columns: int
    lines: int
    tiles: list[pygame.Surface]
    tileset: TileSet
    tilemap: TileMap
    selected: int
    selected_pos: tuple[int, int]
    font: pygame.font.Font
    save_as: Button
    save: Button
    load: Button
    wrm: Button
    wrp: Button
    wlm: Button
    wlp: Button
    hbm: Button
    hbp: Button
    hum: Button
    hup: Button
    reset: Button
    test: Button
    size_txt: Text

    def __init__(self, tileset: TileSet, columns: int, screen_size: tuple[int, int], tilemap: TileMap):
        self.columns = columns
        self.lines = math.ceil(len(TILES) / columns)
        self.screen_size = screen_size
        # 140 * scl + 32 * lines * scl <= screen_size[1]
        # scl * (140 + self.tileset.tile_size[1] * lines) <= screen_size[1]
        self.scale = min(
            screen_size[1] / (140 + tileset.tile_size[1] * self.lines),
            tileset.scale
        )
        self.width = int(tileset.tile_size[0] * self.scale * columns)
        self.tileset = tileset
        self.tilemap = tilemap
        self.selected = 0
        self.selected_pos = (0, 0)

        self.tiles = [
            pygame.transform.scale(
                self.tileset.get_original_tile(k["id"]),
                (
                    math.ceil(self.tileset.tile_size[0] * self.scale),
                    math.ceil(self.tileset.tile_size[1] * self.scale),
                )
            )
            for k in TILES.values()]

        self._setup_buttons()

    def render(self, surface: pygame.Surface, offset: tuple[int, int] = ...):
        pygame.draw.rect(surface, (30, 30, 30), (
            self.screen_size[0] - self.width + offset[0],
            offset[1],
            self.width,
            self.screen_size[1],
        ))

        i = 0
        tw = self.tileset.tile_size[0] * self.scale
        th = self.tileset.tile_size[1] * self.scale
        for line in range(math.ceil(len(TILES) / self.columns)):
            for col in range(self.columns):
                if i >= len(self.tiles):
                    break
                surface.blit(
                    self.tiles[i], (
                        self.screen_size[0] - self.width +
                        offset[0] + tw * col,
                        offset[1] + th * line,
                    )
                )
                i += 1

        if self.selected != -1:
            pygame.draw.rect(surface, (255, 0, 0, 100), (
                self.screen_size[0] - self.width +
                offset[0] + tw * self.selected_pos[0],
                offset[1] + th * self.selected_pos[1],
                tw, th
            ), 2)

        if self.tilemap.source is not None:
            self.save.render(surface, offset)
        self.save_as.render(surface, offset)
        self.load.render(surface, offset)
        self.reset.render(surface, offset)
        self.test.render(surface, offset)

        self.size_txt.render(surface, offset)

        self.wrm.render(surface, offset)
        self.wrp.render(surface, offset)
        self.wlm.render(surface, offset)
        self.wlp.render(surface, offset)

        self.hum.render(surface, offset)
        self.hup.render(surface, offset)
        self.hdm.render(surface, offset)
        self.hdp.render(surface, offset)

    def clicked_at(self, mouse_pos: tuple[int, int]):
        mx = mouse_pos[0] - self.screen_size[0] + self.width
        my = mouse_pos[1]

        sx = self.tileset.tile_size[0] * self.scale
        sy = self.tileset.tile_size[1] * self.scale
        mx //= sx
        my //= sy

        if 0 <= mx < self.columns:
            index = int(mx + my * self.columns)
            if 0 <= index < len(TILES):
                self.selected = index
                self.selected_pos = (mx, my)
                return

        if self.tilemap.source is not None and \
            self.save.contains_point(mouse_pos):
            self.tilemap.save()
        elif self.save_as.contains_point(mouse_pos):
            self.tilemap.saveas()
        elif self.load.contains_point(mouse_pos):
            self.tilemap.load()
        elif self.reset.contains_point(mouse_pos):
            self.tilemap.reset()
        elif self.test.contains_point(mouse_pos):
            self.tilemap.test_level()
        elif self.wrm.contains_point(mouse_pos):
            self.tilemap.resize(-1, 0, 0, 0)
        elif self.wrp.contains_point(mouse_pos):
            self.tilemap.resize(1, 0, 0, 0)
        elif self.wlm.contains_point(mouse_pos):
            self.tilemap.resize(0, 0, -1, 0)
        elif self.wlp.contains_point(mouse_pos):
            self.tilemap.resize(0, 0, 1, 0)
        elif self.hum.contains_point(mouse_pos):
            self.tilemap.resize(0, 0, 0, -1)
        elif self.hup.contains_point(mouse_pos):
            self.tilemap.resize(0, 0, 0, 1)
        elif self.hdm.contains_point(mouse_pos):
            self.tilemap.resize(0, -1, 0, 0)
        elif self.hdp.contains_point(mouse_pos):
            self.tilemap.resize(0, 1, 0, 0)

    def selected_tile(self) -> dict[str, any]:
        if self.selected == -1:
            return None
        tile = list(TILES.values())[self.selected]
        # if tile["type"] == "chain":
        #     self.tilemap.connecting = None
        return tile

    def rescale(self, scale: float):
        self.screen_size = pygame.display.get_surface().get_size()

        self.scale = self.screen_size[1] / \
                     (140 + self.tileset.tile_size[1] * self.lines)

        self.width = self.tileset.tile_size[0] * self.scale * self.columns

        self._setup_buttons()

        self.tiles = [
            pygame.transform.scale(
                self.tileset.get_original_tile(k["id"]),
                (
                    math.ceil(self.tileset.tile_size[0] * self.scale),
                    math.ceil(self.tileset.tile_size[1] * self.scale),
                )
            )
            for k in TILES.values()]

    def _setup_buttons(self):
        self.font = pygame.font.SysFont(None, int(14 * self.scale))

        btn_x = self.screen_size[0] - self.width // 2
        btn_y = self.screen_size[1]

        s = self.scale

        self.size_txt = Text(self.font, str(self.tilemap.shape)[1:-1], (255, 255, 255), 24,
                             center=(btn_x - 24.5 * s, btn_y - 18.5 * s))

        self.save = Button(self.font, 'Save', True, (255, 255, 255),
                           (78 * s, 15 * s), center=(btn_x, btn_y - 129 * s))
        self.save_as = Button(self.font, 'Save as', True, (255, 255, 255),
                              (78 * s, 15 * s), center=(btn_x, btn_y - 112 * s))
        self.load = Button(self.font, 'Load', True, (255, 255, 255),
                           (78 * s, 15 * s), center=(btn_x, btn_y - 95 * s))
        self.reset = Button(self.font, 'R', True, (255, 255, 255),
                            (30 * s, 30 * s), center=(btn_x + 24.5 * s, btn_y - 18.5 * s))

        self.test = Button(self.font, 'T', True, (255, 255, 255),
                           (30 * s, 30 * s), center=(btn_x + 24.5 * s, btn_y - (18.5 + 49.5) * s))

        self.wrm = Button(self.font, '-', True, (255, 255, 255),
                          (14 * s, 14 * s), center=(btn_x + 16 * s, btn_y - 43 * s))
        self.wrp = Button(self.font, '+', True, (255, 255, 255),
                          (16 * s, 16 * s), center=(btn_x + 32 * s, btn_y - 43 * s))
        self.wlm = Button(self.font, '-', True, (255, 255, 255),
                          (14 * s, 14 * s), center=(btn_x - 16 * s, btn_y - 43 * s))
        self.wlp = Button(self.font, '+', True, (255, 255, 255),
                          (16 * s, 16 * s), center=(btn_x - 32 * s, btn_y - 43 * s))

        self.hum = Button(self.font, '-', True, (255, 255, 255),
                          (14 * s, 14 * s), center=(btn_x, btn_y - 59 * s))
        self.hup = Button(self.font, '+', True, (255, 255, 255),
                          (16 * s, 16 * s), center=(btn_x, btn_y - 75 * s))
        self.hdm = Button(self.font, '-', True, (255, 255, 255),
                          (14 * s, 14 * s), center=(btn_x, btn_y - 27 * s))
        self.hdp = Button(self.font, '+', True, (255, 255, 255),
                          (16 * s, 16 * s), center=(btn_x, btn_y - 11 * s))

    def handle_keydown(self, key: int):
        if key not in TILE_KEYS:
            return
        ind = TILE_KEYS.index(key)
        if ind < len(TILES):
            self.selected = ind
            self.selected_pos = (
                ind % self.columns,
                ind // self.columns
            )
