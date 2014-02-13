import sys
import pygame
from pygame.locals import *

def load_image(name, colorkey=(255, 0, 255)):
    #fullname = os.path.join('data', name)
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cant load ", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_spritesheet(name, (width, height),  frames, colorkey=(255, 0, 255)):
    sheet, rect = load_image(name, colorkey)
    result = []
    for i in range(frames):
        result.append(pygame.Surface((width, height)).convert())
        result[i].fill(colorkey)
        result[i].blit(sheet, (0,0), Rect(i*width, 0, width, height) )
        result[i].set_colorkey(colorkey, RLEACCEL)
    return result, result[0].get_rect()


    

