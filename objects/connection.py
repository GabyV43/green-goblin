import pygame

from objects.moveable import Moveable


class Connected(Moveable):
    frozen: bool
    just_molten: bool
    # The list of objects, we're connected to
    cons: list[tuple['Connected', int]]
    con_id: int
    obj_id: int

    def __init__(self, x, y, tileset, index, moveables, collision, uid: int):
        super().__init__(x, y, tileset, index, moveables, collision)
        self.cons = [(self, 0)]
        self.frozen = False
        self.dead = False
        self.just_molten = False
        self.con_id = uid
        self.obj_id = uid

    def can_move_to(self, dx, dy, ids: list[int] = None):
        if ids is None:
            ids = []

        if self.con_id in ids:
            return Moveable.can_move_to(self, dx, dy, ids)
        else:
            ids.append(self.con_id)

        if self.frozen:
            if any(not c.can_move_to(dx, dy, ids) for c, _ in self.cons):
                return False
        else:
            if not self.can_move_to(dx, dy, ids):
                return False
            pulls = []

            for c, dist in self.cons:
                dist_x = abs(self.x + dx - c.x)
                dist_y = abs(self.y + dy - c.y)

                is_pulling = dist_x + dist_y > dist
                is_right_dir = self.x + dx == c.x or self.y + dy == c.y

                if is_pulling:
                    if not is_right_dir:
                        return False
                    pulls.append(c)

            for p in pulls:
                if not p.can_move_to(dx, dy, ids):
                    return False

        return True

    def push(self, dx, dy, ids: list[int] = None):
        if ids is None:
            ids = []

        if self.con_id in ids:
            res = Moveable.push(self, dx, dy, ids)

            if res:
                self.just_molten = False

            return res
        else:
            ids.append(self.con_id)

        if self.frozen:
            # To make sure we'll not move any object twice,
            # we'll reorder the `cons` list
            asc = dx < 0 or dy < 0
            x_axis = dx != 0
            cons = sorted(self.cons, key=lambda con: con[0].x if x_axis else con[0].y, reverse=not asc)

            for c, _ in cons:
                Moveable.push(c, dx, dy, ids)
        else:
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

                if is_pulling:
                    pulls.append(c)

            for c in pulls:
                c.push(dx, dy, ids)

        self.just_molten = False

        return True

    def freeze(self):
        if not self.frozen and not self.just_molten:
            print("Freeze")
            for c, _ in self.cons:
                c.frozen = True
            # freeze_sound = mixer.Sound("sounds_effects/freeze.mp3")
            # # freeze_sound.set_volume(0.3)
            # freeze_sound.play()

    def unfreeze(self):
        print("Unfreeze")
        for c, _ in self.cons:
            c.frozen = False
            c.just_molten = True
        if self.frozen:
            ...
            # unfreeze_sound = mixer.Sound("sounds_effects/unfreeze.mp3")
            # # unfreeze_sound.set_volume(0.3)
            # unfreeze_sound.play()

    def die(self):
        if not self.dead:
            for c, _ in self.cons:
                Moveable.die(c)
            # die_sound = mixer.Sound("sounds_effects/gameover.mp3")
            # die_sound.play()

    def render(self, surface, index=-1, offset=(0, 0)):
        # if self.obj_id == self.con_id:
        self.draw_chain(surface, offset)
        super().render(surface, index, offset)

    def draw_chain(self, surface, offset):
        for c, dist in self.cons:
            if dist == 0 or dist == 1000 or self.obj_id >= c.obj_id:
                continue

            import math

            dist_px = math.sqrt(
                ((self.x - c.x) * self.tileset.size[0]) ** 2 +
                ((self.y - c.y) * self.tileset.size[1]) ** 2)

            chain_width = self.tileset.chain_original.get_width()
            count = math.ceil(dist_px / chain_width)

            angle = math.atan2(c.y - self.y, c.x - self.x)

            for i in range(count):
                self.draw_single_chain_piece(
                    surface,
                    math.degrees(-angle),
                    (
                        (self.x + 0.5) * self.tileset.size[0] * self.tileset.scale + i *
                        math.cos(angle) * self.tileset.chain.get_width(),
                        (self.y + 0.5) * self.tileset.size[1] * self.tileset.scale + i *
                        math.sin(angle) * self.tileset.chain.get_width()
                    ),
                    offset
                )

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
    @staticmethod
    def interconnect(c1: 'Connected', c2: 'Connected', dist: int = 1000):
        for c, _ in c1.cons[1:]:
            if c is c1:
                continue
            if c2 not in (k for k, _ in c.cons):
                c.cons.append((c2, 1000))
            if c not in (k for k, _ in c2.cons):
                c2.cons.append((c, 1000))
        for c, _ in c2.cons[1:]:
            if c is c2:
                continue
            if c1 not in (k for k, _ in c.cons):
                c.cons.append((c1, 1000))
            if c not in (k for k, _ in c1.cons):
                c1.cons.append((c, 1000))

        if c2 in (k for k, _ in c1.cons):
            con = next(con for con in c1.cons if con[0] is c2)
            c1.cons.remove(con)
        c1.cons.append((c2, dist))
        if c1 in (k for k, _ in c2.cons):
            con = next(con for con in c2.cons if con[0] is c1)
            c2.cons.remove(con)
        c2.cons.append((c1, dist))

        cid = min(c1.con_id, c2.con_id)

        for c, _ in c1.cons + c2.cons:
            c.con_id = cid

        assert len(c1.cons) == len(c2.cons)
        for c, _ in c1.cons:
            assert len(c.cons) == len(c1.cons)
        for c, _ in c2.cons:
            assert len(c.cons) == len(c2.cons)
