import pygame
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
        if isinstance(self.entity, Rook):
            print 'im rook'
            laser = Laser(self.entity.rect.center, self.context.board.get_pos(position))
            self.context.animation_group.add(laser)
            return
        if position in self.movement_targets:
            nade = Nade(self.entity.rect.center, self.context.board.get_pos(position))
            self.context.animation_group.add(nade)
    
    def click_right_occupied_tile(self, position, entities):
        if position in self.movement_targets:
            nade = Nade(self.entity.rect.center, self.context.board.get_pos(position))
            self.context.animation_group.add(nade)
            for e in entities:
                e.take_damage(self.entity.get_damage())

class Marker(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image('images/marker.png', -1)
        self.rect.center = position
