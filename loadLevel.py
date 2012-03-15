import pygame
from pygame.locals import *
from Block import Block
from Player import Player
from Pig import Pig

def loadLevel(level_name, screen):
    pigs = []
    blocks = []

    col = row = 0
    GRANULARITY = 20
    WIDTH = 800/GRANULARITY
    HEIGHT = 600/GRANULARITY

    spriteMap = open(level_name)
    region = spriteMap.read(1)
    while region != "":
        x, y = col*GRANULARITY, row*GRANULARITY

        if region == " ":
            pass
        elif region == "\n":
            row += 1
            col  = 0
        elif region == "P":
            pigs.append(Pig(screen, x, y))
        elif region == "T":
            player = Player(screen, x, y)
       # Uncomment and fill in when we have block sprites
       # elif region == "#":
       #     blocks.append(Block(screen, pygame.Rect(x, y, IMAGE_WIDTH, IMAGE_HEIGHT), IMAGE_FILENAME)) 
        else:
            print "Unrecognized character: " + region

        col += 1
        region = spriteMap.read(1)

    return player, pigs, blocks
