import pygame as pg
from pygame.sprite import Sprite
from settings import Settings
from timer import Timer 

class Pacman (Sprite):

    pacman_up = [pg.transform.rotozoom(pg.image.load(f'images/pacman_up{n}.png'), 0, 1) for n in range(2)]
    pacman_down = [pg.transform.rotozoom(pg.image.load(f'images/pacman_down{n}.png'), 0, 1) for n in range(2)]
    pacman_left = [pg.transform.rotozoom(pg.image.load(f'images/pacman_left{n}.png'), 0, 1) for n in range(2)]
    pacman_right = [pg.transform.rotozoom(pg.image.load(f'images/pacman_right{n}.png'), 0, 1) for n in range(2)]


    
    def __init__(self, settings, screen):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.rect = self.image.get_rect()
    
        self.image = pg.image.load('images/pacman_right0.png')
        
        

    
   
    def update(self):
        self.draw

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

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