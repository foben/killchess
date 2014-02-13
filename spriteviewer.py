import sys, pygame
import futils
import pprint
import sys
from entity import SheetAnimation, Explosion
from pygame.locals import *
from pygame.sprite import collide_rect

pp = pprint.PrettyPrinter(indent=2)

def main():
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    frames = int(sys.argv[3])
    framelength = int(sys.argv[4])
    sheet = sys.argv[5]


    pygame.init()
    size = width*2, height*2 
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    anims = pygame.sprite.Group()


    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               return 
        if len(anims.sprites()) < 1:
            anim = SheetAnimation(width, height, frames, framelength, sheet)
            anim.rect.center = (width, height)
            anims.add(anim)

        #Displaying
        screen.fill(black)
        anims.update()
        anims.draw(screen)

        pygame.display.flip()
main()



