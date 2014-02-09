import sys, pygame
import futils
import pprint
from controller import Controller
from board import Board
from pygame.locals import *
from pygame.sprite import collide_rect

pp = pprint.PrettyPrinter(indent=2)

def main():
    pygame.init()
    size = width, height = 540, 540
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    controller = Controller(screen, Board(8, 6))

    while 1:
        clock.tick(60)
        clicked = False
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               return 
            if event.type == MOUSEBUTTONUP:
                clicked = True

        mpos = pygame.mouse.get_pos()
        controller.process(mpos, clicked)

        #Displaying
        screen.fill(black)
        controller.trigger_draw()
        pygame.display.flip()
main()
