import pygame, sys, os, random
from pygame.locals import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Pig(pygame.sprite.Sprite):
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0

        #Gravitational acceleration
        self.g = -1

        #flying speed
        self.flyingSpeed = 8

        #Boundaries
        self.maxx = self.screen.get_width()
        self.maxy = self.screen.get_height()
        #minimums assumed to be zero

    def update(self, gravity):
        self.gravity = gravity
        
        if gravity:
            #todo: collision detection for standing on platforms
            #currently always in freefall
            self.dy -= self.g
        else:
            self.dx = 0
            self.dy = 0
            #randomize speed of the pig.

            self.dy += random.randint(-5,5)
            self.dx += random.randint(-5,5)
        
        self.x += self.dx
        self.y += self.dy
       
        #Inelastic collisions
        if not gravity:
            if self.x != bound(0, self.x, self.maxx):
                self.dx //= -2
            if self.y != bound(0, self.y, self.maxy):
                self.dy //= -2

        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

    def draw(self):
        #Dummy draw method
        if self.gravity:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), 5)
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 5)
