from pygame.locals import *
from objects.moveable import Moveable
from pygame import mixer
import pygame
import math


class Player(Moveable):
    def __init__(self, tileset, x, y, moveables, collision, weight):
        super().__init__(x, y, tileset, 30, moveables, collision)
        self.weight = weight
        self.dead = False
        self.frozen = False

    def move(self, dx, dy):
        if self.frozen:
            if not self.can_move_to(dx, dy):
                return False

            if not self.weight.can_move_to(dx, dy):
                return False

            # weightB4 = self.x + dx == self.weight.x and self.y + dy == self.weight.y # se eu estou andando pra cima da bola
            # se eu ando na direção da bola
            weightB4 = dx > 0 and self.weight.x > self.x or dx < 0 and self.weight.x < self.x
            weightB4 |= dy > 0 and self.weight.y > self.y or dy < 0 and self.weight.y < self.y

            if weightB4:
                # anda ela antes, assim eu não empurro ela
                self.weight.move(dx, dy)
                super().move(dx, dy)
            else:
                super().move(dx, dy)  # caso contrário eu ando antes
                self.weight.move(dx, dy)
        else:
            if not self.can_move_to(dx, dy):
                return False

            dist_x = abs(self.x + dx - self.weight.x)
            dist_y = abs(self.y + dy - self.weight.y)

            is_pulling_weight = dist_x + dist_y > 3

            is_right_dir = self.x + dx == self.weight.x or self.y + dy == self.weight.y

            if is_pulling_weight and not is_right_dir:
                return False

            if is_pulling_weight and not self.weight.can_move_to(dx, dy):
                return False

            self.push(dx, dy)
            if is_pulling_weight:
                self.weight.push(dx, dy)

        feet_sound = mixer.Sound("sounds_effects/walking.mp3")
        feet_sound.set_volume(0.4)
        feet_sound.play()

        return True

    def update(self, event):
        if self.dead:
            return False
        if event.type == KEYDOWN:
            k = event.key
            if k == K_w or k == K_UP:
                return self.move(0, -1)
            elif k == K_s or k == K_DOWN:
                return self.move(0, 1)
            elif k == K_a or k == K_LEFT:
                return self.move(-1, 0)
            elif k == K_d or k == K_RIGHT:
                return self.move(1, 0)

    def render(self, surface, offset=(0, 0)):
        if self.dead:
            super().render(surface, 59, offset)
        elif self.frozen:
            self.draw_chain(surface, offset)
            super().render(surface, 60, offset)
        else:
            self.draw_chain(surface, offset)
            super().render(surface, offset=offset)

    def draw_chain(self, surface, offset):
        dist_px = math.sqrt(((self.x - self.weight.x) * self.tileset.size[0]) ** 2 + (
            (self.y - self.weight.y) * self.tileset.size[1]) ** 2)

        chain_width = self.tileset.chain_original.get_width()
        count = math.ceil(dist_px / chain_width)

        angle = math.atan2(self.weight.y - self.y, self.weight.x - self.x)

        for i in range(count):
            self.draw_single_chain_piece(surface, math.degrees(-angle),
                                         (
                                             (self.x + 0.5) * self.tileset.size[0] * self.tileset.scale + i *
                                             math.cos(
                                                 angle) * self.tileset.chain.get_width(),
                                             (self.y + 0.5) * self.tileset.size[1] * self.tileset.scale + i *
                                             math.sin(
                                                 angle) * self.tileset.chain.get_width()
            ),
                offset
            )

        self.weight.render(surface, offset)

    def draw_single_chain_piece(self, surface, angle, pos, offset):
        chain = self.tileset.chain
        rotated_chain = pygame.transform.rotate(chain, angle)
        new_rect = rotated_chain.get_rect(
            bottomright=chain.get_rect(topleft=pos).center)
        new_rect = new_rect.move(offset)
        surface.blit(rotated_chain, new_rect)

    def die(self):
        die_sound = mixer.Sound("sounds_effects/gameover.mp3")
        die_sound.play()
        super().die()

    def weight_die(self):
        self.lock()
        self.disappear()
        self.weight.disappear()

    def freeze(self):
        self.frozen = True
        self.weight.freeze()
        freeze_sound = mixer.Sound("sounds_effects/freeze.mp3")
        # freeze_sound.set_volume(0.3)
        freeze_sound.play()

    def unfreeze(self):
        self.frozen = False
        self.weight.unfreeze()
        unfreeze_sound = mixer.Sound("sounds_effects/unfreeze.mp3")
        # unfreeze_sound.set_volume(0.3)
        unfreeze_sound.play()

    def get_state(self):
        return (
            self.x,
            self.y,
            self.old_x,
            self.old_y,
            self.dead,
            self.disappeared,
            self.locked,
            self.frozen,
        )

    def load_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.old_x = state[2]
        self.old_y = state[3]
        self.dead = state[4]
        self.disappeared = state[5]
        self.locked = state[6]
        self.frozen = state[7]
