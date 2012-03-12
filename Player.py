import pygame
from pygame.locals import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Player(pygame.sprite.Sprite):
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0

        #Gravitational acceleration
        self.g = -2

        #Walking speed
        self.walkSpeed = 10

        #Boundaries
        self.maxx = self.screen.get_width()
        self.maxy = self.screen.get_height()
        #minimums assumed to be zero

    def update(self, commands, gravity):
        self.gravity = gravity
        
        if gravity:
            #todo: collision detection for standing on platforms
            #currently always in freefall
            self.dy -= self.g
        else:
            self.dx = 0
            self.dy = 0
            #Zero out velocities, then add or subtract = simplest way to deal
            #with holding down both left and right keys
            if K_RIGHT in commands:
                self.dx += self.walkSpeed
            if K_LEFT in commands:
                self.dx -= self.walkSpeed
            if K_UP in commands:
                self.dy -= self.walkSpeed
            if K_DOWN in commands:
                self.dy += self.walkSpeed
        
        self.x += self.dx
        self.y += self.dy
        
        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

    def draw(self):
        #Dummy draw method
        if self.gravity:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), 5)
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 5)
