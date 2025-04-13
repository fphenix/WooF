# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Player Class
# =======================================================================================

import pygame
from setup.settings import *

from gameobj.boxtext import BoxText

class Player:
    def __init__(self, id, name, avatar, fonts, avatars_db):
        self.id = id
        self.window = pygame.display.get_surface()
        self.name = name
        self.avatar = avatar
        self.curr_money = 0
        self.tot_money = 0
        self.fonts = fonts
        self.avatars_db = avatars_db
        self.main_color = PLAYERS_COLORS[id]
        self.key = PLAYERS_TOSSUP_KEYS[id]

        self.freeplay = False

        self.wedge_int = None # int

        self.banned = False #♦indicates if player can Play Toss up or can no-longer play it (already given an wrong answer)

    # -----------------------------------------------------------------------------------
    def bankrupt(self):
        self.curr_money = 0

    # -----------------------------------------------------------------------------------
    # When a player wins a puzzle, need to store its curr money into its tot money
    def bank(self):
        self.add_to_total(self.curr_money)
        self.bankrupt()

    # -----------------------------------------------------------------------------------
    def ban(self):
        self.banned = True

    # -----------------------------------------------------------------------------------
    def unban(self):
        self.banned = False

    # -----------------------------------------------------------------------------------
    def add_to_curr(self, amount):
        self.curr_money += amount
    
    # -----------------------------------------------------------------------------------
    def add_to_total(self, amount):
        self.tot_money += amount
    
    # -----------------------------------------------------------------------------------
    def Player_Etiquette_Small(self, x, y, selected= False, shaded= False, tossup= False):
        fg_color = 'black'
        bg_color = PLAYERS_COLORS[self.id]
        #name
        ltr_txt = ' : \'' + self.key + '\'' if tossup else ""
        name_label = BoxText(
            x= x + 100, y= y,
            w= 200, h= 50,
            text= self.name + ltr_txt,
            font= self.fonts['player'],
            fgcolor= fg_color, bgcolor= bg_color,
            infl= False
        )
        name_label.draw()
        #avatar 
        self.window.blit(pygame.transform.smoothscale(self.avatars_db[self.avatar], (100, 100)) , (x + 50, y + 30))
        #player total money
        money_label = BoxText(
            x= x + 100, y= y + 160,
            w= 200, h= 50,
            text= "Tot:" + str(self.tot_money) + "€",
            font= self.fonts['small'],
            fgcolor= fg_color, bgcolor= bg_color,
            infl= False
        )
        money_label.draw()
        #if tossup is False (normal puzzle) then also show surrent money amount
        #else if True (TossUp) only show total momeny amoun
        if not tossup:
            #player current game money
            curr_money_label = BoxText(
                x= x + 100, y= y + 215,
                w= 200, h= 50,
                text= str(self.curr_money) + "€",
                font= self.fonts['small'],
                fgcolor= fg_color, bgcolor= bg_color,
                infl= False
            )
            curr_money_label.draw()
        #
        sel_shade_rect = pygame.Rect(x-10, y-35, 220, 285) 
        sel_shade_box = pygame.Surface(sel_shade_rect.size, pygame.SRCALPHA)
        #Add a shaded box over the etiquette
        if shaded:
            sel_shade_box.set_alpha(128) 
            pygame.draw.rect(sel_shade_box, 'grey', sel_shade_box.get_rect())
            self.window.blit(sel_shade_box, sel_shade_rect)
        #Draw a frame around the player if "selected"
        if selected:
            pygame.draw.rect(sel_shade_box, bg_color, sel_shade_box.get_rect(), 5)
            self.window.blit(sel_shade_box, sel_shade_rect)
            
    # -----------------------------------------------------------------------------------
    def Player_Etiquette_Big(self, x, y):
        #name
        name_label = BoxText(
            x= x + 200, y= y,
            w= 400, h= 50,
            text= self.name,
            font= self.fonts['player'],
            fgcolor= 'black', bgcolor= self.main_color,
            infl= False
        )
        name_label.draw()
        #avatar 
        self.window.blit(pygame.transform.smoothscale(self.avatars_db[self.avatar], (200, 200)) , (x + 100, y + 30))
