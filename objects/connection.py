import pygame

from objects.moveable import Moveable


class Connected(Moveable):
    frozen: bool
    # The list of objects, we're connected to
    cons: list[tuple['Connected', int]]

    def __init__(self, x, y, tileset, index, moveables, collision):
        super().__init__(x, y, tileset, index, moveables, collision)
        self.cons = [(self, 0)]
        self.frozen = False
        self.dead = False

    def move(self, dx, dy):
        if self.frozen:
            # If at least one of them cannot move, we don't move
            if any(not c.can_move_to(dx, dy) for c, _ in self.cons):
                return False

            # To make sure we'll not move any object twice,
            # we'll reorder the `cons` list
            asc = dx < 0 or dy < 0
            x_axis = dx != 0
            cons = sorted(self.cons, key=lambda con: con[0].x if x_axis else con[0].y, reverse=not asc)

            for c, _ in cons:
                Moveable.move(c, dx, dy)
        else:
            if not self.can_move_to(dx, dy):
                return False

            # First of all check if we can move
            for c, dist in self.cons:
                dist_x = abs(self.x + dx - c.x)
                dist_y = abs(self.y + dy - c.y)

                is_pulling = dist_x + dist_y > dist
                is_right_dir = self.x + dx == c.x or self.y + dy == c.y

                if is_pulling and not is_right_dir:
                    return False

            # We'll not do a `self.push(...)` here
            # because `self` is already inside `self.cons`
            asc = dx < 0 or dy < 0
            x_axis = dx != 0
            cons = sorted(self.cons, key=lambda con: con[0].x if x_axis else con[0].y, reverse=not asc)

            pulls = []
            for c, dist in cons:
                dist_x = abs(self.x + dx - c.x)
                dist_y = abs(self.y + dy - c.y)

                is_pulling = dist_x + dist_y > dist
                if dist != 0:
                    print(f"Diff: ({dist_x}, {dist_y})\nWalk: ({dx}, {dy})\nPos: ({self.x+dx}, {self.y+dy})\nPush: ({c.x}, {c.y})")

                if is_pulling:
                    pulls.append(c)

            for c in pulls:
                c.push(dx, dy)

            print()

        return True

    def freeze(self):
        if not self.frozen:
            for c, _ in self.cons:
                c.frozen = True
            # freeze_sound = mixer.Sound("sounds_effects/freeze.mp3")
            # # freeze_sound.set_volume(0.3)
            # freeze_sound.play()

    def unfreeze(self):
        if self.frozen:
            for c, _ in self.cons:
                c.frozen = False
            # unfreeze_sound = mixer.Sound("sounds_effects/unfreeze.mp3")
            # # unfreeze_sound.set_volume(0.3)
            # unfreeze_sound.play()

    def die(self):
        if not self.dead:
            for c, _ in self.cons:
                Moveable.die(c)
            # die_sound = mixer.Sound("sounds_effects/gameover.mp3")
            # die_sound.play()

    def draw_chain(self, surface, offset):
        return # TODO

        dist_px = math.sqrt(
            ((self.x - self.weight.x) * self.tileset.size[0]) ** 2 +
            ((self.y - self.weight.y) * self.tileset.size[1]) ** 2)

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
        if self.frozen:
            chain = self.tileset.chain_frozen
        else:
            chain = self.tileset.chain
        rotated_chain = pygame.transform.rotate(chain, angle)
        new_rect = rotated_chain.get_rect(
            bottomright=chain.get_rect(topleft=pos).center)
        new_rect = new_rect.move(offset)
        surface.blit(rotated_chain, new_rect)

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

    # A distance of 1000 implies infinite max_distance
    # Don't ask how it works, it just does
    @staticmethod
    def interconnect(c1: 'Connected', c2: 'Connected', dist: int = 1000):
        for c, _ in c1.cons[1:]:
            if c2 not in (k for k, _ in c.cons):
                c.cons.append((c2, 1000))
            if c not in (k for k, _ in c2.cons):
                c2.cons.append((c, 1000))
        for c, _ in c2.cons[1:]:
            if c1 not in (k for k, _ in c.cons):
                c.cons.append((c1, 1000))
            if c not in (k for k, _ in c1.cons):
                c1.cons.append((c, 1000))

        c1.cons.append((c2, dist))
        c2.cons.append((c1, dist))
