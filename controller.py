import pygame
from board import Board
from state import *
from entity import *

class Controller:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.highlighter, self.highlighterrect = \
                futils.load_image('images/tile_hover.png', (255, 0, 255))
        self.marker_group = pygame.sprite.Group()
        self.animation_group = pygame.sprite.Group()
        self.state = State(self)
    
    def trigger_draw(self):
        self.board.draw(self.screen)
        self.screen.blit(self.highlighter, self.highlighterrect)
        self.marker_group.draw(self.screen)
        self.animation_group.draw(self.screen)

    def adjust_highlighter(self, newpos):
        self.highlighterrect.center = newpos 

    def clear_markers(self):
        self.marker_group.empty()

    def add_marker(self, marker):
        self.marker_group.add(marker)

    def process(self, mpos, clicked_left, clicked_right):
        hovered_tile = None
        position = None
        hovered_tile = self.board.get_tile_from_position(mpos)
        if hovered_tile:
            position = hovered_tile.pos
            self.adjust_highlighter(hovered_tile.rect.center)
        if clicked_left and clicked_right:
            return
        if clicked_left and position:
            e_group = self.board.get_entities_on_tile(position)
            e_list = e_group.sprites()
            if len(e_list) < 1:
                self.state.click_empty_tile(position)
            elif len(e_list) == 1:
                self.state.click_occupied_tile(position, e_list)
            elif len(e_list) > 1:
                print "MORE THAN ONE ENTITY HERE!!!!"
                return

        if clicked_right and position:
            e_group = self.board.get_entities_on_tile(position)
            e_list = e_group.sprites()
            if len(e_list) < 1:
                self.state.click_right_empty_tile(position)
            elif len(e_list) == 1:
                self.state.click_right_occupied_tile(position, e_list)
            elif len(e_list) > 1:
                print "MORE THAN ONE ENTITY HERE!!!!"
                return   

    def get_places(self, places, position):
        candidates = [ tuple(map(lambda x, y: x+y, p, position)) for p in places ]
        result = list()
        failcount = 0
        for c in candidates:
            if c[0] < 0 or c[0] > self.board.width - 1:
                failcount += 1
                continue
            if c[1] < 0 or c[1] > self.board.height - 1:
                failcount += 1
                continue
            result.append(c)
        print "%s invalid positions removed" % failcount
        return result

    def update(self):
        self.animation_group.update()
        self.board.update_entities()
        return
