import pygame as pg
from constants import *
import numpy as np
from timer import Timer

BASE_TILE_WIDTH = 16
BASE_TILE_HEIGHT = 16

DEATH = 5

class SpriteSheet(object):
    def __init__(self):
        self.sheet = pg.image.load("images/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASE_TILE_WIDTH * TILE_WIDTH)
        height = int(self.sheet.get_height() / BASE_TILE_HEIGHT * TILE_HEIGHT)
        self.sheet = pg.transform.scale(self.sheet, (width, height))
        
    def get_image(self, x, y, width, height):
        x *= TILE_WIDTH
        y *= TILE_HEIGHT
        self.sheet.set_clip(pg.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class PacmanSprites(SpriteSheet):
    def __init__(self, entity):
        SpriteSheet.__init__(self)
        self.entity = entity
        self.entity.image = self.get_start_image()   

        self.timer = {}
        self.define_timer()
        self.stop_image = (8,0)   

    def get_start_image(self):
        return self.get_image(8, 0)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

    def define_timer(self):
        self.timer[LEFT] = Timer(((8,0), (0, 0), (0, 2), (0, 0)))
        self.timer[RIGHT] = Timer(((10,0), (2, 0), (2, 2), (2, 0)))
        self.timer[UP] = Timer(((10,2), (6, 0), (6, 2), (6, 0)))
        self.timer[DOWN] = Timer(((8,2), (4, 0), (4, 2), (4, 0)))
        self.timer[DEATH] = Timer(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, dt):
        if self.entity.alive == True:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(*self.timer[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(*self.timer[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(*self.timer[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.dir == UP:
                self.entity.image = self.get_image(*self.timer[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.dir == STOP:
                self.entity.image = self.get_image(*self.stop_image)
        else:
           self.entity.image = self.get_image(*self.timer[DEATH].update(dt))

    def reset(self):
        for key in list(self.timer.keys()):
            self.timer[key].reset()

class InkySprite(SpriteSheet):
    def __init__(self, entity):
        SpriteSheet.__init__(self)
        self.x = {BLINKY: 0,PINKY: 2,INKY: 4,CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()
               
    def get_start_image(self):
        return self.get_image(self.x[INKY], 4)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.dir == UP:
                self.entity.image = self.get_image(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.dir == UP:
               self.entity.image = self.get_image(8, 4)

class ClydeSprite(SpriteSheet):
    def __init__(self, entity):
        SpriteSheet.__init__(self)
        self.x = {BLINKY: 0,PINKY: 2,INKY: 4,CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()
               
    def get_start_image(self):
        return self.get_image(self.x[CLYDE], 4)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.dir == UP:
                self.entity.image = self.get_image(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.dir == UP:
               self.entity.image = self.get_image(8, 4)

class BlinkySprite(SpriteSheet):
    def __init__(self, entity):
        SpriteSheet.__init__(self)
        self.x = {BLINKY: 0,PINKY: 2,INKY: 4,CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()
               
    def get_start_image(self):
        return self.get_image(self.x[BLINKY], 4)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.dir == UP:
                self.entity.image = self.get_image(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.dir == UP:
               self.entity.image = self.get_image(8, 4)

class PinkySprite(SpriteSheet):
    def __init__(self, entity):
        SpriteSheet.__init__(self)
        self.x = {BLINKY: 0,PINKY: 2,INKY: 4,CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()
               
    def get_start_image(self):
        return self.get_image(self.x[PINKY], 4)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.dir == UP:
                self.entity.image = self.get_image(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.dir == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.dir == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.dir == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.dir == UP:
               self.entity.image = self.get_image(8, 4)

class FruitSprites(SpriteSheet):
    def __init__(self, entity, level):
        SpriteSheet.__init__(self)
        self.entity = entity
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        self.entity.image = self.get_start_image(level % len(self.fruits))


    def get_start_image(self, key):
        return self.get_image(*self.fruits[key])

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

class LifeSprites(SpriteSheet):
    def __init__(self, numlives):
        SpriteSheet.__init__(self)
        self.reset_lives(numlives)

    def remove_image(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def reset_lives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.get_image(0,0))

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)

class MazeSprites(SpriteSheet):
    def __init__(self, mazefile, rot_file):
        SpriteSheet.__init__(self)
        self.data = self.read_maze_file(mazefile)

        self.rot_data = self.read_maze_file(rot_file)

    def get_image(self, x, y):
        return SpriteSheet.get_image(self, x, y, TILE_WIDTH, TILE_HEIGHT)

    def read_maze_file(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def construct_background(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)

                    rot_val = int(self.rot_data[row][col])
                    sprite = self.rotate(sprite, rot_val)

                    background.blit(sprite, (col * TILE_WIDTH, row * TILE_HEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col * TILE_WIDTH, row * TILE_HEIGHT))

        return background

    def rotate(self, sprite, value):
        return pg.transform.rotate(sprite, value * 90)