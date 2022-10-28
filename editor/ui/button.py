import pygame

from ..renderable import Renderable


class Button(Renderable):
    font: pygame.font.Font
    text: str
    color: any
    text_color: any
    size: tuple[int, int]
    position: tuple[int, int]
    rect: pygame.Rect
    text_drawn: pygame.Surface
    text_rect: pygame.Rect

    def __init__(self, font: pygame.font.Font, text: str, color: any, text_color: any, size: tuple[int, int],
                 position: tuple[int, int] | None = None, center: tuple[int, int] | None = None):
        self.text = text
        self.size = size
        self.color = color
        self.text_color = text_color
        if position is not None:
            assert center is None
            self.position = position
        else:
            assert center is not None
            self.position = (center[0] - size[0] // 2,
                             center[1] - size[1] // 2)

        self.font = font
        self.rect = pygame.Rect(*self.position, *self.size)
        self.render_text()

    def render(self, surface: pygame.Surface, offset: tuple[int, int] = ...):
        pygame.draw.rect(surface, self.color, self.rect.move(offset))
        surface.blit(self.text_drawn, self.text_rect)

    def render_text(self):
        self.text_drawn = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_drawn.get_rect()
        self.text_rect.center = self.rect.center

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(*pos)
