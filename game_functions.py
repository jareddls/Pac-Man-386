import pygame as pg
import sys
import pickle
# from pacman import Pacman

from vector import Vector

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


movement = {pg.K_LEFT: Vector(-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_RIGHT: Vector(1, 0),
            pg.K_UP: Vector(0, -1),
            pg.K_DOWN: Vector(0, 1)
            }

  
def check_keydown_events(event, settings, pacman):
    key = event.key
    # if key == pg.K_SPACE: 
    #     pacman.shooting = True
    if key in movement.keys():
        pacman.vel += settings.pacman_speed_factor * movement[key]

def check_keyup_events(event, settings, pacman):
    key = event.key
    if key == pg.K_ESCAPE:
        pacman.vel = Vector()
    elif key in movement.keys(): 
        pacman.vel -= settings.pacman_speed_factor * movement[key]

def check_events(settings, sound, screen, stats, sb, play_button, pacman):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN: 
            check_keydown_events(event=event, settings=settings, pacman=pacman)
        elif event.type == pg.KEYUP: 
            check_keyup_events(event=event, settings = settings, pacman=pacman)
        elif event.type == pg.MOUSEBUTTONUP:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(settings, sound, screen, stats, sb, play_button, mouse_x, mouse_y)

def check_play_button(settings, sound, screen, stats, sb, play_button, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pg.mouse.set_visible(False)

        stats.game_active = True

        # aliens.reset()
        # ship_lasers.reset()
        # alien_lasers.reset()
        
        sb.prep_score()
        sb.reset()

        pg.mixer.music.load('sounds/pacman_beginning.wav')
        sound.play_bg()
        

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if sb.score > stats.high_score:
        stats.high_score = sb.score
        with open('scores/high_scores.dat', 'wb') as file:
            pickle.dump(stats.high_score, file)
        sb.prep_high_score()
        

def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = 700
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)
