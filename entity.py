import pygame as pg
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.dirs = {UP: Vector2(0, -1),
                    DOWN: Vector2(0, 1),
                    RIGHT: Vector2(1, 0),
                    LEFT: Vector2(-1, 0),
                    STOP: Vector2()}
        self.dir = STOP
        self.set_speed(100)
        self.r = 10
        self.collide_r = 5
        self.color = WHITE

        self.visible = True
        self.disable_portal = False

        self.objective = None

        self.dir_meth = self.random_direction

        self.set_start_node(node)

        self.image = None

    def set_start_node(self, node):
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()
          
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def reach_end_node(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2_target = vec1.magnitudeSquared()
            node2_self = vec2.magnitudeSquared()
            return node2_self >= node2_target
        return False

    def reverse_dir(self):
        self.dir *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def opp_dir(self, direction):
        if direction is not STOP:
            if direction == self.dir * -1:
                return True
        return False

    def set_speed(self, speed):
        self.speed = speed * TILE_WIDTH / 16

    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.dir * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.dir * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions)-1)]

    def obj_dir(self, directions):
        dists = []
        for dir in directions:
            vec = self.node.position + self.dirs[dir] * TILE_WIDTH - self.objective
            dists.append(vec.magnitudeSquared())
        idx = dists.index(min(dists))
        return directions[idx]

    def set_between_nodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.set_start_node(self.start_node)
        self.dir = STOP
        self.speed = 100
        self.visible = True

    def update(self, dt):
        self.position += self.dirs[self.dir] * self.speed * dt
         
        if self.reach_end_node():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.dir_meth(directions)   
            if not self.disable_portal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.dir = direction
            else:
                self.target = self.get_new_target(self.dir)

            self.set_position()


    def draw(self, screen):
        if self.visible:
            if self.image is not None:
                adjusted = Vector2(TILE_WIDTH, TILE_HEIGHT) / 2
                p = self.position - adjusted
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pg.draw.circle(screen, self.color, p, self.r)
