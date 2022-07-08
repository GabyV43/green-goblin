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
from math import ceil

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
        self.button_pressed = False
        self.history = []

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

        general_state = (
            self.get_state(),
            [m.get_state() for m in self.moveables],
            [i.get_state() for i in self.interactables.values()]
        )

        updated = self.player.update(event)
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.loader.reload()
            elif event.key == K_n:
                self.loader.load_next_level()
            elif event.key == K_p:
                self.loader.load_prev_level()
            elif event.key == K_z:
                self.undo()

        if not updated:
            return

        self.history.append(general_state)

        all_events = []

        for mov in self.moveables:
            pos = (mov.x, mov.y)
            if pos in self.interactables:
                event = self.interactables[pos].interact(mov)
                if event is not None:
                    all_events.append(event)
            old_pos = (mov.old_x, mov.old_y)
            if old_pos in self.interactables:
                event = self.interactables[old_pos].uninteract(mov)
                if event is not None:
                    all_events.append(event)

        self.handle_all_events(all_events)

    def handle_all_events(self, all_events: list[Event]):
        all_events.sort(key=lambda e: e.value)
        if Event.BUTTON_PRESS in all_events:
            all_events[:] = filter(lambda x: x != Event.BUTTON_UNPRESS, all_events)
        if Event.UNFREEZE in all_events:
            all_events[:] = filter(lambda x: x != Event.FREEZE, all_events)

        for event in all_events:
            self.handle_event(event)



    def handle_event(self, event):
        if event == Event.LEVEL_UNEND:
            pass
        elif event == Event.LEVEL_END:
            self.check_win()
        elif event == Event.PLAYER_DIE:
            self.player.die()
        elif event == Event.WEIGHT_DIE:
            self.player.weight_die()
        elif event == Event.BUTTON_PRESS:
            if not self.button_pressed:
                button_sound = mixer.Sound("sounds_effects/button_press.mp3")
                button_sound.set_volume(0.5)
                button_sound.play()
                for pos in self.interactables:
                    inter = self.interactables[pos]
                    if type(inter) is Slime:
                        inter.toggle()
            self.button_pressed = True
            for mov in self.moveables:
                pos = (mov.x, mov.y)
                if pos in self.interactables:
                    if type(self.interactables[pos]) is Slime:
                        self.interactables[pos].interact(mov)
        elif event == Event.BUTTON_UNPRESS:
            self.button_pressed = False
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
        self.resized_bg = pygame.transform.scale(self.background, (ceil(128 * scale), ceil(128 * scale)))

    def check_win(self):
        if all(map(lambda e: e.active, self.ends)):
            self.complete = time.time()

    def get_state(self):
        return (
            self.button_pressed,
        )

    def load_state(self, state):
        self.button_pressed = state[0]

    def undo(self):
        if len(self.history) == 0:
            return

        general_state = self.history.pop()
        self.load_state(general_state[0])

        for m, s in zip(self.moveables, general_state[1]):
            m.load_state(s)

        for i, s in zip(self.interactables.values(), general_state[2]):
            i.load_state(s)
