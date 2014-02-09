import pygame
from board import Board
from entity import *

class State:
    def __init__(self, context):
        self.context = context
    def click_empty_tile(self, position):
        print "%s : empty" % (position, )
    def click_occupied_tile(self, position, entities):
        print "%s : occupied with %s" % (position, entities)
        entity = entities[0]
        e_movements = entity.get_movements()
        movement_targets = self.context.get_places(e_movements, position)
        self.context.state = UnitSelectedForMovementState\
                (self.context, entity, movement_targets)

class UnitSelectedForMovementState(State):
    def __init__(self, context, entity, movement_targets):
        State.__init__(self, context)
        self.entity = entity
        self.movement_targets = movement_targets
        for mt in movement_targets:
            marker_position = self.context.board.get_tile(mt).rect.center
            self.context.marker_group.add(Marker(marker_position))

    def click_empty_tile(self, position):
        if position in self.movement_targets:
            self.context.board.move_entity(self.entity, position)
            self.context.state = State(self.context)
            self.context.marker_group.empty()
        else:
            print "Not reachable!"

    def click_occupied_tile(self, position, entities):
        print "Can't move here, already occupied!"

class Controller:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.highlighter, self.highlighterrect = \
                futils.load_image('images/tile_hover.png', (255, 0, 255))
        self.marker_group = pygame.sprite.Group()
        self.state = State(self)
    
    def trigger_draw(self):
        self.board.draw(self.screen)
        self.screen.blit(self.highlighter, self.highlighterrect)
        self.marker_group.draw(self.screen)

    def adjust_highlighter(self, newpos):
        self.highlighterrect.center = newpos 

    def process(self, mpos, clicked):
        hovered_tile = None
        position = None
        hovered_tile = self.board.get_tile_from_position(mpos)
        if hovered_tile:
            position = hovered_tile.pos
            self.adjust_highlighter(hovered_tile.rect.center)
        if clicked and position:
            e_group = self.board.get_entities_on_tile(position)
            e_list = e_group.sprites()
            if len(e_list) < 1:
                self.state.click_empty_tile(position)
            elif len(e_list) == 1:
                self.state.click_occupied_tile(position, e_list)
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
        return

class Marker(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image('images/marker.png', -1)
        self.rect.center = position
