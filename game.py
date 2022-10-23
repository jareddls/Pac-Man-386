import pygame as pg
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pause import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from maze_data import MazeData
from button import Button

main_menu_flag = True

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, 0, 32)
        self.bg = None
        self.bg_normal = None
        self.bg_flash = None

        self.clock = pg.time.Clock()
        self.fruit = None
        self.level = 0

        self.pause = Pause(True)

        self.lives = 3

        self.score = 0
        self.text_group = TextGroup()

        self.life_sprites = LifeSprites(self.lives)

        self.flash_bg = False
        self.flash_time = 0.2
        self.flash_timer = 0

        self.fruit_capt = []

        self.maze_data = MazeData()

        self.play_button = Button(self.screen, "PLAY", 224, 500, 24)


    def restart_game(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.start_game()

        self.score = 0
        self.text_group.update_score(self.score)
        self.text_group.update_level(self.level)
        self.text_group.show_text(READYTXT)

        self.life_sprites.reset_lives(self.lives)

        self.fruit_capt = []

    def reset_level(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None

        self.text_group.show_text(READYTXT)
    

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()

        self.text_group.update_level(self.level)

    def set_bg(self):
        self.bg_normal = pg.surface.Surface(SCREEN_SIZE).convert()
        self.bg_normal.fill(BLACK)
        self.bg_flash = pg.surface.Surface(SCREEN_SIZE).convert()
        self.bg_flash.fill(BLACK)
        self.bg_normal = self.maze_sprites.construct_background(self.bg_normal, self.level % 5)
        self.bg_flash = self.maze_sprites.construct_background(self.bg_normal, 5)
        self.flash_bg = False
        self.bg = self.bg_normal

    def start_game(self):
        self.maze_data.load_maze(self.level)
        self.maze_sprites = MazeSprites(self.maze_data.obj.name + ".txt", self.maze_data.obj.name + "_rotation.txt")
        self.set_bg()
        pg.display.set_caption('PAC-MAN')
        pg.display.set_icon(pg.image.load('images/pacman_left0.png'))

        self.nodes = NodeGroup(self.maze_data.obj.name + ".txt")

        self.maze_data.obj.set_portal_pairs(self.nodes)
        self.maze_data.obj.connect_home_nodes(self.nodes)

        self.pacman = Pacman(self.nodes.get_node_from_tiles(*self.maze_data.obj.pacman_start))

        self.pellets = PelletGroup(self.maze_data.obj.name + ".txt")

        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)

        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(*self.maze_data.obj.add_offset(2, 0)))
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(*self.maze_data.obj.add_offset(2, 3)))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(*self.maze_data.obj.add_offset(0, 3)))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(*self.maze_data.obj.add_offset(4, 3)))

        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(*self.maze_data.obj.add_offset(2, 3)))

        self.nodes.deny_home_acc(self.pacman)
        self.nodes.deny_home_acc_list(self.ghosts)
        
        self.ghosts.inky.start_node.deny_acc(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.start_node.deny_acc(LEFT, self.ghosts.clyde)

        self.maze_data.obj.deny_ghosts_access(self.ghosts, self.nodes)


    def check_pb(pb, mouse_x, mouse_y):
        global main_menu_flag
        button_clicked = pb.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and main_menu_flag:
            pg.mouse.set_visible(False)
            main_menu_flag = False
            pg.mixer.Sound.play(pg.mixer.Sound('sounds/pacman_beginning.wav'))

    def check_events(self, pb=None):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.text_group.hide_text()
                            self.show_entities()
                            pg.mixer.music.load('sounds/ghost_normal.wav')
                            pg.mixer.music.play(-1)
                        else:
                            self.text_group.show_text(PAUSETXT)
                            self.hide_entities()
                            pg.mixer.music.pause()
            elif event.type == pg.MOUSEBUTTONUP:
                if main_menu_flag:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    Game.check_pb(pb, mouse_x, mouse_y)
                else:
                    pass

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.update_score(pellet.points)
            if self.pellets.num_eaten == 30:
                self.ghosts.inky.start_node.allow_acc(RIGHT, self.ghosts.inky)
            if self.pellets.num_eaten == 70:
                self.ghosts.clyde.start_node.allow_acc(LEFT, self.ghosts.clyde)
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()
            if self.pellets.is_empty():
                self.flash_bg = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)
                pg.mixer.music.stop()

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.text_group.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.update_points()
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_acc(ghost)
                    pg.mixer.Sound.play(pg.mixer.Sound('sounds/pacman_eat_ghost.wav'))
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.life_sprites.remove_image()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.text_group.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)

                
    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def check_fruit_events(self):
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.update_score(self.fruit.points)
                self.text_group.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruit_capt = False
                for fruit in self.fruit_capt:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruit_capt = True
                        break
                if not fruit_capt:
                    self.fruit_capt.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def update_score(self, points):
        self.score += points
        self.text_group.update_score(self.score)

    def draw(self):
        if main_menu_flag:
            pg.display.update()
        else:
            self.screen.blit(self.bg, (0,0))
            self.pellets.draw(self.screen)

            if self.fruit is not None:
                self.fruit.draw(self.screen)

            self.pacman.draw(self.screen)
            self.ghosts.draw(self.screen)

            self.text_group.draw(self.screen)

            for i in range(len(self.life_sprites.images)):
                x = self.life_sprites.images[i].get_width() * i
                y = SCREEN_HEIGHT - self.life_sprites.images[i].get_height()
                self.screen.blit(self.life_sprites.images[i], (x, y))

            for i in range(len(self.fruit_capt)):
                x = SCREEN_WIDTH - self.fruit_capt[i].get_width() * (i+1)
                y = SCREEN_HEIGHT - self.fruit_capt[i].get_height()
                self.screen.blit(self.fruit_capt[i], (x, y))

            pg.display.update()

    def update(self):

        if main_menu_flag:
            self.play_button.update()
            self.check_events(self.play_button)
            self.screen.blit(pg.image.load('images/pacman_ss.png'), [0, 0])
            self.draw()
        else:
            dt = self.clock.tick(30) / 1000.0
            self.text_group.update(dt)
            self.pellets.update(dt)
            
            if not self.pause.paused:
                self.ghosts.update(dt)

                if self.fruit is not None:
                    self.fruit.update(dt)

                self.check_pellet_events()
                self.check_ghost_events()
                self.check_fruit_events()

            if self.pacman.alive:
                if not self.pause.paused:
                    self.pacman.update(dt)
            else:
                self.pacman.update(dt)

            if self.flash_bg:
                self.flash_timer += dt
                if self.flash_timer >= self.flash_time:
                    self.flash_timer = 0
                    if self.bg == self.bg_normal:
                        self.bg = self.bg_flash
                    else:
                        self.bg = self.bg_normal

            after_pause_meth = self.pause.update(dt)
            if after_pause_meth is not None:
                after_pause_meth()

            self.check_events()
            self.draw()

    
if __name__ == "__main__":
    game = Game()
    game.start_game()
    while True:
        game.update()