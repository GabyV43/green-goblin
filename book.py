import pygame

from button_menu import ButtonMenu


class Book():
    def __init__(self, filename, margin, screen_size, level_list, level_complete, font):
        self.filename = filename
        self.margin = margin
        self.original_image = pygame.image.load(filename)

        self.level_complete = level_complete

        self.buttons = []

        self.resize(screen_size)
        self.generate_buttons(level_list, font)

    def resize(self, screen_size):
        book_width = screen_size[0] - 2 * self.margin
        book_height = screen_size[1] - 2 * self.margin

        orig_width = self.original_image.get_width()
        orig_height = self.original_image.get_height()

        scale_x = book_width / orig_width
        scale_y = book_height / orig_height

        self.scale = min(scale_x, scale_y)

        self.image = pygame.transform.scale(self.original_image, (orig_width * self.scale, orig_height * self.scale))
        for button in self.buttons:
            button.resize(self.scale)

    def render(self, surface):
        surface.blit(self.image, (self.margin, self.margin))

        for button in self.buttons:
            button.render(surface)

    def generate_buttons(self, level_list, font):
        self.buttons = []

        start_x = 26
        start_y = 22

        btn_size = 13
        spacing_x = 5
        spacing_y = 4
        page_width = 75

        line = 0
        column = 0
        page = 0
        per_line = 4
        line_count = 4
        half_lines = 2

        for i in range(len(level_list)):
            if line < half_lines and column == 0 and page == 0:
                column = per_line // 2
            x = start_x + (btn_size + spacing_x) * column + page_width * page
            y = start_y + (btn_size + spacing_y) * line

            valor = False

            if i <= self.level_complete:
                valor = True

            btn = ButtonMenu(x, y, valor, i + 1, self.scale, self.margin, self.margin, font)

            self.buttons.append(btn)

            column += 1
            if column >= per_line:
                column = 0
                line += 1
                if line >= line_count:
                    line = 0
                    page += 1

    def set_level(self, final_level_complete):
        if final_level_complete < self.level_complete:
            return
        self.level_complete = final_level_complete

        file = open("save.txt", "w+")
        file.write(str(self.level_complete))
        file.close()

        for i, button in enumerate(self.buttons):
            if i <= self.level_complete:
                button.on = True



