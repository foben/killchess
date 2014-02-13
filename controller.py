import pygame
from board import Board
from entity import *

class State:
    def __init__(self, context):
        self.context = context
        self.context.clear_markers()
    def click_empty_tile(self, position):
        print "%s : empty" % (position, )
    def click_occupied_tile(self, position, entities):
        print "%s : occupied with %s" % (position, entities)
        entity = entities[0]
        e_movements = entity.get_movements()
        movement_targets = self.context.get_places(e_movements, position)
        self.context.state = UnitSelectedForActionState\
                (self.context, entity, movement_targets)
    def click_right_empty_tile(self, position):
        print "right click on empty"
        self.context.state = State(self.context)
    def click_right_occupied_tile(self, position, entities):
        print "right click on occupied"

class UnitSelectedForActionState(State):
    def __init__(self, context, entity, movement_targets):
        State.__init__(self, context)
        self.entity = entity
        self.movement_targets = movement_targets
        for mt in movement_targets:
            marker_position = self.context.board.get_tile(mt).rect.center
            self.context.add_marker(Marker(marker_position))

    def click_empty_tile(self, position):
        if position in self.movement_targets:
            self.context.board.move_entity(self.entity, position)
            self.context.state = State(self.context)
            self.context.clear_markers()
        else:
            print "Not reachable!"

    def click_occupied_tile(self, position, entities):
        if len(entities) > 1:
            print "MORE THAN ONE ENTITY HERE!!!!"
            return
        if entities[0] == self.entity:
            self.context.state = State(self.context)
            return
        else:
            print "not same"
        print "Can't move here, already occupied!"

    def click_right_empty_tile(self, position):
        if position in self.movement_targets:
            nade = Nade(self.entity.rect.center, self.context.board.get_pos(position))
            self.context.animation_group.add(nade)

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
        return

class Marker(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image('images/marker.png', -1)
        self.rect.center = position
