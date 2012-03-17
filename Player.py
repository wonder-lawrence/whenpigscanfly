import pygame
from pygame.locals import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Player(pygame.sprite.Sprite):

    def load_image(self, image_name):
        try:
        	image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__ (self, screen, x, y):
        self.screen = screen
        self.image = self.load_image("pyro.png")
        self.x = x
        self.y = y
        self.theta = -30

        self.dx = 0
        self.dy = 0

        self.image_w = 50
        self.image_h = 93
        self.image = pygame.transform.smoothscale(self.image, (self.image_w, self.image_h))

        #Gravitational acceleration
        self.g = 1

        #Speeds
        self.jumpSpeed = -20
        self.walkSpeed = 10

        #Prevent double jumps from holding key down for more than one frame
        self.jumped = False

        #Boundaries
        self.maxx = self.screen.get_width() - self.image_w
        self.maxy = self.screen.get_height() - self.image_h
        #minimums assumed to be zero

        #Currently unused
        self.active = True
        
    def update(self, commands):
        
        #todo: collision detection for standing on platforms
        #currently always in freefall
        self.dx = 0
        if self.y == self.maxy: #Todo: stop falling on blocks, not just botton of screen
            self.dy = 0
            self.jumped = False
        else:
            self.dy += self.g

        if K_RIGHT in commands or K_d in commands:
            self.dx += self.walkSpeed
        if K_LEFT in commands or K_a in commands:
            self.dx -= self.walkSpeed
        if K_UP in commands or K_w in commands:
            if not self.jumped:
                self.dy += self.jumpSpeed
                self.jumped = True
               
        #Unused 
        if K_DOWN in commands or K_s in commands:
            pass

        self.x += self.dx
        self.y += self.dy
       
        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

        self.rect = pygame.Rect(self.x, self.y, self.image_w, self.image_h)

    def kill(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

