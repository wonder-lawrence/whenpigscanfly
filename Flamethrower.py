import pygame
from pygame.locals import *
from math import atan2, radians, degrees, cos, sin

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Flamethrower(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
        	image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__ (self, screen, x, y):
        self.screen = screen
        self.x = x + 40
        self.y = y + 45
        
        self.theta = -30
        self.thetaMin = -74
        self.thetaMax = 90

        self.image_dims = (74, 36)
        self.base_image = self.load_image("backburner.png")
        self.base_image = pygame.transform.smoothscale(self.base_image, self.image_dims)
        self.image = self.base_image
        
        
        #Currently unused
        self.active = True
        
    def rotateTo(self, (player_x, player_y), (mouse_x, mouse_y)):
        if player_y != mouse_y: #Avoid zero divide
            self.theta = degrees(atan2((player_x - mouse_x),(player_y - mouse_y)))  
            self.theta += 105 #Magic constant
            if self.thetaMin < self.theta < self.thetaMax:
                self.image = pygame.transform.rotate(self.base_image, self.theta)
     
    def update(self, player_x, player_y):
        if self.thetaMin< self.theta < self.thetaMax:
            self.x = player_x + 40
            self.y = player_y + 45
        
            if self.theta > 0:
                self.y -= sin(radians(self.theta))*self.image_dims[0]
            else:
                self.x += sin(radians(self.theta))*self.image_dims[1]


    def kill(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
