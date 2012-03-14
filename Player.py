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
        self.image = self.load_image("TimL.png")
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0

        #Gravitational acceleration
        self.g = -1

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
                self.image= self.load_image("TimR.png")
            if K_LEFT in commands:
                self.dx -= self.walkSpeed
                self.image= self.load_image("TimL.png")
            if K_UP in commands:
                self.dy -= self.walkSpeed
            if K_DOWN in commands:
                self.dy += self.walkSpeed
        
        self.x += self.dx
        self.y += self.dy
       
        #Inelastic collisions
        if gravity:
            if self.x != bound(0, self.x, self.maxx):
                self.dx //= -2
            if self.y != bound(0, self.y, self.maxy):
                self.dy //= -2

        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

        self.rect = pygame.Rect(self.x, self.y, 29, 50)

    def kill(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

