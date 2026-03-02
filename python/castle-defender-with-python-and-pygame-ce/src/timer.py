from settings import pygame


class Timer:
    def __init__(self, duration, repeat=False, autostart=False, function=None):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.function = function

        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()

            if current_time - self.start_time >= self.duration:
                if self.function and self.start_time != 0:
                    self.function()

                self.deactivate()
