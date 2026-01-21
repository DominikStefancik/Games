import os

import pygame

from constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()

pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Hangman")

clock = pygame.time.Clock()

is_running = True

while is_running:
    # Make sure the game loop runs at the speed we set
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           is_running = False


pygame.quit()
