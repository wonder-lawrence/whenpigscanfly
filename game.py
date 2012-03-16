import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel

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
controls = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d]
#dynamic list of active commands. Subset of controls.
commands = []

#Gravity boolean. True is Mario, False is Pokemon
gravity = False

#Read in a file to generate the sprites on a level
player, pigs, blocks = loadLevel("one.txt", screen)
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
   
    #Remove inactive pigs
    pigs = filter(lambda pig: pig.active, pigs)
    
    #Draw
    #Background
    if gravity:
        screen.fill((223, 223, 255))
    else:
        screen.fill((223, 255, 223))

    #Non-moving sprites (aka "blocks")
    for block in blocks:
        block.draw()

    #Moving sprites
    player.draw()
    for pig in pigs:
        pig.draw()

    pygame.display.flip() 
