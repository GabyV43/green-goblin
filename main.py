import pygame
from pygame.locals import *
from loader import Loader

class Game:
    def __init__(self, size, loader):
        pygame.init()
        self.screen = pygame.display.set_mode(size, RESIZABLE)
        self.loader = loader
        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)

            #Replace with background image
            self.screen.fill((50, 50, 50))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == WINDOWRESIZED or event.type == WINDOWSIZECHANGED:
                    width, height = pygame.display.get_surface().get_size()
                    self.loader.resize_tileset(width, height)
                else:
                    self.loader.level.update(event)

            self.loader.level.render(self.screen)

            pygame.display.flip()



WIDTH = 640
HEIGHT = 640

""" TODO
- 2 fases int. gelo OK
- 1 fase int. fogo OK
- 2 fases madeira
- 2 fases espinhos
"""

level_list = [
    "maps/tutorial1.tmx",
    "maps/tutorial2.tmx",
    "maps/tutorial6.tmx",
    "maps/tutorial4.tmx",
    "maps/tutorial5.tmx",
    "maps/tutorial3.tmx",
    "maps/intro2finais.tmx",
    "maps/level1.tmx",
    "maps/level2.tmx",
    "maps/intfinalbox.tmx",
    "maps/introcaixa.tmx",
    "maps/level4.tmx",
    "maps/gelo1.tmx",
    "maps/gelo2.tmx",
    "maps/fogo1.tmx",
    "maps/level2.5.tmx",
    # 1~2 fases de slime
    "maps/level3.tmx", # trocar essa fase pelo amor de deus
    "maps/wood1.tmx",
    "maps/intromad.tmx",
    "maps/level5.tmx",
    "maps/lab2.tmx",
    "maps/level6.1.tmx",
    # "maps/level6.tmx",
    "maps/level6v2.tmx",
    "maps/level10.tmx",
]
loader = Loader(level_list, (WIDTH, HEIGHT))

game = Game((WIDTH, HEIGHT), loader)
game.run()

