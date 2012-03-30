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
        self.updateRects()

        #Gravitational acceleration
        self.g = 1

        #Speeds
        self.jumpSpeed = -20
        self.walkSpeed = 10
        self.floatSpeed = 1 #x movement while jumping
        #Prevent double jumps from holding key down for more than one frame
        self.falling = False
        self.collided = False
        self.supported = False

        #Boundaries
        self.maxx = self.screen.get_width() - self.image_w
        self.maxy = self.screen.get_height() - self.image_h
        self.maxdx = 12
        self.maxdy = 15
        #minimums assumed to be zero

        self.flamethrower = Flamethrower(self.screen, self.x, self.y)

        self.debug = False

        #Currently unused
        self.active = True

    def updateRects(self):
        self.rect = pygame.Rect(self.x, self.y, self.image_w, self.image_h)
        self.standRect = pygame.Rect(self.x, self.y+1, self.image_w, self.image_h)

    def update(self, commands):
        if self.y == self.maxy:
            self.falling = False

        if self.falling:
            self.dy += self.g
            xspeed = self.floatSpeed
        else:
            self.dx = self.dy = 0
            xspeed = self.walkSpeed

        if K_RIGHT in commands or K_d in commands:
            self.dx += xspeed
        if K_LEFT in commands or K_a in commands:
            self.dx -= xspeed
        if K_UP in commands or K_w in commands:
            if not self.falling:
                self.dy += self.jumpSpeed
                self.falling = True
               
        #Unused 
        if K_DOWN in commands or K_s in commands:
            pass
        
        self.dx = bound(-self.maxdx, self.dx, self.maxdx)
        self.dy = bound(self.jumpSpeed, self.dy, self.maxdy)

        self.x += self.dx
        self.y += self.dy
       
        #Don't go off edge of screen
        boundx = bound(0, self.x, self.maxx)
        if boundx != self.x:
            self.x = boundx
            self.dx = 0

        boundy = bound(0, self.y, self.maxy)
        if boundy != self.y:
            self.y = boundy
            self.dy = 0

        self.updateRects()
        self.collided = False
        self.supported = False
        self.flamethrower.update(self.x, self.y)

    def kill(self):
        pass

    def collideWith(self, block):
        fudgeFactor = 60
        bottom = self.y + self.image_h + self.dy
        if self.debug:
            self.bottom = bottom
        if pygame.sprite.collide_rect(self, block):
            if self.dy == 0:
                self.collideSide(block)
                if self.debug:
                    print "Side 1"
            elif bottom - fudgeFactor < block.rect.top < bottom + fudgeFactor:
                self.collideTop(block)
                if self.debug:
                    print "Top"
            elif self.y - self.dy - fudgeFactor < block.rect.bottom:
                self.collideBottom(block)
                if self.debug:
                    print "Bottom"
            else:
                self.collideSide(block)
                if self.debug:
                    print "Side 2"
        elif self.y + self.image_h + 1 == block.rect.top:
            self.supported = True

    def doneWithCollides(self):
        if not self.supported:
            self.falling = True

    def collideTop(self, block):
        if not self.collided and self.falling:
            self.dx = self.dy = 0
            self.y = block.rect.top - self.image_h
            self.falling = False
            self.collided = True
            self.updateRects()
            self.flamethrower.update(self.x, self.y)
        self.supported = True

    def collideSide(self, block):
        if not self.collided:
            if self.falling:
                speed = self.dx
            else:
                speed = 0
            if self.dx < 0:
                self.dx = speed
                self.x = block.rect.right
            else:
                self.dx = -speed
                self.x = block.rect.left - self.image_w - 1
            self.collided = True
            self.updateRects()
            self.flamethrower.update(self.x, self.y)

    def collideBottom(self, block):
        if self.falling and not self.collided:
            self.dy *= -1
            self.y = block.rect.bottom
            self.updateRects()
            self.collided = True
            self.flamethrower.update(self.x, self.y)

    def shoot(self):
        return self.flamethrower.shoot()

    def rotateFlamethrower(self, mouse_pos):
        self.flamethrower.rotateTo((self.x, self.y), mouse_pos)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.flamethrower.draw()

        if self.debug:
            fudgeFactor = 60
            top =  self.y - self.dy - fudgeFactor 
            bot1 = self.bottom - fudgeFactor
            bot2 = self.bottom + fudgeFactor
            pygame.draw.line(self.screen, (255, 0, 0), (0, top), (900, top))
            pygame.draw.line(self.screen, (0, 0, 255), (0, bot1), (900, bot1))
            pygame.draw.line(self.screen, (0, 255, 0), (0, bot2), (900, bot2))
