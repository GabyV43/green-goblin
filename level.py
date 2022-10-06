from email import message
from interactables.box_end import BoxEnd
from interactables.player_end import PlayerEnd
from interactables.weight_end import WeightEnd
import pygame
from pygame import Surface
from pygame.locals import *
from event import Event
from objects.box import Box
from objects.player import Player
from objects.weight import Weight
from interactables.slime import Slime
import time
from tileset import TileSet
from pygame import mixer
from math import ceil


class Level:
    player: Player

    def __init__(self, tileset: TileSet, player, moveables, interactables, decorations, collision, loader, name):
        self.tileset = tileset
        self.player = player
        self.moveables = moveables
        self.interactables = interactables
        self.decorations = decorations
        self.collision = collision
        self.background = pygame.image.load('images/tent_fundo1.png')
        self.resized_bg = self.background
        self.offset = (0, 0)
        self.loader = loader
        self.name = name
        self.complete = None
        self.ends = list(filter(lambda t:
                                type(t) is PlayerEnd
                                or type(t) is WeightEnd
                                or type(t) is BoxEnd,
                                (interactables[pos] for pos in interactables)))
        for end in self.ends:
            if type(end) is PlayerEnd:
                if end.x == self.player.x and end.y == self.player.y:
                    end.active = True
            elif type(end) is WeightEnd:
                if end.x == self.player.weight.x and end.y == self.player.weight.y:
                    end.active = True
            elif type(end) is BoxEnd:
                for mov in self.moveables:
                    if type(mov) is Box:
                        if end.x == mov.x and end.y == mov.y:
                            end.active = True
                            break
        self.button_pressed = False
        self.history = []

        self.level_completed = False

        self.stop_message = False
        self.message_shown = False
        self.click_r = 0
        self.click_z = 0

    def render(self, surface: Surface):
        w = int(surface.get_width() // self.tileset.scale // 4)
        h = int(surface.get_height() // self.tileset.scale // 4)

        for x in range(w):
            for y in range(h):
                surface.blit(self.resized_bg, (x * 128 *
                             self.tileset.scale, y * 128 * self.tileset.scale))

        self.collision.render(surface, self.offset)

        for dec in self.decorations:
            dec.render(surface, self.offset)

        for pos in self.interactables:
            self.interactables[pos].render(surface, offset=self.offset)

        for mov in self.moveables:
            mov.render(surface, offset=self.offset)

        self.player.render(surface, self.offset)

        self.appear_screen(surface)

        if self.complete is not None:
            self.level_completed = True
            win_sound = mixer.Sound("sounds_effects/win.mp3")
            win_sound.set_volume(0.15)
            win_sound.play()
            if time.time() - self.complete > 0.5:
                self.loader.load_next_level()

    def update(self, event: pygame.event.Event):
        if self.complete is not None:
            return

        general_state = (
            self.get_state(),
            [m.get_state() for m in self.moveables],
            [i.get_state() for i in self.interactables.values()]
        )

        updated = self.player.update(event)

        if event is None:
            pass
        elif event.type == KEYDOWN:
            if event.key == K_r:
                self.click_r += 1
                self.reload()
            elif event.key == K_n:
                self.loader.load_next_level()
            elif event.key == K_p:
                self.loader.load_prev_level()
            elif event.key == K_z:
                self.click_z += 1
                self.undo()
            elif event.key == K_k:
                self.loader.reload()
        elif event.type == JOYBUTTONDOWN:
            if event.button == 1:  # B button
                print("UNDO")
                self.click_z += 1
                self.undo()
            elif event.button == 3:  # Y button
                self.click_r += 1
                self.reload()

        if not updated:
            return

        self.history.append(general_state)

        all_events = []

        for mov in self.moveables:
            pos = (mov.x, mov.y)
            if pos in self.interactables:
                print("int")
                event = self.interactables[pos].interact(mov)
                if event is not None:
                    all_events.append(event)
            old_pos = (mov.old_x, mov.old_y)
            if old_pos in self.interactables:
                ####################
                print("unin")
                event = self.interactables[old_pos].uninteract(mov)
                if event is not None:
                    all_events.append(event)

        self.handle_all_events(all_events)

    def handle_all_events(self, all_events: list[Event]):
        all_events.sort(key=lambda e: e.value)
        if Event.BUTTON_PRESS in all_events:
            all_events[:] = filter(
                lambda x: x != Event.BUTTON_UNPRESS, all_events)
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
            fall_sound = mixer.Sound("sounds_effects/girlfall.mp3")
            # fall_sound.set_volume(0.3)
            fall_sound.play()
        elif event == Event.BUTTON_PRESS:
            if not self.button_pressed:
                button_sound = mixer.Sound("sounds_effects/button_press.mp3")
                # button_sound.set_volume(0.5)
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
        self.resized_bg = pygame.transform.scale(
            self.background, (ceil(128 * scale), ceil(128 * scale)))

        if scale_x > scale_y:
            self.offset = ((width - scale * tw) / 2, 0)
        else:
            self.offset = (0, (height - scale * th) / 2)

    def check_win(self):
        # print(all(map(lambda e: e.active, self.ends)), not self.player.dead, not self.player.weight_dead)
        if all(map(lambda e: e.active, self.ends)) and not self.player.dead and not self.player.weight_dead:
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
        self.load_general_state(general_state)

    def reload(self):
        if len(self.history) == 0:
            return
        general_state = self.history[0]
        current_state = (
            self.get_state(),
            [m.get_state() for m in self.moveables],
            [i.get_state() for i in self.interactables.values()]
        )
        self.history.append(current_state)
        self.load_general_state(general_state)

        print(self.history)

    def load_general_state(self, state):
        self.load_state(state[0])

        for m, s in zip(self.moveables, state[1]):
            m.load_state(s)

        for i, s in zip(self.interactables.values(), state[2]):
            i.load_state(s)

    def appear_screen(self, surface):
        if self.stop_message == True:
            return

        if self.name == "level2.tmx":
            if self.message_shown or self.player.weight.x == 4 and self.player.weight.y == 8:
                self.message_shown = True
                warn = pygame.image.load("images/message.png")
                surface.blit(warn, (0, 0))
            if self.click_z != 0 and self.click_r != 0:
                self.stop_message = True

        if self.name == "tutorial1.tmx":
            warn2 = pygame.image.load("images/message2.png")
            surface.blit(warn2, (0, 0))
            if len(self.history) >= 3:
                self.stop_message = True

        elif self.name == "intfinalbox.tmx":
            warn = pygame.image.load("images/message.png")
            surface.blit(warn, (0, 0))
            if len(self.history) >= 10:
                self.stop_message = True
