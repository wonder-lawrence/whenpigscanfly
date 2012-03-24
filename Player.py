import pygame
from pygame.locals import *
from Flamethrower import Flamethrower

def bound (lo, val, hi):
    return max(lo, min(val, hi))

def abs (x):                                                                        
    if x < 0:                                                                       
        return -1 * x                                                               
    else:                                                                           
        return x                                                                    
                    
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
        self.falling = False
        self.bounced = False

        #Boundaries
        self.maxx = self.screen.get_width() - self.image_w
        self.maxy = self.screen.get_height() - self.image_h
        self.maxdx = 12
        self.maxdy = 15
        #minimums assumed to be zero

        self.flamethrower = Flamethrower(self.screen, self.x, self.y)

        #Currently unused
        self.active = True
        
    def update(self, commands):
        if self.y == self.maxy:
            self.falling = False

      #  if self.dy == 1:
       #     self.falling = True

        if self.falling:
            self.dy += self.g
            xspeed = self.floatSpeed
        else:
            self.dx = 0
            self.dy = 1
            xspeed = self.walkSpeed

        if K_RIGHT in commands or K_d in commands:
            self.dx += xspeed
        if K_LEFT in commands or K_a in commands:
            self.dx -= xspeed
        if K_UP in commands or K_w in commands:
            if not self.falling:
                self.dy += self.jumpSpeed
                self.falling = True
                self.y -= 1
               
        #Unused 
        if K_DOWN in commands or K_s in commands:
            pass
        
        self.dx = bound(-self.maxdx, self.dx, self.maxdx)
        self.dy = bound(self.jumpSpeed, self.dy, self.maxdy)

        self.x += self.dx
        self.y += self.dy
       
        #Don't go off edge of screen
        self.x = bound(0, self.x, self.maxx)
        self.y = bound(0, self.y, self.maxy)

        self.rect = pygame.Rect(self.x, self.y, self.image_w, self.image_h)
        self.bounced = False
        self.flamethrower.update(self.x, self.y)

    def kill(self):
        pass

    def collideTop(self, block):
        if not self.bounced:
            if self.falling:
                self.dx = 0
                self.dy = 0
                self.y = block.rect.top - self.image_h
                self.falling = False
            else:
                self.y -= 1
            self.bounced = True

    def collideSide(self, block):
        if not self.bounced:
            if self.falling:
                speed = self.floatSpeed
            else:
                speed = 0
            if self.dx < 0:
                self.dx = speed
                self.x = block.rect.right
            else:
                self.dx = -speed
                self.x = block.rect.left - self.image_w - 1
            self.bounced = True

    def collideBottom(self):
        if self.falling and not self.bounced:
            self.dy *= -1
        else:
            pass
        self.bounced = True

    def shoot(self):
        return self.flamethrower.shoot()

    def rotateFlamethrower(self, mouse_pos):
        self.flamethrower.rotateTo((self.x, self.y), mouse_pos)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.flamethrower.draw()
