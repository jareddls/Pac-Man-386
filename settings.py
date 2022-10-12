import pygame as pg

class Settings():
    def __init__(self):
        #Screen settings
        self.screen_width = 610
        self.screen_height = 670

        #maybe have fps cap so speed can't be weird
        self.fps = 60

        #we have a buffer so that our image doesn't get all jacked up
        self.top_and_bottom_buff = 50
        self.maze_width, self.maze_height = self.screen_width - self.maze_width, self.screen_height - self.maze_height

        self.rows = 30
        self.cols = 28

        self.font = pg.font.Font('fonts/pixel.ttf')
        self.txt_size = 24