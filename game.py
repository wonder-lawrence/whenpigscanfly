import pygame, sys, os
from pygame.locals import *

def quit():
    pygame.quit()
    sys.exit()

pygame.init()
screenDimensions = (800, 600)
window = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption('When Pigs Fly')
screen = pygame.display.get_surface() 

clock = pygame.time.Clock()
FPS = 50
time_passed = 0

#game loop
while True:
    time_passed = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()

    screen.fill((255, 255, 255))

    pygame.display.flip() 
