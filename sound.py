import pygame as pg

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.2)

        pacman_beginning_sound = pg.mixer.Sound('sounds/pacman_beginning.wav')
        pacman_death_sound = pg.mixer.Sound('sounds/pacman_death.wav')
        pacman_pellet_sound = pg.mixer.Sound('sounds/pacman-pellet-eat.wav')

        self.sounds = {'start': pacman_beginning_sound, 'death': pacman_death_sound, 'pellet': pacman_pellet_sound}

    def play_beginning(self, loop=0, start=0, fade_ms=3000):
        pg.mixer.music.play(loop, start, fade_ms)

    def pacman_death(self):
        pg.mixer.Sound.play(self.sounds['death'])
        pg.mixer.Sound.set_volume(self.sounds['death'], 0.1)

    def pacman_pellet(self):
        pg.mixer.Sound.play(self.sounds['pellet'])
        pg.mixer.Sound.set_volume(self.sounds['pellet'], 0.1)
