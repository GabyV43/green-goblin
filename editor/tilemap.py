import csv

from typing import Any
from loader import Loader
from io import StringIO
import os
from tkinter import filedialog, messagebox
import numpy
import pygame
from .scalable import Scalable
from .tiles import TILES
from .renderable import Renderable
from .tileset import TileSet
from xml.etree import ElementTree as ET
from dataclasses import dataclass


WANG_ORDER = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
]

PLAYER_IDS = [30]
WEIGHT_IDS = [148]
MOVABLES_IDS = [146]
INTERACTABLES_IDS = [204, 206, 208, 262, 263, 378, 408, 523, 581, 553]
SLIME_IDS = [527, 556, 585, 470, 471, 472, 529, 558, 587, 562, 563, 564]
SLIME_IN_IDS = [266, 267, 268, 323, 352, 381, 325, 354, 383, 358, 359, 360]

@dataclass
class Conn:
    fr: tuple[int, int]
    to: tuple[int, int]
    dist: int

class TileMap(Renderable, Scalable):
    source: str | None
    tileset: TileSet
    ground: numpy.ndarray
    interactables: dict[tuple[int, int], int]
    movables: dict[tuple[int, int], int]
    connections: list[Conn]
    shape: tuple[int, int]
    player: tuple[int, int] | None
    weight: tuple[int, int] | None
    screen: Any
    border: pygame.rect.Rect
    # We call it wang_ground because we'll have wang_slime too
    wang_ground: dict[str, int]
    # wang_slime: dict[str, int]

    def __init__(self, tileset: TileSet, matrix: numpy.ndarray, screen: Any, init: bool = True, source: str | None = None):
        self.source = source
        self.tileset = tileset
        self.ground = matrix
        self.screen = screen
        self.shape = self.ground.shape

        self.border = pygame.Rect(
            0,
            0,
            self.shape[0] * self.tileset.tile_size[0] * self.tileset.scale,
            self.shape[1] * self.tileset.tile_size[1] * self.tileset.scale
        ).inflate(4, 4)

        self.interactables = {}
        self.movables = {}
        self.connections = []

        self.player = None
        self.weight = None

        tree = ET.parse(tileset.file)
        root = tree.getroot()
        wangset = root[-1]
        assert wangset.tag == "wangsets"
        assert wangset[0].attrib["name"] == "Walls"

        self.wang_ground = {}

        for wtile in wangset[0][1:]:
            wid = wtile.attrib["wangid"].replace(",", "")
            tid = int(wtile.attrib["tileid"])

            self.wang_ground[wid] = tid

            code = wtile.attrib["wangid"].split(",")
            # U _ R _ D _ L _
            # 0 1 2 3 4 5 6 7
            #            -2-1
            indexes = []
            for x in range(-2, 5, 2):  # -2, 0, 2, 4
                y = x + 2
                z = x + 1
                if int(code[x]) + int(code[y]) < 2:
                    if z < 0:
                        z += 8
                    indexes.append(z)

            for i in range(0, 2 ** len(indexes)):
                pcode = list(bin(i)[2:])
                pcode = ['0'] * (len(indexes) - len(pcode)) + pcode

                new_code = []
                for i, c in enumerate(code):
                    if i in indexes:
                        new_code.append(pcode[indexes.index(i)])
                    else:
                        new_code.append(c)

                self.wang_ground[''.join(new_code)] = tid

        print("wang_tiles: ", len(self.wang_ground))

        if init:
            matrix.fill(-1)
            self._set_border()

    def render(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        scale = self.tileset.scale
        tw, th = self.tileset.tile_size
        w, h = self.ground.shape

        # draw ground
        for y in range(h):
            for x in range(w):
                tile = self.get((x, y))
                if tile == -1:
                    continue
                img = self.tileset.get_tile(tile)
                surface.blit(
                    img,
                    (
                        x * tw * scale + offset[0],
                        y * th * scale + offset[1],
                    )
                )

        # draw interactables
        for pos in self.interactables:
            inter = self.interactables[pos]

            surface.blit(self.tileset.get_tile(inter), (
                pos[0] * tw * scale + offset[0],
                pos[1] * th * scale + offset[1],
            ))

        # draw moveables
        for pos in self.movables:
            mov = self.movables[pos]

            surface.blit(self.tileset.get_tile(mov), (
                pos[0] * tw * scale + offset[0],
                pos[1] * th * scale + offset[1],
            ))

        # draw player and weight
        if self.weight is not None:
            surface.blit(self.tileset.get_tile(TILES["weight"]["id"]), (
                self.weight[0] * tw * scale + offset[0],
                self.weight[1] * th * scale + offset[1],
            ))

        if self.player is not None:
            surface.blit(self.tileset.get_tile(TILES["player"]["id"]), (
                self.player[0] * tw * scale + offset[0],
                self.player[1] * th * scale + offset[1],
            ))

        pygame.draw.rect(surface, (90, 90, 90), self.border, 2)

    def rescale(self, scale: float):
        self.border = pygame.Rect(
            0,
            0,
            self.shape[0] * self.tileset.tile_size[0] * scale,
            self.shape[1] * self.tileset.tile_size[1] * scale
        ).inflate(4, 4)

    def set_ground(self, pos: tuple[int, int], sound: pygame.mixer.Sound | None = None, recurse: bool = True):
        if not (0 <= pos[0] < self.shape[0]) or not (0 <= pos[1] < self.shape[1]):
            return
        # Get neighbors configuration (1 byte)
        config = []
        for ord in WANG_ORDER:
            x = pos[0] + ord[0]
            y = pos[1] + ord[1]
            if x < 0 or x >= self.shape[0] or y < 0 or y >= self.shape[1]:
                config.append('1')
            else:
                config.append('1' if self.ground[x, y] != -1 else '0')

        # Retrieve adequate tile id
        code = ''.join(config)
        id = self.wang_ground.get(code, 313)
        if code not in self.wang_ground:
            id = 313
        self.set(pos, id, sound=sound)

        # Notify neighbors of the change
        if not recurse:
            return False

        for ord in WANG_ORDER:
            x = ord[0] + pos[0]
            y = ord[1] + pos[1]
            if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
                if self.ground[x, y] != -1:
                    self.set_ground((x, y), recurse=False)

    def remove_ground(self, pos: tuple[int, int]):
        if not (0 <= pos[0] < self.shape[0]) or not (0 <= pos[1] < self.shape[1]):
            return

        self.ground[pos[0], pos[1]] = -1

        for ord in WANG_ORDER:
            x = ord[0] + pos[0]
            y = ord[1] + pos[1]
            if 0 <= x < self.shape[0] and 0 <= y < self.shape[1]:
                if self.get((x, y)) != -1:
                    self.set_ground((x, y), recurse=False)

    def set(self, pos: tuple[int, int], val: int, sound: pygame.mixer.Sound | None = None):
        if not (0 <= pos[0] < self.shape[0]) or not (0 <= pos[1] < self.shape[1]):
            return
        if self.ground[pos[0], pos[1]] == -1 and sound is not None:
            sound.play()
        self.ground[pos[0], pos[1]] = val
        if self.player == pos:
            self.player = None
        if self.weight == pos:
            self.weight = None
        if pos in self.interactables:
            del self.interactables[pos]
        if pos in self.movables:
            del self.movables[pos]

    def get(self, pos: tuple[int, int]) -> int | None:
        if not (0 <= pos[0] < self.shape[0]) or not (0 <= pos[1] < self.shape[1]):
            return
        return self.ground[pos[0], pos[1]]

    def set_player(self, pos: tuple[int, int], sound: pygame.mixer.Sound | None = None):
        if self.get(pos) != -1:
            return
        self.player = pos
        if pos in self.movables:
            del self.movables[pos]

    def set_weight(self, pos: tuple[int, int], sound: pygame.mixer.Sound | None = None):
        if self.get(pos) != -1:
            return
        self.weight = pos
        if pos in self.movables:
            del self.movables[pos]

    def set_movable(self, pos: tuple[int, int], id: int, sound: pygame.mixer.Sound | None = None):
        if self.get(pos) != -1:
            return
        self.movables[pos] = id
        if self.player == pos:
            self.player = None
        if self.weight == pos:
            self.weight = None

    def set_interactable(self, pos: tuple[int, int], id: int, sound: pygame.mixer.Sound | None = None):
        if self.get(pos) != -1:
            return
        self.interactables[pos] = id

    def set_slime(self, pos: tuple[int, int], active: bool, sound: pygame.mixer.Sound | None = None):
        if self.get(pos) != -1:
            return
        # TODO make slimes intelligent
        self.interactables[pos] = 527 if active else 266

    def remove(self, pos: tuple[int, int], selected: int):
        if selected == -1:
            if self.player == pos:
                self.player = None
            if self.weight == pos:
                self.weight = None
            if pos in self.movables:
                del self.movables[pos]
            if pos in self.interactables:
                del self.interactables[pos]
            self.remove_ground(pos)
        else:
            type = list(TILES.keys())[selected]
            if type == "ground":
                self.remove_ground(pos)
            elif type == "player":
                if self.player == pos:
                    self.player = None
            elif type == "weight":
                if self.weight == pos:
                    self.weight = None
            else:
                tile = TILES[type]
                dic = self.movables if tile["type"] == "movable" else self.interactables
                if pos in dic and dic[pos] == TILES[type]["id"]:
                    del dic[pos]

    def _ground_to_csv(self) -> str:
        csv = ""
        for y in range(self.shape[1]):
            if y > 0:
                csv += '\n'
            for x in range(self.shape[0]):
                if x > 0:
                    csv += ','
                val = self.get((x, y)) or -1
                csv += str(val + 1)
        return csv

    def _movables_to_csv(self) -> str:
        csv = ""
        for y in range(self.shape[1]):
            if y > 0:
                csv += '\n'
            for x in range(self.shape[0]):
                if x > 0:
                    csv += ','
                if (x, y) in self.movables:
                    csv += str(self.movables[(x, y)] + 1)
                elif (x, y) == self.player:
                    csv += str(TILES["player"]["id"] + 1)
                elif (x, y) == self.weight:
                    csv += str(TILES["weight"]["id"] + 1)
                else:
                    csv += '0'
        return csv

    def _interactables_to_csv(self) -> str:
        csv = ""
        for y in range(self.shape[1]):
            if y > 0:
                csv += '\n'
            for x in range(self.shape[0]):
                if x > 0:
                    csv += ','
                if (x, y) in self.interactables:
                    csv += str(self.interactables[(x, y)] + 1)
                else:
                    csv += '0'
        return csv

    def to_xml(self, location: str) -> bytes:
        map = ET.Element("map")
        map.attrib["version"] = "1.8"
        map.attrib["tiledversion"] = "1.8.4"
        map.attrib["orientation"] = "orthogonal"
        map.attrib["renderorder"] = "right-down"
        map.attrib["width"] = str(self.shape[0])
        map.attrib["height"] = str(self.shape[1])
        map.attrib["tilewidth"] = "32"
        map.attrib["tileheight"] = "32"
        map.attrib["infinite"] = "0"
        map.attrib["nextlayerid"] = "5"
        map.attrib["nextobjectid"] = "1"

        tileset = ET.SubElement(map, "tileset")
        tileset.attrib["firstgid"] = "1"
        tileset.attrib["source"] = os.path.relpath(
            self.tileset.file,
            os.path.dirname(location)
        )

        connections = ET.SubElement(map, "connections")
        for con in self.connections:
            conn = ET.SubElement(connections, "conn")
            conn.attrib["from"] = f"{con.fr[0]},{con.fr[1]}"
            conn.attrib["to"] = f"{con.to[0]},{con.to[1]}"
            conn.attrib["distance"] = str(con.dist)

        ground = ET.SubElement(map, "layer")
        ground.attrib["id"] = "1"
        ground.attrib["name"] = "collision"
        ground.attrib["width"] = str(self.shape[0])
        ground.attrib["height"] = str(self.shape[1])

        ground_data = ET.SubElement(ground, "data")
        ground_data.attrib["encoding"] = "csv"
        ground_data.text = self._ground_to_csv()

        inter = ET.SubElement(map, "layer")
        inter.attrib["id"] = "3"
        inter.attrib["name"] = "obj1"
        inter.attrib["width"] = str(self.shape[0])
        inter.attrib["height"] = str(self.shape[1])

        inter_data = ET.SubElement(inter, "data")
        inter_data.attrib["encoding"] = "csv"
        inter_data.text = self._interactables_to_csv()

        movab = ET.SubElement(map, "layer")
        movab.attrib["id"] = "4"
        movab.attrib["name"] = "obj2"
        movab.attrib["width"] = str(self.shape[0])
        movab.attrib["height"] = str(self.shape[1])

        movab_data = ET.SubElement(movab, "data")
        movab_data.attrib["encoding"] = "csv"
        movab_data.text = self._movables_to_csv()

        ET.indent(map)
        return ET.tostring(map, encoding='utf8', method='xml')

    def from_xml(self, source: str):
        self.source = source
        tree = ET.parse(source)
        root = tree.getroot()
        self.movables = {}
        self.interactables = {}
        self.connections = []
        begin = 1
        if root[1].tag == 'connections':
            begin = 2

        self.ground = self.load_layer(root[begin])

        for layer in root[begin:-1]:
            if layer.attrib["name"][:3].lower() == "obj":
                self.load_objects(layer)
            else:
                ...  # We're ignoring decorations for now
        self.load_objects(root[-1])

        if root[1].tag == 'connections':
            self.load_connections(root[1])

        self.shape = self.ground.shape

        self.screen.rescale(-1)

        self._set_border()

    def load_layer(self, layer: ET.Element) -> numpy.ndarray:
        data = layer[0]
        assert data.tag == "data"
        assert data.attrib["encoding"] == "csv"

        sio = StringIO((data.text or '').strip().replace(',\n', '\n'))
        return numpy.array(list(csv.reader(sio)), dtype=int).T - 1

    def load_objects(self, layer: ET.Element):
        data = layer[0]
        assert data.tag == 'data'

        assert data.attrib["encoding"] == 'csv'

        sio = StringIO((data.text or '').strip().replace(',\n', '\n'))
        matrix = numpy.array(list(csv.reader(sio)), dtype=int)

        for iy, ix in numpy.ndindex(matrix.shape):
            pos = (ix, iy)
            id = matrix[iy, ix] - 1
            if id in PLAYER_IDS:
                self.player = pos
            elif id in WEIGHT_IDS:
                self.weight = pos
            elif id in MOVABLES_IDS:
                self.movables[pos] = id
            elif id in INTERACTABLES_IDS:
                self.interactables[pos] = id
            elif id in SLIME_IDS:
                self.interactables[pos] = TILES["slime"]["id"]
            elif id in SLIME_IN_IDS:
                self.interactables[pos] = TILES["slimeInverted"]["id"]
            elif id == -1:
                pass  # In this case there is nothing there
            else:
                raise Exception(f"Unkown id {id}")

    def load_connections(self, layer: ET.Element):
        for con in layer:
            assert con.tag == 'conn'
            conn = Conn(
                tuple(map(int, con.attrib["from"].split(','))),
                tuple(map(int, con.attrib["to"].split(','))),
                int(con.attrib["distance"]),
            )
            self.connections.append(conn)

    def resize(self, right: int, bottom: int, left: int, top: int):
        assert abs(right + bottom + left + top) == 1

        if right == 1:
            self.ground = numpy.r_[
                self.ground, -numpy.ones((1, self.shape[1]), dtype=int)]
        elif right == -1:
            if self.shape[0] > 1:
                self.ground = self.ground[:-1, :]
        elif bottom == 1:
            self.ground = numpy.c_[
                self.ground, -numpy.ones((self.shape[0], 1), dtype=int)]
        elif bottom == -1:
            if self.shape[1] > 1:
                self.ground = self.ground[:, :-1]
        elif left == 1:
            self.ground = numpy.r_[
                -numpy.ones((1, self.shape[1]), dtype=int), self.ground]
        elif left == -1:
            if self.shape[0] > 1:
                self.ground = self.ground[1:, :]
        elif top == 1:
            self.ground = numpy.c_[
                -numpy.ones((self.shape[0], 1), dtype=int), self.ground]
        elif top == -1:
            if self.shape[1] > 1:
                self.ground = self.ground[:, 1:]

        self._move_all(left, top)
        self.shape = self.ground.shape
        self._set_border()
        self.screen.rescale(-1)
        self.border = pygame.Rect(
            0,
            0,
            self.shape[0] * self.tileset.tile_size[0] * self.tileset.scale,
            self.shape[1] * self.tileset.tile_size[1] * self.tileset.scale
        ).inflate(4, 4)

    def _set_border(self):
        x = y = 0
        for x in range(1, self.shape[0]):
            self.set_ground((x, y))
        for y in range(1, self.shape[1]):
            self.set_ground((x, y))
        for x in range(self.shape[0] - 2, -1, -1):
            self.set_ground((x, y))
        for y in range(self.shape[1] - 2, -1, -1):
            self.set_ground((x, y))

    def _move_all(self, dx: int, dy: int):
        if dx == 0 and dy == 0:
            return
        if self.player is not None:
            self.player = (self.player[0] + dx, self.player[1] + dy)
        if self.weight is not None:
            self.weight = (self.weight[0] + dx, self.weight[1] + dy)

        new_movables = {}
        new_inters = {}

        for pos in self.movables:
            new_pos = (pos[0] + dx, pos[1] + dy)
            new_movables[new_pos] = self.movables[pos]
        for pos in self.interactables:
            new_pos = (pos[0] + dx, pos[1] + dy)
            new_inters[new_pos] = self.interactables[pos]
        for con in self.connections:
            new_fr = (con.fr[0] + dx, con.fr[1] + dy)
            new_to = (con.to[0] + dx, con.to[1] + dy)
            con.fr = new_fr
            con.to = new_to

        self.movables = new_movables
        self.interactables = new_inters

    def reset(self):
        self.movables.clear()
        self.interactables.clear()
        self.player = self.weight = None
        self.ground.fill(-1)
        self._set_border()

    def save(self):
        filename = self.source or ''
        xml = self.to_xml(filename)
        with open(filename, 'w') as f:
            f.write(xml.decode())

    def saveas(self, filename: str | None = None):
        if filename is None:
            filename = filedialog.asksaveasfilename(
                filetypes=[("Tiled TileMap Xml", "*.tmx")],
                defaultextension=".tmx",
            )
        if filename != '':
            xml = self.to_xml(filename)
            with open(filename, 'w') as f:
                f.write(xml.decode())
            self.source = filename
            pygame.display.set_caption(f'Green Goblin Editor - {filename}')

    def load(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Tiled TileMap Xml", "*.tmx")],
            defaultextension=".tmx",
        )
        if filename != '':
            self.from_xml(filename)
            pygame.display.set_caption(f'Green Goblin Editor - {filename}')

    def test_level(self):
        # Check if there's a player and weight
        if self.player is None:
            messagebox.showerror(
                "No Player found", "You must add a Player before testing your level")
            return
        elif self.weight is None:
            messagebox.showerror(
                "No Weight found", "You must add a Weight before testing your level")
            return

        # First save the file
        lvl_name = os.path.normpath('./maps/tmp.tmx')
        self.saveas(lvl_name)

        # Now create a Level entity
        loader = Loader([lvl_name], self.screen.screen_size,
                        on_all_finished_handler=lambda: self.screen.finish_test())
        self.screen.loader = loader
