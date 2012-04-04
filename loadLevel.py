import pygame
from pygame.locals import *
from Block import Block
from Player import Player
from Pig import Pig

def loadLevel(level_name, screen):
    """
    loadLevel - expects the name of a sprite map and the screen, and returns the
    sprites for the level.
    
    The sprite map is the name of a file, whose contents consist of spaces,
    newlines, P's, and exactly one T.  Max line length is 40; max number of
    lines is 30. For best results, align blocks and keep pigs away from edges.
    
    Return type: a tuple of one Player object, a possibly empty list of Pig
    objects, and a possibly empty list of Block objects.
    """

    pigs = []
    blocks = []

    col = row = 0
    GRANULARITY = 20

    spriteMap = open(level_name)
    region = spriteMap.read(1)
    while region != "":
        x, y = col*GRANULARITY, row*GRANULARITY

        if (region == " " or region == "\t"):
            pass
        elif region == "\n":
            row += 1
            col  = -1
        elif region == "P":
            pigs.append(Pig(screen, x, y))
        elif region == "T":
            player = Player(screen, x, y)
        elif region == "#":
            blocks.append(Block(screen, pygame.Rect(x, y, 60, 60), "filecab.png")) 
        else:
            print "Unrecognized character: " + region

        col += 1
        region = spriteMap.read(1)

    spriteMap.close()
    return player, pigs, blocks
