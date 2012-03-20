import pygame
from pygame.locals import *
from Flamethrower import Flamethrower

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
        self.floatSpeed = 1 #x movement while jumping
        #Prevent double jumps from holding key down for more than one frame
        self.jumped = False
        self.reversed = False

        #Boundaries
        self.maxx = self.screen.get_width() - self.image_w
        self.maxy = self.screen.get_height() - self.image_h
        self.maxdx = 12
        #minimums assumed to be zero

        self.flamethrower = Flamethrower(self.screen, self.x, self.y)

        #Currently unused
        self.active = True
        
    def update(self, commands):
        if not self.jumped:
            self.dx = 0
            xspeed = self.walkSpeed
        else:
            xspeed = self.floatSpeed
        if self.y == self.maxy or not self.jumped:
            self.dy = 0
            self.jumped = False
        else:
            self.dy += self.g

        if K_RIGHT in commands or K_d in commands:
            self.dx += xspeed
        if K_LEFT in commands or K_a in commands:
            self.dx -= xspeed
        if K_UP in commands or K_w in commands:
            if not self.jumped:
                self.dy += self.jumpSpeed
                self.jumped = True
               
        #Unused 
        if K_DOWN in commands or K_s in commands:
            pass
        
        self.dx = bound(-self.maxdx, self.dx, self.maxdx)

        self.x += self.dx
        self.y += self.dy
       
        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

        self.rect = pygame.Rect(self.x, self.y, self.image_w, self.image_h)
        self.reversed = False
        self.flamethrower.update(self.x, self.y)

    def kill(self):
        pass

    def land(self, block):
        self.y = block.rect.top- self.image_h
        self.dy = self.dx = 0
        self.jumped = False
        self.reversed = True

    def reverse(self):
        if not self.reversed:
            self.dx *= -1
            self.dy *= -1
            self.x += self.dx
            self.y += self.dy
            self.flamethrower.update(self.x, self.y)
            self.reversed = True

    def fall(self):
        if self.x > self.maxx:
            self.jumped = False
            update(self)

    def shoot(self):
        return self.flamethrower.shoot()

    def rotateFlamethrower(self, mouse_pos):
        self.flamethrower.rotateTo((self.x, self.y), mouse_pos)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.flamethrower.draw()
