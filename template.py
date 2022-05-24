import pygame
from pygame.locals import *
import numpy as np
import csv
import math

file = 'images/cave-tileset2.png'

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

class Game:
    renders = []

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Pygame Tiled Demo")
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_l:
                        self.load_image(file)
                    elif event.key == K_DOWN or event.key == K_s:
                        player.move((0, 1))
                    elif event.key == K_UP or event.key == K_w:
                        player.move((0, -1))
                    elif event.key == K_LEFT or event.key == K_a:
                        player.move((-1, 0))
                    elif event.key == K_RIGHT or event.key == K_d:
                        player.move((1, 0))

                elif event.type == WINDOWRESIZED or event.type == WINDOWSIZECHANGED:
                    w, h = pygame.display.get_surface().get_size()
                    mw, mh = (10 * 16, 10 * 16)
                    needed_scale = math.floor(min(w / mw, h / mh))
                    ts.resize(needed_scale)
                    tm.resize()
                    player.resize()

            for r in self.renders:
                r.render()

            self.screen.blit(r.image, (0, 0))

            pygame.display.flip()

        pygame.quit()

    def load_image(self, file):
        self.file = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()

        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')
        self.screen.blit(self.image, self.rect)
        pygame.display.update()

class Tileset:
    def __init__(self, file, size=(16, 16), margin=0, spacing=0, scale=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.orig_tiles = []
        self.tiles = []
        self.load()
        self.resize(scale)

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))

                self.orig_tiles.append(tile)
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'

    def resize(self, scale=1):
        self.scale = scale
        for i, tile in enumerate(self.orig_tiles):
            self.tiles[i] = pygame.transform.scale(tile, (self.size[0] * scale, self.size[1] * scale))


class Tilemap:
    def __init__(self, tileset, map, size=(10, 20), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = map

        w, h = self.size
        tw, th = self.tileset.size
        scale = self.tileset.scale
        self.image = pygame.Surface((tw * w * scale, th * h * scale), SRCALPHA)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                if self.map[i, j] != -1:
                    tile = self.tileset.tiles[self.map[i, j]]
                    self.image.blit(tile, (j*self.tileset.size[0]*self.tileset.scale, i*self.tileset.size[1]*self.tileset.scale))

    def resize(self):
        w, h = self.size
        tw, th = self.tileset.size
        scale = self.tileset.scale
        self.image = pygame.Surface((tw * w * scale, th * h * scale))

    # def distance(self, a, b):

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

class Player:
    def __init__(self, pos, weight_pos, tilemap):
        self.pos = list(pos)
        self.weight_pos = list(weight_pos)

        self.orig_player_img = pygame.image.load(open('images/goblin_pixel.png'))
        self.orig_weight_img = pygame.image.load(open('images/weight.png'))

        self.tilemap = tilemap

        self.resize()

    def render(self):
        image = self.tilemap.image
        image.blit(self.player_img, (self.pos[0] * self.tilemap.tileset.size[0] * self.tilemap.tileset.scale, self.pos[1] * self.tilemap.tileset.size[1] * self.tilemap.tileset.scale))
        image.blit(self.weight_img, (self.weight_pos[0] * self.tilemap.tileset.size[0] * self.tilemap.tileset.scale, self.weight_pos[1] * self.tilemap.tileset.size[1] * self.tilemap.tileset.scale))

    def resize(self):
        scale = self.tilemap.tileset.scale
        tsize = self.tilemap.tileset.size
        self.player_img = pygame.transform.scale(self.orig_player_img, (scale * tsize[0], scale * tsize[1]))
        self.weight_img = pygame.transform.scale(self.orig_weight_img, (scale * tsize[0], scale * tsize[1]))

    def move(self, dir):
        new_x = self.pos[0] + dir[0]
        new_y = self.pos[1] + dir[1]

        dx = new_x - self.weight_pos[0]
        dy = new_y - self.weight_pos[1]

        # dist = abs(dx) + abs(dy)
        dist = self.tilemap.distance((new_x, new_y), self.weight_pos)

        if dist > 3:
            if dx == 0 or dy == 0:
                self.weight_pos[0] += sign(dx)
                self.weight_pos[1] += sign(dy)
                self.pos[0] = new_x
                self.pos[1] = new_y
        else:
            self.pos[0] = new_x
            self.pos[1] = new_y





with open('maps/level1.csv') as f:
    data = np.array(list(csv.reader(f)), dtype=int)


total_size = (10 * 16, 10 * 16)
window_size = (640, 640)
needed_scale = min([w / s for w, s in zip(window_size, total_size)])

ts = Tileset(open('images/cave-tileset2.png'), size=(16, 16), scale=needed_scale)
tm = Tilemap(ts, data, size=(10, 10))

player = Player((8, 1), (8, 2), tm)

game = Game(window_size)
game.renders.append(player)
game.renders.append(tm)
game.run()
