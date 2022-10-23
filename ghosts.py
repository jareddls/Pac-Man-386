import pygame as pg
from vector import Vector2
from constants import *
from entity import Entity
from modes import Mode
from sprites import InkySprite, PinkySprite, BlinkySprite, ClydeSprite

class Ghost(Entity):
    def __init__(self, node, pacman = None, blinky = None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.objective = Vector2()
        self.dir_meth = self.obj_dir
        self.pacman = pacman
        self.mode = Mode(self)

        self.blinky = blinky
        self.home_node = node

        self.sprites = None

    def scatter(self):
        self.objective = Vector2()

    def chase(self):
        self.objective = self.pacman.position

    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.dir_meth = self.random_direction 

    def normal_mode(self):
        self.set_speed(100)
        self.dir_meth = self.obj_dir
        self.home_node.deny_acc(DOWN, self)
        
        
    def spawn(self):
        self.objective = self.spawn_node.position

    def set_spawn_node(self, node):
        self.spawn_node = node

    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.dir_meth = self.obj_dir
            self.spawn()

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.dir_meth = self.obj_dir

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

class Blinky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = BlinkySprite(self)

class Pinky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = PinkySprite(self)

    def scatter(self):
        self.objective = Vector2(TILE_WIDTH * NUM_COLS, 0)

    def chase(self):
        self.objective = self.pacman.position + self.pacman.dirs[self.pacman.dir] * TILE_WIDTH * 4

class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = InkySprite(self)

    def scatter(self):
        self.objective = Vector2(TILE_WIDTH * NUM_COLS, TILE_HEIGHT * NUM_ROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.dirs[self.pacman.dir] * TILE_WIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.objective = self.blinky.position + vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = ClydeSprite(self)

    def scatter(self):
        self.objective = Vector2(0, TILE_HEIGHT * NUM_ROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILE_WIDTH * 8)**2:
            self.scatter()
        else:
            self.objective = self.pacman.position + self.pacman.dirs[self.pacman.dir] * TILE_WIDTH * 4

class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
    

    def __iter__(self):
        return iter(self.ghosts)

    def start_freight(self):
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

        pg.mixer.music.stop()
        pg.mixer.music.load('sounds/ghost_freight.wav')
        pg.mixer.music.play(-1)

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self):
        for ghost in self:
            ghost.points *= 2

    def reset_points(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def draw(self, screen):
        for ghost in self:
            ghost.draw(screen)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)