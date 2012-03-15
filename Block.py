import pygame
from pygame.locals import *

class Block(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
        	image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__ (self, screen, rect, image_name):
        self.screen = screen
        self.image = self.load_image(image_name)
        self.rect = rect
        self.active = True

    def update(self):
        pass

    def kill(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

