from abc import ABC, abstractmethod

import pygame


class Renderable(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        ...
