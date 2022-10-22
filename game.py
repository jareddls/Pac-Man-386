import pygame as pg
import game_functions as gf
from pacman import Pacman
from ghost import *
from settings import *
from maze import Maze

from sound import Sound
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button

class Game:
    blackBG = (0,0,0)


    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.maze = Maze(screen=self.screen, maze_map_file='maze.txt')
        self.player = Pacman(screen = self.screen, maze = self.maze)

        # self.settings = Settings()
        # size = self.settings.screen_width, self.settings.screen_height, self.settings.maze_width   # tuple

        # self.screen = pg.display.set_mode(size=size)
        # pg.display.set_caption("Pac-Man")
        
        # self.sound = Sound(bg_music="sounds/pacman_beginning.wav")
        # self.stats = GameStats(settings=self.settings)
        # self.scoreboard = Scoreboard(game=self, stats=self.stats, sound=self.sound)  
        # self.play_button = Button(self.settings, self.screen, "PLAY", 305, 550, 24)

    def play(self):
        while True:
            gf.sm_events(self)
            self.maze.build_maze()
            self.maze.update()
            self.player.draw()
            pg.display.flip()


            # gf.check_events(settings=self.settings, sound=self.sound, screen=self.screen, stats=self.stats, sb=self.scoreboard, play_button=self.play_button)

            # if self.stats.game_active:
            #     self.scoreboard.update_score()
                
            #     self.scoreboard.update_level()
            #     self.scoreboard.update_ships()

            #     self.scoreboard.prep_ships()
            #     self.scoreboard.update_hs()
                
            #     gf.check_high_score(stats=self.stats, sb=self.scoreboard)
            #     self.scoreboard.prep_high_score()   
            # else: 
            #     self.screen.blit(self.settings.bg, (0,70))
            #     self.play_button.update()
            #     self.scoreboard.reset()

            #     gf.check_high_score(stats=self.stats, sb=self.scoreboard)
            #     self.scoreboard.update_hs()

            #     self.scoreboard.prep_score()
            #     # self.scoreboard.prep_ships()
            #     self.scoreboard.prep_level()
            #     self.scoreboard.prep_pt_table()
            #     self.scoreboard.update_pt_table()
            #     self.stats.reset_stats()
                

            # pg.display.flip()
def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()