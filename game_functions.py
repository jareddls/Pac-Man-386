import pygame as pg
import sys

#sm stands for start menu
def sm_events(self):
    for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = 'playing'

def sm_update(self):
    pass

def sm_draw(self):
    pass

#wp stands for while playing
def wp_events(self):
    pass

def wp_update(self):
    pass

def wp_draw(self):
    pass

def player_die(self):
    pass

def draw_coins(self):
    pass

#go stands for game over
def go_events(self):
    pass

def go_update(self):
    pass

def go_draw(self):
    pass