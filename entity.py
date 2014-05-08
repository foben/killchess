import math
import pygame
import futils
from random import randint
from math import sqrt
from pygame.locals import *
from pygame.sprite import collide_rect
from pygame import Surface

class Entity(pygame.sprite.Sprite):
    def __init__(self, image='images/dude.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image(image, (255, 0, 255))
        self.movelist = [ (-1, -1), (-1, 0), (-1, 1),\
                          (0, -1), (0, 1),\
                          (1, -1), (1, 0), (1, 1)  ]
        self.health = 2

    def get_name(self):
        return "Dude"

    def get_movements(self):
        return self.movelist

    def get_health(self):
        return self.health

    def get_damage(self):
        return 1

    def take_damage(self, amount):
        print "taking %s damage" % amount
        self.health -= amount

    def update(self):
        if self.health <= 0:
            self.die()

    def die(self):
        self.kill()

class Knight(Entity):
    def __init__(self):
        Entity.__init__(self, image='images/knight.png')
        self.movelist = [ (-2,1), (-2, -1), (-1, -2), (1, -2),\
                          (2, -1), (2, 1), (-1, 2), (1, 2) ]

    def get_name(self):
        return "Knight"

class Rook(Entity):
    def __init__(self):
        Entity.__init__(self, image='images/rook.png')

    def get_movements(self):
        result = [ (mod*x, 0) for x in range(1,8) for mod in [1, -1]]
        result += [ (0, mod*x) for x in range(1,8) for mod in [1, -1]]
        return result

class SheetAnimation(pygame.sprite.Sprite):
    def __init__(self, width=35, height=35, frame_count=1, \
            frame_length=5, sheet='images/sheet_nade.png', loops=-1):
        pygame.sprite.Sprite.__init__(self)
        self.frames, self.rect = \
                futils.load_spritesheet(sheet, (width, height), frame_count)
        self.frame = 0
        self.image = self.frames[self.frame].copy()
        self.total_frames = len(self.frames)
        self.tick_count = 0
        self.frame_length = frame_length
        self.loops = loops
        self.loop = 0

    def update(self):
        self.tick_count += 1
        if self.tick_count % self.frame_length == 0:
            self.frame += 1
            if self.frame >= self.total_frames:
                self.loop += 1
                self.frame = 0
                if self.loops > -1 and self.loop >= self.loops:
                    self.kill()
            self.image = self.frames[self.frame].copy()
            ckey = self.image.get_colorkey()
            self.image = self.manipulate_frame(self.image)
            self.image.set_colorkey(ckey)
        self.tick()

    def manipulate_frame(self, frame):
        return frame

    def tick(self):
        pass

class Explosion(SheetAnimation):
    def __init__(self, position):
        SheetAnimation.__init__(self, 40, 40, 7, 5, 'images/sheet_explosion.png', 1)
        self.rect.center = position

class Nade(SheetAnimation):
    def __init__(self, start_pos, end_pos):
        SheetAnimation.__init__(self, 35, 35, 3, 4, 'images/sheet_nade.png')
        self.max_ticks = 75.0
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.tick_count = 0
        self.rect.center = start_pos
        self.stepx = (end_pos[0] - start_pos[0])/self.max_ticks
        self.stepy = (end_pos[1] - start_pos[1])/self.max_ticks
        self.cx = 0.0 + self.rect.centerx
        self.cy = 0.0 + self.rect.centery
   
    def tick(self):
        self.cx += self.stepx
        self.cy += self.stepy
        self.rect.centerx = self.cx
        self.rect.centery = self.cy
        if self.tick_count >= self.max_ticks:
            for g in self.groups():
                g.add(Explosion(self.rect.center))
            self.kill()

    def manipulate_frame(self, frame):
        scalef = 1 + (1 - (math.fabs(self.tick_count - (self.max_ticks/2))/(self.max_ticks/2)))*2
        nwidth = int(self.rect.width * scalef)
        nheight = int(self.rect.height * scalef)
        return pygame.transform.scale(frame, (nwidth, nheight))

class Laser(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos):
        pygame.sprite.Sprite.__init__(self)
        self.ticks = 0
        #self.image, self.rect = futils.load_image('images/laserh.png')
        self.laserimage, self.laserrect = futils.load_image('images/laserh.png')
        self.width = max(math.fabs(end_pos[0] - start_pos[0]), 35)
        self.height = max( math.fabs(end_pos[1] - start_pos[1]), 15)
        self.image = Surface((self.width, self.height))
        self.image.fill((255, 155, 255))
        self.rect = pygame.Rect((0,0), (self.width, self.height))
        if start_pos[1] == end_pos[1]:
            if start_pos[0] < end_pos[0]:
                self.rect.midleft = start_pos
                self.rect.midright = end_pos
            else:
                self.rect.midleft = end_pos
                self.rect.midright = start_pos
            for x in range(int(self.width)):
                self.image.blit(self.laserimage, (x,0))
                
        elif start_pos[0] == end_pos[0]:
            if start_pos[1] < end_pos[1]:
                self.rect.midtop = start_pos
                self.rect.midbottom = end_pos
            else:
                self.rect.midtop = end_pos
                self.rect.midbottom = start_pos


    def update(self):
        self.ticks += 1
        transp = self.ticks * 15 
        self.image.set_alpha(255 - transp)
        if self.ticks >= 20: self.kill()

