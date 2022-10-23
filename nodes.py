import pygame as pg
from vector import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.neighbors = {UP: None, DOWN: None, RIGHT: None, LEFT: None, PORTAL: None}
        self.access = {UP:      [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN:    [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT:   [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT:    [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def deny_acc(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allow_acc(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def draw(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pg.draw.line(screen, WHITE, line_start, line_end, 4)
                pg.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodes_look_up = {}

        # + is the node where pacman can change direction
        # x are the walls
        # . are the pellets
        # n is placed on nodes
        # we place pellets on . and +
        # we place power pellets on p/P
        #   P is for placement on nodes and p is for placement on paths
        # | and - are also placed on paths
        self.node_symbols = ['+', 'P', 'n']
        self.path_symbols = ['.', '-', '|', 'p']
        
        data = self.read_maze_file(level)

        self.create_node_table(data)
        self.connect_h(data)
        self.connect_v(data)

        self.home_key = None
    
    def deny_acc(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.deny_acc(direction, entity)

    def allow_acc(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.allow_acc(direction, entity)

    def deny_acc_list(self, col, row, direction, entities):
        for entity in entities:
            self.deny_acc(col, row, direction, entity)

    def allow_acc_list(self, col, row, direction, entities):
        for entity in entities:
            self.allow_acc(col, row, direction, entity)

    def deny_home_acc(self, entity):
        self.nodes_look_up[self.home_key].deny_acc(DOWN, entity)

    def allow_home_acc(self, entity):
        self.nodes_look_up[self.home_key].allow_acc(DOWN, entity)

    def deny_home_acc_list(self, entities):
        for entity in entities:
            self.deny_home_acc(entity)

    def allow_home_acc_list(self, entities):
        for entity in entities:
            self.allow_home_acc(entity)

    def create_home_nodes(self, x_off, y_off):
        home_data = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.create_node_table(home_data, x_off, y_off)
        self.connect_h(home_data, x_off, y_off)
        self.connect_v(home_data, x_off, y_off)
        self.home_key = self.construct_key(x_off + 2, y_off)
        return self.home_key

    def connect_home_nodes(self, home_key, otherkey, direction):     
        key = self.construct_key(*otherkey)
        self.nodes_look_up[home_key].neighbors[direction] = self.nodes_look_up[key]
        self.nodes_look_up[key].neighbors[direction * -1] = self.nodes_look_up[home_key]

    def read_maze_file(self, text_file):
        #dtype is there so we don't encounter problems when there's different types
        return np.loadtxt(text_file, dtype = '<U1')

    def create_node_table(self, data, x_off = 0, y_off = 0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_off, row + y_off)
                    self.nodes_look_up[(x, y)] = Node(x, y)

    def connect_h(self, data, x_off = 0, y_off = 0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_off, row + y_off)
                    else:
                        otherkey = self.construct_key(col + x_off, row + y_off)
                        self.nodes_look_up[key].neighbors[RIGHT] = self.nodes_look_up[otherkey]
                        self.nodes_look_up[otherkey].neighbors[LEFT] = self.nodes_look_up[key]
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_v(self, data, x_off = 0, y_off = 0):
        data_table = data.transpose()
        for col in list(range(data_table.shape[0])):
            key = None
            for row in list(range(data_table.shape[1])):
                if data_table[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_off, row + y_off)
                    else:
                        otherkey = self.construct_key(col + x_off, row + y_off)
                        self.nodes_look_up[key].neighbors[DOWN] = self.nodes_look_up[otherkey]
                        self.nodes_look_up[otherkey].neighbors[UP] = self.nodes_look_up[key]
                        key = otherkey
                elif data_table[col][row] not in self.path_symbols:
                    key = None

    def construct_key(self, x, y):
        return x * TILE_WIDTH, y * TILE_HEIGHT
   
    def get_node_from_pixels(self, x_pix, y_pix):
        if (x_pix, y_pix) in self.nodes_look_up.keys():
            return self.nodes_look_up[(x_pix, y_pix)]
        return None

    def get_node_from_tiles(self, col, row):
        x, y = self.construct_key(col, row)
        if (x, y) in self.nodes_look_up.keys():
            return self.nodes_look_up[(x, y)]
        return None

    def get_start_temp_node(self):
        nodes = list(self.nodes_look_up.values())
        return nodes[0]

    def set_portal_pair(self, pair1, pair2):
        key_1 = self.construct_key(*pair1)
        key_2 = self.construct_key(*pair2)
        if key_1 in self.nodes_look_up.keys() and key_2 in self.nodes_look_up.keys():
            self.nodes_look_up[key_1].neighbors[PORTAL] = self.nodes_look_up[key_2]
            self.nodes_look_up[key_2].neighbors[PORTAL] = self.nodes_look_up[key_1]

    def draw(self, screen):
        for node in self.nodes_look_up.values():
            node.draw(screen)