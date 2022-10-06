from operator import contains
from typing import List, Tuple
import pygame
from pygame.locals import *
from book import Book
from button_menu import ButtonMenu
from loader import Loader
from pygame import mixer


class Game:
    state: str
    book: Book
    size: Tuple[int, int]
    loader: Loader
    info: pygame.display.Info
    running: bool
    screen: pygame.Surface
    joysticks: List[pygame.joystick.Joystick]

    def __init__(self, size: Tuple[int, int], loader: Loader, book: Book, state: str):
        self.joysticks = [pygame.joystick.Joystick(i)
                          for i in range(pygame.joystick.get_count())]
        # info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
        # screen_width, screen_height = info.current_w, info.current_h
        # size = (screen_width-10, screen_height-100)
        loader.resize_tileset(*size)
        book.resize(size)

        self.screen = pygame.display.set_mode(size, RESIZABLE)
        self.loader = loader
        self.running = True
        self.state = state
        self.book = book

    def run(self):
        clock = pygame.time.Clock()
        back_sound = mixer.Sound("sounds_effects/cave.mp3")
        back_sound.set_volume(0.3)
        # back_sound.play(loops=1000)

        while self.running:
            clock.tick(60)

            # Replace with background image
            self.screen.fill((51, 60, 64))

            updated = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == WINDOWRESIZED or event.type == WINDOWSIZECHANGED:
                    width, height = pygame.display.get_surface().get_size()
                    self.loader.resize_tileset(width, height)
                    self.book.resize((width, height))
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.state == "game":
                            self.state = "menu"
                        else:
                            self.running = False
                elif event.type == JOYDEVICEADDED or event.type == JOYDEVICEREMOVED:
                    pygame.joystick.init()
                    self.joysticks = [pygame.joystick.Joystick(i)
                                      for i in range(pygame.joystick.get_count())]

                if self.state == "game":
                    updated = True
                    self.loader.level.update(event)
                elif self.state == "menu":
                    pass  # TODO update Book so we can select level with keyboard/controller

            if not updated:
                self.loader.level.update(None)

            # if self.state == "video":
            #     cutscene = moviepy.editor.VideoFileClip("video/opendoor_new.mp4")
            #     curscene.preview()
            if self.state == "menu":

                self.book.render(self.screen)

                mousex, mousey = pygame.mouse.get_pos()

                for button in self.book.buttons:
                    button.render(self.screen)
                    if pygame.mouse.get_pressed()[0]:
                        if button.contains(mousex, mousey):
                            if button.on:
                                # print("on")
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
                    self.book.set_level(self.loader.current_level + 1)

            pygame.display.flip()


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
    "maps/level3.tmx",  # intro slime
    "maps/wood1.tmx",
    "maps/intromad.tmx",
    "maps/level5.tmx",
    "maps/lab2.tmx",
    "maps/level6.1.tmx",
    # "maps/level6.tmx",
    "maps/level6v2.tmx",
    "maps/level10.tmx",
    "maps/gelo-hard.tmx",
    "maps/fases_gaby/ECM.tmx",
    "maps/fases_gaby/ECM2.tmx",
    "maps/fases_mark/box_hard.tmx",
    "maps/fases_mark/box_medium.tmx",
    "maps/fases_mark/intro_caixa.tmx",
    "maps/fases_mark/hard_test.tmx",
    "maps/export.tmx",
    "maps/teste.tmx",
    "maps/fases_mark/box_new.tmx",
    "maps/fases_mark/box_test.tmx"
]

if __name__ == '__main__':
    WIDTH, HEIGHT = 800, 600

    loader = Loader(level_list, (WIDTH, HEIGHT))

    pygame.init()

    font = pygame.font.Font('./fonts/slkscr.ttf', 8)

    try:
        file = open("save.txt")
        lvl_num = int(file.readlines()[0].strip())
        file.close()
    except:
        lvl_num = 0

    book = Book("images/book.png", 10, (WIDTH, HEIGHT),
                level_list, lvl_num, font)

    game = Game((WIDTH, HEIGHT), loader, book, "menu")
    game.run()
