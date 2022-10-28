import pygame

from . import cache
from .screen import Screen


def main():
    pygame.init()
    cache.load_cache()

    running = True
    size = (800, 600)
    surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    screen = Screen(size, 3)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                screen.handle_event(event)

        surface.fill((0, 0, 0))
        screen.render(surface)
        pygame.display.flip()

    cache.save_cache()


if __name__ == '__main__':
    main()
