import pygame as pg
from settings import Settings

class Ghost:
    def __init__(self):
        pass

    def update(self):
        pass
    def draw(self):
        pass

    #important for when we eat the big tic tac that turns them into AI that runs away
    def set_speed(self):
        pass

    def set_traget(self):
        pass

    def moveable_direction(self):
        pass

    def move(self):
        pass


    #all four below work together for the AI of the ghosts
    def get_path_direction(self):
        pass

    def find_next_cell(self):
        pass

    def BFS(self):
        pass

    def get_rand_dir(self):
        pass

    #other
    def get_pixel_position(self):
        pass

    def set_color(self):
        pass

    #for the ghosts
    def set_personality(self):
        pass