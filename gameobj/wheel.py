# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Wheel Class
# =======================================================================================

import pygame
import math
from random import random

from setup.settings import *

from setup.utils import keepbetween, isColorLight

# -----------------------------------------------------------------------------------
class Wheel:
    def __init__(self, centerx, centery, radius, start_angle, logo, fonts, hole_radius= 100):
        self.window = pygame.display.get_surface()

        self.radius = radius
        self.start_angle = start_angle
        self.rot_angle = 0
        self.angle = start_angle
        self.angle_force = 0
        self.hole_radius = hole_radius
        self.fonts = fonts

        self.force_angle = ONE_REVOLUTION * 0.5
        
        self.wedge_values_list = list()

        self.logo_img = logo

        self.logo = pygame.transform.scale(self.logo_img.convert_alpha(), (2 * hole_radius, 2 * hole_radius))

        self.txt_pos = (self.radius // 2) + (self.hole_radius // 2)
        self.center = (centerx, centery)
        
        self.rect = pygame.Rect((centerx - radius, centery - radius), (2 * self.radius, 2 * self.radius))
        self.pie_width = int(360/WHEEL_NB_WEDGES) #degrees
        self.pointer_coords = [
            [centerx, centery - radius - WHEEL_POINTER_OFFSET, ( 0,  1)],
            [centerx + radius + WHEEL_POINTER_OFFSET, centery, (-1,  0)],
            [centerx, centery + radius + WHEEL_POINTER_OFFSET, ( 0, -1)],
            [centerx - radius - WHEEL_POINTER_OFFSET, centery, ( 1,  0)]
        ]

        self.locked = False
        self.spinning = False

    # -----------------------------------------------------------------------------------
    def choose_wheel(self, n):
        self.wedge_values_list = list()
        for wedge in range(WHEEL_NB_WEDGES):
            if isinstance(WHEELS[n][wedge], int):
                txt = str(WHEELS[n][wedge]) + " €"
            else:
                txt = WHEELS[n][wedge]
            self.wedge_values_list.append(txt)

    # -----------------------------------------------------------------------------------
    # wedge number the player's pointer is on
    def get_wedge_nb_from_angle(self, player_offset):
        return int(player_offset + self.angle // (360 / WHEEL_NB_WEDGES)) % WHEEL_NB_WEDGES

    # -----------------------------------------------------------------------------------
    # wedge content the player's pointer is on
    def get_wedge_content(self, player_offset):
        pointed_wedge = self.get_wedge_nb_from_angle(player_offset)
        return self.wedge_values_list[pointed_wedge]

    # -----------------------------------------------------------------------------------
    def launch(self):
        if not self.locked:
            self.angle_force = (random() * WHEEL_FORCE) + WHEEL_FORCE_SPAN
            self.locked = True
            self.spinning = True

    # -----------------------------------------------------------------------------------
    def unlock(self):
        self.locked = False

	# -----------------------------------------------------------------------------------
    def draw_force_select(self, x, y):
        pygame.draw.rect(
            surface= self.window,
            color= 'red',
            rect= (x, y, 100, 100),      # x y w h
            width= 5,
            border_bottom_right_radius= 30,
            border_top_left_radius= 30
        )

        pygame.draw.arc(
            surface= self.window,
            color= 'blue',
            rect= (x+5, y+5, 90, 90),  	    # x y w h
            start_angle= FORCE_ANGLE_MIN, 	# radians	
            stop_angle= self.force_angle,	# radians
            width= 30						# here radius is 90/2=45, 30 doesn't fill it completely to get desired result
        )

    # -----------------------------------------------------------------------------------
    def draw_wire(self, n):
        startx, starty, _ = self.pointer_coords[n]
        endx, endy = 1100, 70
        self.wire_points = [
            [(endx, starty), (endx, endy)],
            [(startx, 20), (endx, 20), (endx, endy)],
            [(900, starty), (900, 20), (endx, 20), (endx, endy)],
            [(startx, 20), (endx, 20), (endx, endy)]
        ]
        
        for point in self.wire_points[n]:
            nextx, nexty = point
            pygame.draw.line(self.window, PLAYERS_COLORS[n], (startx, starty), (nextx, nexty), 15)
            startx, starty = point
        
    # -----------------------------------------------------------------------------------
    def draw_pointer(self, n):
        x, y, dir = self.pointer_coords[n]
        dirx, diry = dir
        l, l2, l3, l4 = WHEEL_POINTER_OFFSET, 4, 7, 10
        xe, ye = x  + (dirx * l),   y + (diry * l)
        x2, y2 = xe + (dirx * l2), ye + (diry * l2)
        x3, y3 = x2 + (dirx * l3), y2 + (diry * l3)
        x4, y4 = x2 + (dirx * l4), y2 + (diry * l4)
        pygame.draw.line(self.window, PLAYERS_COLORS[n], (x, y), (xe, ye), 15)
        pygame.draw.line(self.window, PLAYERS_COLORS[n], (x, y), (x2, y2), 5)
        pygame.draw.line(self.window, PLAYERS_COLORS[n], (x, y), (x3, y3), 3)
        pygame.draw.line(self.window, PLAYERS_COLORS[n], (x, y), (x4, y4), 1)
    
    # -----------------------------------------------------------------------------------
    def draw(self): #degrees
        idx = 0
        for drawangle in range(0, 360, self.pie_width): #degrees
            wedge_color = pygame.Color(WEDGE_COLORS[self.wedge_values_list[idx]])
            fgcolor = 'black' if isColorLight(wedge_color.r, wedge_color.g, wedge_color.b) else 'white'
            text_surf = self.fonts['wheel'].render(self.wedge_values_list[idx], True, fgcolor)
            text_rect = text_surf.get_rect(midleft= self.rect.center)

            pie_start_angle = math.radians(drawangle - (self.angle + self.pie_width)) #radians
            hangle = math.radians(drawangle - (self.angle + (self.pie_width // 2)))
            pie_stop_angle  = math.radians(drawangle - self.angle) #radians
           
            pygame.draw.arc(
                surface= self.window,
                color= wedge_color, 
                rect= self.rect, 
                start_angle= pie_start_angle, 
                stop_angle= pie_stop_angle,
                width= self.radius - self.hole_radius
            )
            
            r_text = pygame.transform.rotate(text_surf, math.degrees(hangle))
            x = self.rect.centerx + (self.txt_pos * math.cos(hangle))
            y = self.rect.centery - (self.txt_pos * math.sin(hangle))
            text_rect = r_text.get_rect(center= (x, y))
            
            self.window.blit(r_text, text_rect)
            idx += 1

        rot_logo = pygame.transform.rotate(self.logo, -self.angle)
        logo_rect = rot_logo.get_rect(center= self.center)
        self.window.blit(rot_logo, logo_rect)

        for n in range(4):
            #draw pointers
            self.draw_pointer(n)

    # -----------------------------------------------------------------------------------
    def update(self):
        if self.angle_force > 0:
            self.angle = keepbetween(self.angle + self.angle_force, 0, 360)
            self.angle_force *= WHEEL_DAMPENER
            if self.angle_force < WHEEL_STOP:
                self.angle_force = 0
                self.spinning = False
