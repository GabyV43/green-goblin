import time

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((600, 600))

t0 = time.time()
print("start")
font = pygame.font.Font("fonts/slkscr.ttf", 72)
print("Elapsed:", time.time() - t0)
img = font.render("TESTE 123", True, GRAY)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(BLACK)
    screen.blit(img, (50, 50))

    pygame.display.update()

pygame.quit()
