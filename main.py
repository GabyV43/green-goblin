from operator import contains
import pygame
from pygame.locals import *
from book import Book
from button_menu import ButtonMenu
from loader import Loader
from pygame import mixer


class Game:
    def __init__(self, size, loader, state):
        pygame.init()
        self.screen = pygame.display.set_mode(size, RESIZABLE)
        self.loader = loader
        self.running = True
        self.state = state

    def run(self):
        clock = pygame.time.Clock()
        back_sound = mixer.Sound("sounds_effects/cave.mp3")
        back_sound.set_volume(0.3)
        # back_sound.play(loops=1000)

        while self.running:
            clock.tick(60)

            # Replace with background image
            self.screen.fill((51, 60, 64))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == WINDOWRESIZED or event.type == WINDOWSIZECHANGED:
                    width, height = pygame.display.get_surface().get_size()
                    self.loader.resize_tileset(width, height)
                    book.resize((width, height))
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.state = "menu"
                self.loader.level.update(event)

            if self.state == "menu":

                book.render(self.screen)

                mousex, mousey = pygame.mouse.get_pos()

                for button in book.buttons:
                    button.render(self.screen)
                    if pygame.mouse.get_pressed()[0]:
                        if button.contains(mousex, mousey):
                            if button.on:
                                print("on")
                                self.loader.load_level_number(
                                    button.number - 1)
                                self.state = "game"
                    if pygame.mouse.get_pressed()[1]:
                        if button.contains(mousex, mousey):
                            self.loader.load_level_number(
                                button.number - 1)
                            self.state = "game"

            elif self.state == "game":
                self.loader.level.render(self.screen)

                if self.loader.level.level_completed:
                    book.set_level(self.loader.current_level + 1)

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
    "maps/level3.tmx",  # trocar essa fase pelo amor de deus
    "maps/wood1.tmx",
    "maps/intromad.tmx",
    "maps/level5.tmx",
    "maps/lab2.tmx",
    "maps/level6.1.tmx",
    # "maps/level6.tmx",
    "maps/level6v2.tmx",
    "maps/level10.tmx",
    "maps/gelo-hard.tmx",
]
loader = Loader(level_list, (WIDTH, HEIGHT))

game = Game((WIDTH, HEIGHT), loader, "menu")

font = pygame.font.Font('./fonts/slkscr.ttf', 8)

try:
    file = open("save.txt")
    lvl_num = int(file.readlines()[0].strip())
    file.close()
except:
    lvl_num = 0

book = Book("images/book.png", 10, (WIDTH, HEIGHT), level_list, lvl_num, font)

game.run()
