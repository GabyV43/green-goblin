import pygame
from pygame.locals import *
from player import Player
from tileset import TileSet
from tilemap import TileMap

class Game:
    def __init__(self, size, renderables):
        pygame.init()
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.renderables = renderables
        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)

            # Replace with background image
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    k = event.key
                    if k == K_w or k == K_UP:
                        player.move(0, -1)
                    elif k == K_s or k == K_DOWN:
                        player.move(0, 1)
                    elif k == K_a or k == K_LEFT:
                        player.move(-1, 0)
                    elif k == K_d or k == K_RIGHT:
                        player.move(1, 0)

            for r in self.renderables:
                r.render(self.screen)

            # self.screen.blit(self.p, (0, 0))

            pygame.display.flip()

#549

tileset = TileSet('tileset/TilesetV_2.png', (32, 32), 0, 0, 1)

tilemap1 = TileMap('maps/level1_Tile Layer 1.csv', tileset)
tilemap2 = TileMap('maps/level1_Cristais.csv', tileset)

player = Player(tileset, 594, 5, 2)

game = Game((640, 480), [tilemap1, tilemap2, player])
game.run()

# Teach Gabyy how to use Git
