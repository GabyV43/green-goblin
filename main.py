import pygame
from pygame.locals import *
from levelloader import LevelLoader
from player import Player
from tileset import TileSet
from tilemap import TileMap
from box import Box

class Game:
    def __init__(self, size, renderables, updatables):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        self.renderables = renderables
        self.updatables = updatables
        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)

            # Replace with background image
            self.screen.fill((50, 50, 50))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == WINDOWRESIZED or event.type == WINDOWSIZECHANGED:
                    width, height = pygame.display.get_surface().get_size()
                    resize_tileset(width, height)
                else:
                    for up in self.updatables:
                        up.update(event)

            for r in self.renderables:
                r.render(self.screen)

            pygame.display.flip()


tileset = TileSet('tileset/TilesetV_2.png', (32, 32), 0, 0, 1)

tilemap1 = TileMap('maps/level1_Tile Layer 1.csv', tileset)
tilemap2 = TileMap('maps/level1_Cristais.csv', tileset)

collision = tilemap1.data != -1
moveables = []

weight = Box(8, 2, tileset, 509, moveables, collision)
player = Player(tileset, 178, 5, 2, moveables, collision, weight)

moveables.append(weight)
moveables.append(player)

def resize_tileset(width, height):
    th, tw = tilemap1.data.shape
    tw *= tileset.size[0]
    th *= tileset.size[1]

    scale_x = width / tw
    scale_y = height / th

    scale = min(scale_x, scale_y)

    tileset.resize(scale)


WIDTH = 800
HEIGHT = 800
resize_tileset(WIDTH, HEIGHT)

game = Game((WIDTH, HEIGHT), [tilemap1, tilemap2, *moveables], [player])
game.run()
