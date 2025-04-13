# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Button Class & Visual Keyboard
# =======================================================================================

import pygame
from setup.settings import *

# -----------------------------------------------------------------------------------
class Button():
    def __init__(self, x, y, width, height, text, font, border= 0, enabled= True):
        self.window = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        self.text = text
        self.font = font
        self.collision_rect = None

        self.enabled = enabled
        self.selected = False
        self.border = border

    # -----------------------------------------------------------------------------------
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    # -----------------------------------------------------------------------------------
    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    # -----------------------------------------------------------------------------------
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    # -----------------------------------------------------------------------------------
    def resize(self, w, h):
        self.w = w
        self.h = h
        
    # -----------------------------------------------------------------------------------
    def check_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[MB_LEFT]
        if self.collision_rect == None:
            return False
        return self.enabled and left_click and self.collision_rect.collidepoint(mouse_pos)
    
    # -----------------------------------------------------------------------------------
    def get_value(self):
        return self.text

    # -----------------------------------------------------------------------------------
    def toggle_state(self):
        self.enabled = not(self.enabled)

    # -----------------------------------------------------------------------------------
    def isEnabled(self):
        return self.enabled

    # -----------------------------------------------------------------------------------
    def draw(self):
        if not self.enabled:
            bgcolor = BTN_BG_COLOR_SHADED
            fgcolor = BTN_FG_COLOR_SHADED
        else:
            bgcolor = BTN_BG_COLOR_ACTIVE if self.selected else BTN_BG_COLOR
            fgcolor = BTN_FG_COLOR_ACTIVE if self.selected else BTN_FG_COLOR

        text_surf = self.font.render(self.text, antialias= True, color=fgcolor, bgcolor=bgcolor)
        box_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32).convert_alpha()
        box_rect = box_surf.get_rect(center= (self.x, self.y))
        center_within = box_surf.get_rect().center
        box_surf.fill(bgcolor)
        box_surf.blit(text_surf, text_surf.get_rect(center= center_within))
        
        self.window.blit(box_surf, box_rect)
        if self.border > 0:
            pygame.draw.rect(self.window, fgcolor, box_rect, self.border)

        self.collision_rect = box_rect
        #pygame.draw.rect(self.window, 'red', self.collision_rect, self.border) #debug : to see collision boxes for buttons
