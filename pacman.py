import pygame as pg
from settings import Settings

class Pacman:
    def __init__(self):
        pass

    pacman_up = [pg.transform.rotozoom(pg.image.load(f'images/pacman_up{n}.png'), 0, 1) for n in range(2)]
    pacman_down = [pg.transform.rotozoom(pg.image.load(f'images/pacman_down{n}.png'), 0, 1) for n in range(2)]
    pacman_left = [pg.transform.rotozoom(pg.image.load(f'images/pacman_left{n}.png'), 0, 1) for n in range(2)]
    pacman_right = [pg.transform.rotozoom(pg.image.load(f'images/pacman_right{n}.png'), 0, 1) for n in range(2)]
   
    def update(self):
        pass
    def draw(self):
        pass
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