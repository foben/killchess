import pygame
import futils
from entity import Entity, Knight, Rook
from pygame.locals import *
from pygame.sprite import collide_rect

class BoardTile(pygame.sprite.Sprite):
    def __init__(self, (x, y), image_path='images/tile.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = futils.load_image(image_path)
        self.pos = (x, y)

    def update_image(self, image):
        self.image = futils.load_image(image)[0]

class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entity_map =[[ pygame.sprite.Group() for y in range(height) ] \
                             for x in range(width) ]
        self.board = [[
            BoardTile((x, y), \
                ('images/tileodd.png' if (x+y) % 2 == 0 else 'images/tileeven.png')) \
                for y in range(height) ] \
                for x in range(width) ]
        self.all_tiles_group = pygame.sprite.Group()
        ## Arrange the tiles 
        tilesize = 60
        pos = [tilesize, tilesize]
        for x in range(width):
            for y in range(height):
                tile = self.board[x][y]
                self.all_tiles_group.add(tile)
                tile.rect.center = pos
                pos[1] += tilesize
            pos[0] += tilesize
            pos[1] = tilesize

        self.add_entity(Entity(), (1, 2))
        self.add_entity(Knight(), (4, 3))
        self.add_entity(Rook(), (0, 0))

    def add_entity(self, entity, (x, y)):
        entity.rect.center = self.board[x][y].rect.center
        self.entity_map[x][y].add(entity)

    def update_entities(self):
        for  x in range(len(self.entity_map)):
            for y in range(len(self.entity_map[x])):
                self.entity_map[x][y].update()

    def get_tile_from_position(self, (xa, ya)):
        r = Rect(xa, ya, 1, 1)
        for tile in self.all_tiles_group:
            collides = r.colliderect(tile.rect)
            if collides:
                return tile
        return None

    def get_tile(self, (x, y)):
        return self.board[x][y]

    def get_pos(self, (x, y)):
        return self.get_tile((x, y)).rect.center

    def get_entities_on_tile(self, (x, y)):
        return self.entity_map[x][y]

    def move_entity(self, entity, (x, y)):
        entity.kill()
        self.entity_map[x][y].add(entity)
        entity.rect.center = self.board[x][y].rect.center
        return

    def draw(self, screen):
        self.all_tiles_group.draw(screen)
        for r in self.entity_map:
            for c in r:
                c.draw(screen)
