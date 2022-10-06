

class Moveable:
    def __init__(self, x, y, tileset, index, moveables, collision):
        self.x = x
        self.y = y
        self.old_x = -1
        self.old_y = -1
        self.tileset = tileset
        self.index = index
        self.moveables = moveables
        self.collision = collision
        self.dead = False
        self.locked = False
        self.disappeared = False

    def move(self, dx, dy):
        if self.can_move_to(dx, dy):
            self.push(dx, dy)

    def push(self, dx, dy):
        self.old_x = self.x
        self.old_y = self.y
        self.x += dx
        self.y += dy

        for box in self.moveables:
            if box is self:
                continue
            if box.x == self.x and box.y == self.y:
                box.push(dx, dy)
                break

    def can_move_to(self, dx, dy):
        if self.locked:
            return

        new_x = self.x + dx
        new_y = self.y + dy

        if self.collision[new_y, new_x]:
            return False

        for box in self.moveables:
            if box is self:
                continue
            if box.x == new_x and box.y == new_y:
                if not box.can_move_to(dx, dy):
                    return False

        return True

    def render(self, surface, index=-1, offset=(0, 0)):
        if self.disappeared:
            return
        if index == - 1:
            index = self.index
        scale = self.tileset.scale
        tw, th = self.tileset.size

        img = self.tileset.tiles[index]
        surface.blit(img, (self.x * tw * scale +
                     offset[0], self.y * th * scale + offset[1]))

    def die(self):
        self.dead = True

    def disappear(self):
        self.disappeared = True

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def get_state(self):
        return (
            self.x,
            self.y,
            self.old_x,
            self.old_y,
            self.dead,
            self.disappeared,
            self.locked,
        )

    def load_state(self, state):
        self.x = state[0]
        self.y = state[1]
        self.old_x = state[2]
        self.old_y = state[3]
        self.dead = state[4]
        self.disappeared = state[5]
        self.locked = state[6]
