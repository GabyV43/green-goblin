from pygame.locals import *
from box import Box


class Player(Box):
    def __init__(self, tileset, index, x, y, moveables, collision, ball):
        super().__init__(x, y, tileset, index, moveables, collision)
        self.ball = ball

    def move(self, dx, dy):
        if not self.can_move_to(dx, dy):
            return

        dist_x = abs(self.x + dx - self.ball.x)
        dist_y = abs(self.y + dy - self.ball.y)

        is_pulling_ball = dist_x + dist_y > 3

        is_right_dir = self.x + dx == self.ball.x or self.y + dy == self.ball.y

        if is_pulling_ball and not is_right_dir:
            return

        if is_pulling_ball and not self.ball.can_move_to(dx, dy):
            return

        self.push(dx, dy)
        if is_pulling_ball:
            self.ball.push(dx, dy)

    def update(self, event):
        if event.type == KEYDOWN:
            k = event.key
            if k == K_w or k == K_UP:
                self.move(0, -1)
            elif k == K_s or k == K_DOWN:
                self.move(0, 1)
            elif k == K_a or k == K_LEFT:
                self.move(-1, 0)
            elif k == K_d or k == K_RIGHT:
                self.move(1, 0)
