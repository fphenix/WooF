# V1.1 : added countdown
# V1.2 : added repeat
# V1.3 : added autostart

# =======================================================================================
# util module imported into fPhenix 2025 : Wheel Of Fortune
# Timer Class
# =======================================================================================

import pygame

# =======================================================================================
class Timer:
    def __init__(self, duration, function = None, repeat = False, autostart = False):
        self.duration = duration    #milliseconds
        self.func = function
        self.start_time = 0
        self.countdown = 0
        self.active = False
        self.repeat = repeat
        if autostart:
            self.activate()

    # -----------------------------------------------------------------------------------
    def isRunning(self):
        return self.active

    # -----------------------------------------------------------------------------------
    def set_duration(self, duration):
        self.duration = duration
        
    # -----------------------------------------------------------------------------------
    def activate(self):
        self.active = True
        self.countdown = self.duration
        self.start_time = pygame.time.get_ticks()

    # -----------------------------------------------------------------------------------
    def deactivate(self):
        self.active = False
        self.start_time = 0
        self.countdown = 0
        if self.repeat:
            self.activate()

    # -----------------------------------------------------------------------------------
    def update(self):
        if self.active:
            curr_time = pygame.time.get_ticks()
            spent = curr_time - self.start_time
            self.countdown = self.duration - spent
            if self.countdown <= 0:
                #if a function exists and Timer activated, then run the function
                if self.func and self.start_time != 0:
                    self.func()
                self.deactivate()
