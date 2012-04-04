import pygame, sys, os, random
from pygame.locals import *

class Pig(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
           print "Cannot load image: " + image_name
           raise SystemExit, message
        return image.convert_alpha()
    
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.image = self.load_image("flying_pig1.png")
        self.image = self.image.convert_alpha()
        self.x = x
        self.y = y
        self.active = True

        self.image_w = 30
        self.image_h = 30
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

    def reverse(self):
        self.dx *= -1
        self.dy *= -1

    def draw(self):
        if self.active:
            self.screen.blit(self.image, (self.x, self.y))
