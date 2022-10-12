import pygame


class ButtonMenu():
    def __init__(self, x, y, on, number, scale, offsetx, offsety, font, book_page):
        self.x = x
        self.y = y
        self.on = on
        self.offsetx = offsetx
        self.offsety = offsety
        self.number = number
        self.image_on = pygame.image.load("images/menu_button_on.png")
        self.image_off = pygame.image.load("images/menu_button_off.png")
        self.text_img = font.render(str(number), True, "#FFFFFF")
        self.text_img_off = font.render(str(number), True, "#5a5466")
        self.text_off_x = (self.image_on.get_width() -
                           self.text_img.get_width()) / 2
        self.text_off_y = (self.image_on.get_height() -
                           self.text_img.get_height()) // 2
        self.book_page = book_page

        self.resize(scale)

    def resize(self, scale):
        self.width = self.image_on.get_width() * scale
        self.height = self.image_off.get_height() * scale
        self.image_on_resized = pygame.transform.scale(
            self.image_on, (self.width, self.height))
        self.image_off_resized = pygame.transform.scale(
            self.image_off, (self.width, self.height))
        self.text_img_resized = pygame.transform.scale(
            self.text_img, (self.text_img.get_width() * scale, self.text_img.get_height() * scale))
        self.text_img_off_resized = pygame.transform.scale(
            self.text_img_off, (self.text_img.get_width() * scale, self.text_img.get_height() * scale))
        self.xredim = self.x * scale
        self.yredim = self.y * scale
        self.text_off_x_redim = self.text_off_x * scale
        self.text_off_y_redim = self.text_off_y * scale

    def render(self, surface, page):
        
        if page == self.book_page:
            if self.on:
                surface.blit(self.image_on_resized, (self.xredim +
                            self.offsetx, self.offsety + self.yredim))
                surface.blit(self.text_img_resized, (self.xredim + self.offsetx +
                            self.text_off_x_redim, self.offsety + self.yredim + self.text_off_y_redim))

            else:
                surface.blit(self.image_off_resized, (self.xredim +
                            self.offsetx, self.offsety + self.yredim))
                surface.blit(self.text_img_off_resized, (self.xredim + self.offsetx +
                            self.text_off_x_redim, self.offsety + self.yredim + self.text_off_y_redim))

    def contains(self, x, y):
        if x >= self.xredim + self.offsetx and x <= self.xredim + self.width + self.offsetx:
            if y >= self.yredim + self.offsety and y <= self.yredim + self.height + self.offsety:
                return True
        return False
