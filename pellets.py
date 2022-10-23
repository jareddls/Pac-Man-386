import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, col):
        self.name = PELLET
        self.position = Vector2(col * TILE_WIDTH, row * TILE_HEIGHT)
        self.color = WHITE
        self.r = int(2 * TILE_WIDTH / 16)
        self.collide_r = int(2 * TILE_WIDTH / 16)
        self.points = 10
        self.visible = True
        
    def draw(self, screen):
        if self.visible:
            adjusted = Vector2(TILE_WIDTH, TILE_HEIGHT) / 2
            p = self.position + adjusted
            pygame.draw.circle(screen, self.color, p.asInt(), self.r)

#the class where pacman eats this type of pellet to gain the ability to eat ghosts
class PowerPellet(Pellet):
    def __init__(self, row, col):
        Pellet.__init__(self, row, col)
        self.name = POWERPELLET
        self.r = int(8 * TILE_WIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer= 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0

class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pellet_list = []
        self.powerpellets = []
        self.create_pellet_list(pelletfile)
        self.num_eaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def create_pellet_list(self, pelletfile):
        data = self.read_pellet_file(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.powerpellets.append(pp)
                    
    def read_pellet_file(self, text_file):
        return np.loadtxt(text_file, dtype='<U1')
    
    def is_empty(self):
        if len(self.pellet_list) == 0:
            return True
        return False
    
    def draw(self, screen):
        for pellet in self.pellet_list:
            pellet.draw(screen)
