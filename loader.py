import xml.etree.ElementTree as ET
from io import StringIO
import numpy as np
import csv
from interactables.box_end import BoxEnd
from interactables.button import Button
from interactables.fire import Fire
from interactables.heavy_button import HeavyButton
from interactables.hole import Hole
from interactables.ice import Ice
from interactables.player_end import PlayerEnd
from interactables.slime import Slime
from interactables.spike import Spike
from interactables.weight_end import WeightEnd
from interactables.wood import Wood
from level import Level
from objects.box import Box
from tilemap import TileMap
from tileset import TileSet

from objects.player import Player
from objects.weight import Weight

import os

PLAYER_ID = 30
BOX_ID = 146
WEIGHT_ID = 148
WOOD_ID = 204
HOLE_ID = 206
SPIKE_ID = 208
BUTTON_ID = 262
HEAVY_BUTTON_ID = 263
ICE_ID = 378
FIRE_ID = 408
WEIGHT_END_ID = 523
PLAYER_END_ID = 581
BOX_END_ID = 553
SLIME_IDS = [527, 556, 585, 470, 471, 472, 529, 558, 587, 562, 563, 564]
SLIME_IN_IDS = [266, 267, 268, 323, 352, 381, 325, 354, 383, 358, 359, 360]


class Loader():
    def __init__(self, level_list, screen_size, current_level=0):
        self.tileset = None
        self.screen_size = screen_size
        self.level_list = level_list
        self.current_level = current_level
        self.load_level(level_list[current_level])

    def load_tileset(self, file, tw, th, scale):
        if self.tileset is not None and self.tileset.file == file:
            return

        path = os.path.join('maps', file)
        tree = ET.parse(path)
        root = tree.getroot()
        image = root[0]
        if image.tag != 'image':
            raise Exception("Invalid tileset")
        img_source = image.attrib['source']

        path = os.path.join(os.path.dirname(path), img_source)
        if not os.path.exists(path):
            raise Exception("Couldn't find tileset image")

        self.tileset = TileSet(path, [tw, th], 0, 0, scale)

    def load_layer(self, layer: ET.Element):
        data = layer[0]
        if data.tag != 'data':
            raise Exception("Invalid layer data")

        encoding = data.attrib["encoding"]
        if encoding == "csv":
            sio = StringIO(data.text.strip().replace(',\n', '\n'))
            matrix = np.array(list(csv.reader(sio)), dtype=int) - 1
            return TileMap(self.tileset, matrix)
        else:
            raise Exception("Invalid encoding:", encoding)

    def load_objects(self, objects):
        data = objects[0]
        if data.tag != 'data':
            raise Exception("Invalid layer data")

        encoding = data.attrib["encoding"]
        self.player = self.weight = None
        if encoding == "csv":
            sio = StringIO(data.text.strip().replace(',\n', '\n'))
            matrix = np.array(list(csv.reader(sio)), dtype=int)

            self.moveables = []
            self.interactables = {}

            is_wall = self.collision.data != -1

            for iy, ix in np.ndindex(matrix.shape):
                obj = inter = None

                id = matrix[iy, ix] - 1
                if id == PLAYER_ID:
                    self.player = obj = Player(
                        self.tileset, ix, iy, self.moveables, is_wall, None)
                elif id == WEIGHT_ID:
                    self.weight = obj = Weight(
                        ix, iy, self.tileset, self.moveables, is_wall)
                elif id == BOX_ID:
                    obj = Box(ix, iy, self.tileset, self.moveables, is_wall)
                elif id == WOOD_ID:
                    inter = Wood(ix, iy, self.tileset)
                elif id == SPIKE_ID:
                    inter = Spike(ix, iy, self.tileset)
                elif id == HOLE_ID:
                    inter = Hole(ix, iy, self.tileset)
                elif id == BUTTON_ID:
                    inter = Button(ix, iy, self.tileset)
                elif id == HEAVY_BUTTON_ID:
                    inter = HeavyButton(ix, iy, self.tileset)
                elif id == ICE_ID:
                    inter = Ice(ix, iy, self.tileset)
                elif id == FIRE_ID:
                    inter = Fire(ix, iy, self.tileset)
                elif id == WEIGHT_END_ID:
                    inter = WeightEnd(ix, iy, self.tileset)
                elif id == PLAYER_END_ID:
                    inter = PlayerEnd(ix, iy, self.tileset)
                elif id == BOX_END_ID:
                    inter = BoxEnd(ix, iy, self.tileset)
                elif id in SLIME_IDS:
                    inter = Slime(ix, iy, self.tileset, id, True)
                elif id in SLIME_IN_IDS:
                    inter = Slime(ix, iy, self.tileset, id + 204, False)
                elif id == -1:
                    pass  # In this case there is nothing there
                else:
                    raise Exception(f"Unkown id {id}")

                if obj is not None:
                    self.moveables.append(obj)
                elif inter is not None:
                    self.interactables[ix, iy] = inter

            if self.player is None:
                raise Exception("No player found")
            if self.weight is None:
                raise Exception("No weight found")
            self.player.weight = self.weight
        else:
            raise Exception("Invalid encoding:", encoding)

    def load_level(self, name):
        print(name)
        tree = ET.parse(name)

        root = tree.getroot()

        if root.tag != 'map':
            raise Exception(
                "Level file is configured incorrectly, please load a proper .tmx file")

        self.order = root.attrib["renderorder"]

        tileset_el = root[0]
        tw, th = int(root.attrib["tilewidth"]), int(root.attrib["tileheight"])
        w, h = int(root.attrib["width"]), int(root.attrib["height"])
        sx, sy = self.screen_size[0] / (tw * w), self.screen_size[1] / (th * h)
        self.load_tileset(tileset_el.attrib["source"], tw, th, min(sx, sy))

        self.collision = self.load_layer(root[1])

        self.decorations = [self.load_layer(r) for r in root[2:-1]]

        self.objects = self.load_objects(root[-1])

        # build level object

        self.level = Level(
            self.tileset,
            self.player,
            self.moveables,
            self.interactables,
            self.decorations,
            self.collision,
            self,
            os.path.split(name)[-1]
        )

        self.level.resize_tileset(self.screen_size[0], self.screen_size[1])

        return self.level

    def load_level_number(self, number):
        self.current_level = number
        self.reload()

    def reload(self):
        level_name = self.level_list[self.current_level]
        self.load_level(level_name)

    def load_next_level(self):
        self.current_level += 1
        self.reload()

    def load_prev_level(self):
        self.current_level -= 1
        self.reload()

    def resize_tileset(self, width, height):
        self.screen_size = [width, height]
        self.level.resize_tileset(width, height)
