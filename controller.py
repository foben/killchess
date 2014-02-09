import pygame
from board import Board
from entity import *

class Controller:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.highlighter, self.highlighterrect = \
                futils.load_image('images/tile_hover.png', (255, 0, 255))
        self.state = {'state': 'selection', 'substate': None}
        self.marker_group = pygame.sprite.Group()
    

    def update(self):
        return

    def trigger_draw(self):
        self.board.draw(self.screen)
        self.screen.blit(self.highlighter, self.highlighterrect)
        self.marker_group.draw(self.screen)

    def adjust_highlighter(self, newpos):
        self.highlighterrect.center = newpos 

    def process(self, mpos, clicked):
        hovered_tile = self.board.get_tile_from_position(mpos)
        position = None
        if hovered_tile:
            position = hovered_tile.pos
            self.adjust_highlighter(hovered_tile.rect.center)
        
        if clicked and position:
            self.process_click_on_tile(position)
        
    def process_click_on_tile(self, position):
        #print "before:  %s" % self.state
        if self.state['state'] == "selection" and not self.state['substate']:
            self.process_selection_click(position)
        elif self.state['state'] == "selection" and self.state['substate'] == 'unit':
            self.process_unit_selected_click(position)
        #print "after:  %s" % self.state

    
    def process_unit_selected_click(self, position):
        valids = self.state['targets']
        self.marker_group.empty()
        if position in valids:
            self.board.move_entity(self.state['unit'], position)
            self.clear_state()
        else:
            self.clear_state()

    def process_selection_click(self, position):
        self.marker_group.empty()
        e_group = self.board.get_entities_on_tile(position)
        e_list = e_group.sprites()
        if len(e_list) > 1:
            print "MORE THAN ONE ENTITY HERE!!!!"
            self.clear_state()
            return
        if len(e_list) < 1:
            print "No entity here"
            self.clear_state()
            return
        entity = e_list[0]
        mv = entity.get_movements()
        places = self.get_places(mv, position)
        for p in places:
            marker_position = self.board.get_tile(p).rect.center
            self.marker_group.add(Marker(marker_position))
        self.state['targets'] = places
        self.state['unit'] = entity
        self.state['substate'] = 'unit'

    def clear_state(self):
        self.state = {'state': 'selection', 'substate':None }

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

class State:
    def click_empty_tile(self, position):
        print "%s : empty" % position
    def click_occupied_tile(self, position, entities):
        print "%s : occupied with %s" % (position, entities)


class Marker(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image('images/marker.png', -1)
        self.rect.center = position
