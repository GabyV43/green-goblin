from pygame.locals import *

from objects.connection import Connected
from objects.moveable import Moveable
import pygame
import math
from pygame.time import get_ticks


INITIAL_DELAY = 300
AFTER_DELAY = 100


class Player(Connected):
    def __init__(self, tileset, x, y, moveables, collision, uid: int):
        super().__init__(x, y, tileset, 30, moveables, collision, uid)
        self.dead = False
        self.frozen = False
        self.weight_dead = False
        self.old_dx = 0
        self.old_dy = 0
        self.held_time = -1
        self.held_button = -1
        self.held_repeat = 0

    # def move(self, dx, dy):
    #     if self.frozen:
    #         if not self.can_move_to(dx, dy):
    #             return False
    #
    #         if not self.weight.can_move_to(dx, dy):
    #             return False
    #
    #         # weightB4 = self.x + dx == self.weight.x and self.y + dy == self.weight.y # se eu estou andando pra cima da bola
    #         # se eu ando na direção da bola
    #         weightB4 = dx > 0 and self.weight.x > self.x or dx < 0 and self.weight.x < self.x
    #         weightB4 |= dy > 0 and self.weight.y > self.y or dy < 0 and self.weight.y < self.y
    #
    #         if weightB4:
    #             # anda ela antes, assim eu não empurro ela
    #             self.weight.move(dx, dy)
    #             super().move(dx, dy)
    #         else:
    #             super().move(dx, dy)  # caso contrário eu ando antes
    #             self.weight.move(dx, dy)
    #     else:
    #         if not self.can_move_to(dx, dy):
    #             return False
    #
    #         dist_x = abs(self.x + dx - self.weight.x)
    #         dist_y = abs(self.y + dy - self.weight.y)
    #
    #         is_pulling_weight = dist_x + dist_y > 3
    #
    #         is_right_dir = self.x + dx == self.weight.x or self.y + dy == self.weight.y
    #
    #         if is_pulling_weight and not is_right_dir:
    #             # chain_sound = mixer.Sound("sounds_effects/chain.mp3")
    #             # # feet_sound.set_volume(0.2)
    #             # chain_sound.play()
    #             return False
    #
    #         if is_pulling_weight and not self.weight.can_move_to(dx, dy):
    #             return False
    #
    #         self.push(dx, dy)
    #         if is_pulling_weight:
    #             self.weight.push(dx, dy)
    #
    #     # feet_sound = mixer.Sound("sounds_effects/walking.mp3")
    #     # feet_sound.set_volume(0.4)
    #     # feet_sound.play()
    #
    #     return True

    def update(self, event):
        if self.dead:
            return False
        if event is None:
            if self.held_button != -1:
                t = get_ticks() - self.held_time
                if t > INITIAL_DELAY:
                    t -= INITIAL_DELAY
                    t //= AFTER_DELAY
                    if t + 1 > self.held_repeat:
                        self.held_repeat += 1
                        if self.held_button == 0:
                            return self.move(0, -1)
                        elif self.held_button == 1:
                            return self.move(0, 1)
                        elif self.held_button == 2:
                            return self.move(-1, 0)
                        elif self.held_button == 3:
                            return self.move(1, 0)
        elif event.type == KEYDOWN:
            k = event.key
            if k == K_w or k == K_UP:
                self.held_button = 0
                self.held_time = get_ticks()
                return self.move(0, -1)
            elif k == K_s or k == K_DOWN:
                self.held_button = 1
                self.held_time = get_ticks()
                return self.move(0, 1)
            elif k == K_a or k == K_LEFT:
                self.held_button = 2
                self.held_time = get_ticks()
                return self.move(-1, 0)
            elif k == K_d or k == K_RIGHT:
                self.held_button = 3
                self.held_time = get_ticks()
                return self.move(1, 0)
        elif event.type == KEYUP:
            k = event.key
            if (k == K_w or k == K_UP) and self.held_button == 0:
                self.held_button = -1
                self.held_repeat = 0
            elif (k == K_s or k == K_DOWN) and self.held_button == 1:
                self.held_button = -1
                self.held_repeat = 0
            elif (k == K_a or k == K_LEFT) and self.held_button == 2:
                self.held_button = -1
                self.held_repeat = 0
            elif (k == K_d or k == K_RIGHT) and self.held_button == 3:
                self.held_button = -1
                self.held_repeat = 0
        elif event.type == JOYHATMOTION:
            (dx, dy) = event.value
            if self.old_dx != dx:
                self.old_dx = dx
                if dx != 0:
                    return self.move(dx, 0)
            elif self.old_dy != dy:
                self.old_dy = dy
                if dy != 0:
                    return self.move(0, -dy)

    def render(self, surface, index=-1, offset=(0, 0)):
        if self.dead:
            if index == -1:
                index = 59
            super().render(surface, index, offset)
        elif self.frozen:
            if index == -1:
                index = 60
            super().render(surface, index, offset)
        else:
            super().render(surface, index, offset=offset)

