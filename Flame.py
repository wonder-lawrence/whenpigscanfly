import pygame
from pygame.locals import *
from math import sin, cos, radians

class Flame(pygame.sprite.Sprite):

    def load_image(self):
        try:
        	image = pygame.image.load("fire1.png")
        except pygame.error, message:
            print "Cannot load image: fire1.png"
            raise SystemExit, message
        return image.convert_alpha()

    def __init__ (self, screen, theta, x, y):
        self.screen = screen
        self.theta = -180 + theta

        self.image = self.load_image()
        self.image = pygame.transform.rotate(self.image, self.theta)
        self.image_dims = self.image.get_width(), self.image.get_height()
        
        self.x = x 
        self. y = y
        self.speed = 10

        self.rect = pygame.Rect((self.x, self.y), self.image_dims)

        self.active = True

    def update(self):
        self.x -= self.speed*cos(radians(self.theta)) 
        self.y += self.speed*sin(radians(self.theta)) 
        self.rect = pygame.Rect((self.x, self.y), self.image_dims)
        self.active = self.rect.colliderect(self.screen.get_rect())

    def kill(self):
        self.active = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
