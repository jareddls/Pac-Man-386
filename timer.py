from constants import *

class Timer(object):
    def __init__(self, frames=[], speed=20, loop=True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    def reset(self):
        self.current_frame = 0
        self.finished = False

    def update(self, dt):
        if not self.finished:
            self.next_frame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame -= 1
   
        return self.frames[self.current_frame]

    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0