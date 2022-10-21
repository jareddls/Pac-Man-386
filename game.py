import pygame as pg
import game_functions as gf
from pacman import *
from ghost import *
from settings import *
from maze import Maze



class Game:

    blackBG = (0,0,0)


    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.maze = Maze(screen=self.screen, maze_map_file='maze.txt')

    def play(self):
        while True:
            gf.sm_events(self)
            self.maze.build_maze()
            self.maze.update()
            pg.display.flip()


def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()