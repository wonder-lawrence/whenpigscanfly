import pygame, sys, os
from pygame.locals import *
from loadLevel import loadLevel

def quit():
    pygame.quit()
    sys.exit()

def abs (x):
    if x < 0:
        return -1 * x
    else:
        return x

pygame.init()

#Screen
WIDTH, HEIGHT = 800, 600
LEVEL_WIDTH = 2000
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('When Pigs Fly')
screen = pygame.display.get_surface() 
level = pygame.Surface((LEVEL_WIDTH, HEIGHT+1))

#Offset between model (level) and view (screen) 
offset = 0

#Clock
clock = pygame.time.Clock()
FPS = 50
time_passed = 0

#Static list of controls
controls = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d]
#Dynamic list of active commands. Subset of controls.
commands = []

#Read in a file to generate the sprites on a level
player, pigs, blocks = loadLevel("one.txt", level)
flames = []

#Score and score display
font = pygame.font.Font(None, 48)
score_str = ""
score = 0
redHue = 255

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
                flames.append(player.shoot())
        elif event.type == KEYUP:
            if event.key in commands:
                commands.remove(event.key)
        elif event.type == MOUSEMOTION:
            player.rotateFlamethrower((event.pos[0]+offset, event.pos[1]))
        elif event.type == MOUSEBUTTONDOWN:
            flames.append(player.shoot())

    #Update
    player.update(commands)
    for flame in flames:
        flame.update()
    for pig in pigs:
        pig.update()

    #Check pig collisions
    for pig in pigs:
        if pygame.sprite.collide_rect(player, pig):
            player.kill()
        for flame in flames:
            if pygame.sprite.collide_rect(flame, pig):
                pig.kill()
                flame.kill()
                score += 1

    #Check block collisions
    for block in blocks:
        if pygame.sprite.collide_rect(player, block):
            tmp_str = str(player.y + player.image_h) +" "+str(block.rect.top)
            if player.y + player.image_h < block.rect.top +2 <= player.y + player.image_h + 10:
                player.collideTop(block)
                tmp_str += "  Top     "
            elif block.rect.bottom < player.y + abs(player.dy):
                player.collideBottom()
                tmp_str += "  Bottom  "
            else:
                player.collideSide(block)
                tmp_str += "  Side    "

        for pig in pigs:
            if pygame.sprite.collide_rect(pig, block):
                pig.reverse()

    if tmp_str != score_str:
        score_str = tmp_str
        redHue = 255

    #Flame with blocks
    for flame in flames:
        collided = False
        for block in blocks:
            if pygame.sprite.collide_rect(flame, block):
                collided = True
        if collided:
           flame.kill(True)
        else:
            flame.blockImmune = False

    #Remove inactive sprites
    pigs   = filter(lambda pig: pig.active, pigs)
    flames = filter(lambda flm: flm.active, flames)
   
  #  score_str = str(score)

    #Draw
    #Background
    level.fill((205, 133, 63))

    #Non-moving sprites (aka "blocks")
    for block in blocks:
        block.draw()

    #Moving sprites
    player.draw()
    for flame in flames:
        flame.draw()
    for pig in pigs:
        pig.draw()

    #Set offset
    if player.x - offset < 50 and offset != 0:
        offset -= 10
    if player.x - offset > WIDTH-150 and offset + WIDTH < LEVEL_WIDTH:
        offset += 10
    
    screen.blit(level, (-offset, 0))
    screen.blit(font.render(score_str, True, (redHue, 0, 0)), (10,10))
    redHue *= 145
    redHue //= 150
    pygame.display.flip() 
