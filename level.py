from interactables.player_end import PlayerEnd
from interactables.weight_end import WeightEnd
import pygame
from pygame import Surface
from pygame.locals import *
from event import Event
from interactables.slime import Slime
import time
from tileset import TileSet
from pygame import mixer

class Level:
    def __init__(self, tileset: TileSet, player, moveables, interactables, decorations, collision, loader):
        self.tileset = tileset
        self.player = player
        self.moveables = moveables
        self.interactables = interactables
        self.decorations = decorations
        self.collision = collision
        self.background = pygame.image.load('images/tent_fundo1.png')
        self.resized_bg = self.background
        self.loader = loader
        self.complete = None
        self.ends = list(filter(lambda t: type(t) is PlayerEnd or type(t) is WeightEnd, (interactables[pos] for pos in interactables)))

    def render(self, surface: Surface):
        w = int(surface.get_width() // self.tileset.scale // 4)
        h = int(surface.get_height() // self.tileset.scale // 4)

        for x in range(w):
            for y in range(h):
                surface.blit(self.resized_bg, (x * 128 * self.tileset.scale, y * 128 * self.tileset.scale))

        self.collision.render(surface)

        for dec in self.decorations:
            dec.render(surface)

        for pos in self.interactables:
            self.interactables[pos].render(surface)

        for mov in self.moveables:
            mov.render(surface)

        self.player.render(surface)

        if self.complete is not None:
            win_sound = mixer.Sound("sounds_effects/win.mp3")
            win_sound.set_volume(0.15)
            win_sound.play()
            if time.time() - self.complete > 0.5:
                self.loader.load_next_level()

    def update(self, event):
        if self.complete is not None:
            return

        updated = self.player.update(event)
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.loader.reload()
            elif event.key == K_n:
                self.loader.load_next_level()
            elif event.key == K_p:
                self.loader.load_prev_level()

        if not updated:
            return

        for mov in self.moveables:
            pos = (mov.x, mov.y)
            if pos in self.interactables:
                event = self.interactables[pos].interact(mov)
                if event is not None:
                    self.handle_event(event)
            old_pos = (mov.old_x, mov.old_y)
            if old_pos in self.interactables:
                event = self.interactables[old_pos].uninteract(mov)
                if event is not None:
                    self.handle_event(event)

    def handle_event(self, event):
        print(event)
        if event == Event.LEVEL_UNEND:
            pass
        elif event == Event.LEVEL_END:
            self.check_win()
        elif event == Event.PLAYER_DIE:
            self.player.die()
        elif event == Event.WEIGHT_DIE:
            self.player.weight_die()
        elif event == Event.BUTTON_PRESS:
            for pos in self.interactables:
                inter = self.interactables[pos]
                if type(inter) is Slime:
                    inter.toggle()
        elif event == Event.PLAYER_LOCK:
            self.player.lock()
        elif event == Event.FREEZE:
            self.player.freeze()
        elif event == Event.UNFREEZE:
            self.player.unfreeze()



    def resize_tileset(self, width, height):
        th, tw = self.collision.data.shape
        tw *= self.tileset.size[0]
        th *= self.tileset.size[1]

        scale_x = width / tw
        scale_y = height / th

        scale = min(scale_x, scale_y)

        self.tileset.resize(scale)
        self.resized_bg = pygame.transform.scale(self.background, (128 * scale, 128 * scale))

    def check_win(self):
        if all(map(lambda e: e.active, self.ends)):
            self.complete = time.time()
