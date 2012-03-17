import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel
from Flamethrower import Flamethrower

def quit():
    pygame.quit()
    sys.exit()

pygame.init()

#Screen
WIDTH, HEIGHT = 800, 600
LEVEL_WIDTH = 2000
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('When Pigs Fly')
screen = pygame.display.get_surface() 
level = pygame.Surface((LEVEL_WIDTH, HEIGHT))

#Offset between model (level) and view (screen) 
offset = 0

font = pygame.font.Font(None, 48)

#Clock
clock = pygame.time.Clock()
FPS = 50
time_passed = 0

#Static list of controls
controls = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d]
#Dynamic list of active commands. Subset of controls.
commands = []

#Gravity boolean. True is Mario, False is Pokemon
gravity = False

#Read in a file to generate the sprites on a level
player, pigs, blocks = loadLevel("one.txt", level)
flamethrower = Flamethrower(level, player.x, player.y)

#Debugging string - set this and it appears onscreen!
db_str = ""

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
        elif event.type == MOUSEMOTION:
            flamethrower.rotateTo((player.x-offset, player.y), event.pos)

    #Update
    player.update(commands, gravity)
    flamethrower.update(player.x, player.y)
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
        level.fill((223, 223, 255))
    else:
        level.fill((223, 255, 223))

    #Non-moving sprites (aka "blocks")
    for block in blocks:
        block.draw()

    #Moving sprites
    player.draw()
    flamethrower.draw()
    for pig in pigs:
        pig.draw()

    #Set offset
    if player.x - offset < 50 and offset != 0:
        offset -= 10
    if player.x - offset > WIDTH-50 and offset != LEVEL_WIDTH:
        offset += 10

    screen.blit(level, (-offset, 0))
    screen.blit(font.render(db_str, 1, (0, 0, 0)), (10,10))
    pygame.display.flip() 
