import pygame, sys, os, random
from pygame.locals import *

class Pig(pygame.sprite.Sprite):
    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

        #Width and height (curently of ellipse, later of sprite image)
        self.image_w = 40
        self.image_h = 100

        self.active = True

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
            (self.image_w, self.image_h) = (self.image_h, self.image_w)
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
            boundBox = pygame.Rect(self.x, self.y, self.image_w, self.image_h)
            pygame.draw.ellipse(self.screen, (255, 192, 203), boundBox)
