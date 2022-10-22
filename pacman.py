import pygame as pg
from pygame.sprite import Sprite
from settings import Settings
from timer import Timer 

class Pacman (Sprite):

    pacman_up = [pg.transform.rotozoom(pg.image.load(f'images/pacman_up{n}.png'), 0, 1) for n in range(2)]
    pacman_down = [pg.transform.rotozoom(pg.image.load(f'images/pacman_down{n}.png'), 0, 1) for n in range(2)]
    pacman_left = [pg.transform.rotozoom(pg.image.load(f'images/pacman_left{n}.png'), 0, 1) for n in range(2)]
    pacman_right = [pg.transform.rotozoom(pg.image.load(f'images/pacman_right{n}.png'), 0, 1) for n in range(2)]

    pacman_death = [pg.transform.rotozoom(pg.image.load(f'images/pacman_death{n}.png'), 0, 1) for n in range(12)]
    
    def __init__(self, screen, maze):
        super().__init__()
        self.screen = screen
        self.maze = maze
        self.image = pg.image.load('images/pacman_right0.png')
        self.rect = self.image.get_rect()

        
        self.spawn_info = self.maze.player_spawn[1]
        self.tile = self.maze.player_spawn[0]
        self.rect.centerx, self.rect.centery = self.spawn_info
        self.dying = False

        


   
    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def coin_collision(self):
        pass
    def delete_coin(self):
        pass
    def move(self):
        pass
    def get_pixel_position(self):
        pass

    #kind of for use in conjunction with hit_wall, so that we know which ways we can go?
    def  moveable_direction(self):
        pass
    #should probably return true or false so we know if we can move or not
    def hit_wall(self):
        pass