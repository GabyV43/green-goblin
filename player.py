from pygame.locals import *


class Player:
    def __init__(self, tileset, index, x, y, collision, index_ball, x_ball, y_ball):
        self.tileset = tileset
        self.index = index
        self.x = x
        self.y = y
        self.collision = collision
        self.index_ball = index_ball
        self.x_ball = x_ball
        self.y_ball = y_ball

    def render(self, surface):
        scale = self.tileset.scale
        tw, th = self.tileset.size

        img = self.tileset.tiles[self.index]
        surface.blit(img, (self.x * tw * scale, self.y * th * scale))

        img_ball = self.tileset.tiles[self.index_ball]
        surface.blit(img_ball, (self.x_ball * tw * scale, self.y_ball * th * scale))

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if not self.collision[new_y, new_x]:
            self.x = new_x
            self.y = new_y

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
