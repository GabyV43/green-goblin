from abc import ABC, abstractmethod

import pygame


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        ...
