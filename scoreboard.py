import pygame as pg 
from pygame.sprite import Group
import game_functions as gf

class Scoreboard:
    def __init__(self, game, stats, sound): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = stats
        self.sound = sound

        self.text_color = (255, 255, 255)
        self.font = pg.font.Font('fonts/pixel.ttf', 24)
        self.score_image = None 
        self.score_rect = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def increment_score(self, type): 
        self.score += type
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 50

        self.score_title = self.font.render('SCORE', True, self.text_color, self.settings.bg_color)
        self.score_title_rect = self.score_title.get_rect()
        self.score_title_rect.right = self.screen_rect.right - 20
        self.score_title_rect.top = 15
        

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = 50

        self.hs_title = self.font.render('HIGHSCORE', True, self.text_color, self.settings.bg_color)
        self.hs_title_rect = self.hs_title.get_rect()
        self.hs_title_rect.left = self.screen_rect.left + 20
        self.hs_title_rect.top = 15

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(f'Level: {self.stats.level}'), True,
            self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.bottom = self.score_rect.bottom + 710

    def prep_pt_table(self):
        """Show the table"""
        self.first_inkey_pts_text = self.font.render('INKEY', True, (255,255,255), (0,0,0))
        self.first_inkey_pts_text_rect = self.first_inkey_pts_text.get_rect()
        self.first_inkey_pts_text_rect =  (200, 350)

        self.second_pinky_pts_text = self.font.render('PINKY', True, (255,255,255), (0,0,0))
        self.second_pinky_pts_text_rect = self.second_pinky_pts_text.get_rect()
        self.second_pinky_pts_text_rect = (200, 400)

        self.third_blinky_pts_text = self.font.render('BLINKY', True, (255,255,255), (0,0,0))
        self.third_blinky_pts_text_rect = self.third_blinky_pts_text.get_rect()
        self.third_blinky_pts_text_rect = (500, 350)

        self.fourth_clyde_pts_text = self.font.render('CLYDE', True, (255,255,255), (0,0,0))
        self.fourth_clyde_pts_text_rect = self.fourth_clyde_pts_text.get_rect()
        self.fourth_clyde_pts_text_rect = (500, 400)

    def reset(self): 
        self.score = 0
        self.level = 1
        self.update_score()

    def update_score(self): 
        self.draw_score()

    def update_hs(self): 
        self.draw_hs()

    def update_level(self): 
        self.draw_level()

    def update_pt_table(self):
        self.draw_pt_table()

    def draw_score(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_title, self.score_title_rect)
    
    def draw_hs(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.hs_title, self.hs_title_rect)
    
    def draw_level(self):
        self.screen.blit(self.level_image, self.level_rect)

    def draw_pt_table(self):
        self.screen.blit(pg.image.load('images/blue_ghost_left0.png'), (325, 350))
        self.screen.blit(pg.image.load('images/pink_ghost_left0.png'), (325, 400))
        self.screen.blit(pg.image.load('images/red_ghost_right0.png'), (450, 350))
        self.screen.blit(pg.image.load('images/yellow_ghost_right0.png'), (450, 400))

        self.screen.blit(self.first_inkey_pts_text, self.first_inkey_pts_text_rect)
        self.screen.blit(self.second_pinky_pts_text, self.second_pinky_pts_text_rect)
        self.screen.blit(self.third_blinky_pts_text, self.third_blinky_pts_text_rect)
        self.screen.blit(self.fourth_clyde_pts_text, self.fourth_clyde_pts_text_rect)