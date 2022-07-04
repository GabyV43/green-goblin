from pygame.locals import *
from objects.moveable import Moveable
from pygame import mixer

class Player(Moveable):
    def __init__(self, tileset, x, y, moveables, collision, weight):
        super().__init__(x, y, tileset, 30, moveables, collision)
        self.weight = weight
        self.dead = False
        self.locked = False
        self.frozen = False

    def can_move_to(self, dx, dy):
        return super().can_move_to(dx, dy) and not self.locked

    def move(self, dx, dy):
        if self.frozen:
            if not self.can_move_to(dx, dy):
                return False

            if not self.weight.can_move_to(dx, dy):
                return False

            if self.x + dx == self.weight.x and self.y + dy == self.weight.y: # se eu estou andando pra cima da bola
                self.weight.move(dx, dy) # anda ela antes, assim eu não empurro ela
                super().move(dx, dy)
            else:
                super().move(dx, dy) # caso contrário eu ando antes
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
            feet_sound.set_volume(0.2)
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

    def render(self, surface):
        if self.dead:
            super().render(surface, 59)
        else:
            super().render(surface)

    def die(self):
        die_sound = mixer.Sound("sounds_effects/gameover.mp3")
        die_sound.play()
        super().die()


    def weight_die(self):
        self.lock()
        self.disappear()
        self.weight.disappear()

    def lock(self):
        self.locked = True

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False
