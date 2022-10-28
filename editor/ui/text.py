import pygame

from ..renderable import Renderable
from ..scalable import Scalable


class Text(Renderable, Scalable):
    font: pygame.font.Font
    text: str
    color: any
    size: int
    position: tuple[int, int]
    center: tuple[int, int]
    centered: bool
    rect: pygame.Rect
    drawn: pygame.Surface

    def __init__(self, font: pygame.font.Font, text: str, color: any, size: int,
                 position: tuple[int, int] | None = None, center: tuple[int, int] | None = None):
        self.font = font
        self.text = text
        self.color = color
        self.centered = center is not None
        if position is not None:
            assert center is None
            self.position = position
            self.center = None
        else:
            assert center is not None
            self.center = center
            self.position = None

        self.drawn = self.font.render(self.text, True, self.color)
        self.rect = self.drawn.get_rect()
        if self.centered:
            self.position = (self.center[0] - self.rect.width // 2,
                             self.center[1] - self.rect.height // 2)
        else:
            self.center = (self.position[0] + self.rect.width // 2,
                           self.position[1] + self.rect.height // 2)
        self.rect.center = self.center

    def render(self, surface: pygame.Surface, offset: tuple[int, int] = ...):
        surface.blit(self.drawn, self.rect)

    def rescale(self, scale: float):
        return super().rescale(scale)

    def set_text(self, text: str):
        self.text = text
        self.drawn = self.font.render(self.text, True, self.color)
        self.rect = self.drawn.get_rect()
        if self.centered:
            self.rect.center = self.center
            self.position = self.rect.topleft
        else:
            self.rect.topleft = self.position
            self.center = self.rect.center
