import pygame, sys, os
from pygame.locals import *
from Player import Player
from Pig import Pig

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

#static list of controls
controls = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
#dynamic list of active commands. Subset of controls.
commands = []

#Gravity boolean. True is Mario, False is Pokemon
gravity = False

#The player (a sprite)
player = Player(screen, 400, 300)

pigs = [Pig(screen, 100, 200), Pig(screen, 500, 400)] 

#game loop
while True:
    time_passed = clock.tick(FPS)

    #Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            elif event.key in controls:
                commands.append(event.key)
            elif event.key == K_SPACE:
                gravity = not gravity
        elif event.type == KEYUP:
            if event.key in commands:
                commands.remove(event.key)

    #Background
    screen.fill((255, 255, 255))

    #Non-moving sprites go here

    #Update
    player.update(commands, gravity)
    for pig in pigs:
        pig.update(gravity)

    #Check pig-player collisions
    for pig in pigs:
        if pygame.sprite.collide_rect(player, pig):
            if gravity:
                pig.kill()
            else:
                player.kill()

    #Draw
    player.draw()
    for pig in pigs:
        pig.draw()

    pygame.display.flip() 
