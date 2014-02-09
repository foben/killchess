import pygame
import futils
from pygame.locals import *
from pygame.sprite import collide_rect

class Entity(pygame.sprite.Sprite):
    def __init__(self, image='images/dude.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image(image, (255, 0, 255))
        self.movelist = [ (-1, -1), (-1, 0), (-1, 1),\
                          (0, -1), (0, 1),\
                          (1, -1), (1, 0), (1, 1)  ]

    def get_name(self):
        return "Dude"

    def get_movements(self):
        return self.movelist


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



