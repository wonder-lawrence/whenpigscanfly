import pygame, sys, os, random
from pygame.locals import *

class Pig(pygame.sprite.Sprite):
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

        #Width and height (curently of ellipse, later of sprite image)
        self.image_w = 100
        self.image_h = 40

        self.active = True

        #Speed
        self.flyingSpeed = 6
        self.walkingSpeed = 5
        self.dx = self.walkingSpeed
        self.dy = 0

        #Boundaries
        self.maxx = self.screen.get_width()
        self.maxy = self.screen.get_height()
        #minimums assumed to be zero

    def update(self):
        #Update position
        self.x += self.dx
        self.y += self.dy

        #Don't go off edge of screen, change direction instead
        if self.x < 0 or self.x + self.image_w > self.maxx:
            self.dx *= -1

        if self.y < 0 or self.y + self.image_h > self.maxy:
            self.dy *= -1

        self.rect = pygame.Rect(self.x, self.y, self.image_w, self.image_h)

    def kill(self):
        self.active = False

    def draw(self):
        #Dummy draw method
        if self.active:
            pygame.draw.ellipse(self.screen, (255, 192, 203), self.rect)
