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
        clicked_left = False
        clicked_right = False
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               return 
            if event.type == MOUSEBUTTONUP:
                button = event.button
                if button == 1:
                    clicked_left = True
                if button == 3:
                    clicked_right = True

        mpos = pygame.mouse.get_pos()
        controller.process(mpos, clicked_left, clicked_right)

        #Displaying
        screen.fill(black)
        controller.update()
        controller.trigger_draw()

        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(str(mpos), 1, (255,255,0))
        screen.blit(label, (5, 5))


        pygame.display.flip()
main()
