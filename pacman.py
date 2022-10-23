from platform import node
import pygame as pg
from vector import Vector2
from constants import *
#import entity because we want to give pacman to inherit the same thing as the ghosts, but pacman will just have more ability
from entity import Entity
from sprites import PacmanSprites
from sound import Sound

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.dirs = {STOP: Vector2(),
                    UP: Vector2(0,-1),
                    DOWN: Vector2(0,1),
                    LEFT: Vector2(-1,0),
                    RIGHT: Vector2(1,0)}

        self.dir = LEFT
        self.set_between_nodes(LEFT)
        self.speed = 100
        #radius
        self.r = 10
        self.sprites = PacmanSprites(self)

        self.color = YELLOW

        self.node = node
        self.set_position()
        self.target = node
        self.collide_r = 5

        self.alive = True
    
    def reset(self):
        Entity.reset(self)
        self.dir = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True
        self.image = self.sprites.get_start_image()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.dir = STOP
        pg.mixer.music.stop()
        pg.mixer.Sound.set_volume(pg.mixer.Sound('sounds/pacman_death.wav'), 0.1)
        pg.mixer.Sound.play(pg.mixer.Sound('sounds/pacman_death.wav'))
    

    #implementing this since it's cleaner than implementing keydown/keyup in pacman
    def get_valid_key(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_UP]:
            return UP
        if key_pressed[pg.K_DOWN]:
            return DOWN
        if key_pressed[pg.K_RIGHT]:
            return RIGHT
        if key_pressed[pg.K_LEFT]:
            return LEFT

        return STOP

    def eat_pellets(self, pellet_list):
        for pellet in pellet_list:
            if self.collide_check(pellet):
                pg.mixer.Sound.set_volume(pg.mixer.Sound('sounds/pacman-pellet-eat.wav'), 0.1)
                pg.mixer.Sound.play(pg.mixer.Sound('sounds/pacman-pellet-eat.wav'))
                return pellet
        return None

    def collide_ghost(self, ghost):
        return self.collide_check(ghost)

    def collide_check(self, other):
        d = self.position - other.position
        dSq = d.magnitudeSquared()
        rSq = (self.collide_r + other.collide_r) ** 2
        if dSq <= rSq:
            return True
        return False

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.dirs[self.dir] * self.speed * dt
        dir = self.get_valid_key()
        if self.reach_end_node():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(dir)
            if self.target is not self.node:
                self.dir = dir
            else:
                self.target = self.get_new_target(self.dir)

            if self.target is self.node:
                self.dir = STOP
            self.set_position()
        else:
            if self.opp_dir(dir):
                self.reverse_dir()
