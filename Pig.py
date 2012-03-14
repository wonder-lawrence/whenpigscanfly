import pygame, sys, os, random
from pygame.locals import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Pig(pygame.sprite.Sprite):
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
       
        #Flying and walking speed
        self.flyingSpeed = 6
        self.walkingSpeed = 10

        #Assume no gravity and set velocity accordingly
        #May need to pass in gravity eventually
        self.gravity = False
        self.dx = 0
        self.dy = self.walkingSpeed

        #Boundaries
        self.maxx = self.screen.get_width()
        self.maxy = self.screen.get_height()
        #minimums assumed to be zero

    def update(self, gravity):
        if gravity != self.gravity:
            self.gravity = gravity
            if gravity: #new gravity
                self.dx = self.flyingSpeed
                self.dy = 0
            else: #newly no gravity
                self.dx = 0
                self.dy = self.walkingSpeed

        #Update position
        self.x += self.dx
        self.y += self.dy

        #Don't go off edge of screen, change direction instead
        bounded = bound(0, self.x, self.maxx)
        if self.x != bounded:
            self.dx *= -1
            self.x = bounded

        bounded = bound(0, self.y, self.maxy)
        if self.y != bounded:
            self.dy *= -1
            self.y = bounded
        
    def draw(self):
        #Dummy draw method
        pygame.draw.circle(self.screen, (255, 192, 203), (self.x, self.y), 5)
