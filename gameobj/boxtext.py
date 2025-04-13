# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Box Text/Labels Class
# =======================================================================================

import pygame

class BoxText:
    def __init__(self, x, y, w, h, text, font, fgcolor, bgcolor, sel_bgcolor= None, infl= False, border= 0):
        self.window = pygame.display.get_surface()
        self.text = text
        self.font = font
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.sel_bgcolor = sel_bgcolor
        self.selected = False
        self.x = x # x pos
        self.y = y # y pos
        self.w = w # width or inflate-x size ; if None get size from rendered text surface
        self.h = h # height or inflate-y size
        self.infl = infl # w,h size (False) or inflate-by w,h (True)
        self.border = border

        self.Init()

    def select(self):
        self.selected = True
        self.Init()

    def unselect(self):
        self.selected = False
        self.Init()

    def Init(self):
        bgcolor = self.bgcolor if not self.selected else self.sel_bgcolor
        text_surf = self.font.render(self.text, True, self.fgcolor, bgcolor)
        if self.infl:
            self.box_surf = pygame.Surface(text_surf.get_rect().inflate(self.w, self.h).size)
        else:
            if self.w == None:
                self.w, self.h = text_surf.get_width(), text_surf.get_height()   
            self.box_surf = pygame.Surface((self.w, self.h))
        box_rect = text_surf.get_rect(center = self.box_surf.get_rect().center)
        self.box_surf.fill(bgcolor)
        self.box_surf.blit(text_surf, box_rect)
        if self.border > 0:
            pygame.draw.rect(self.box_surf, self.fgcolor, box_rect, self.border)
        self.text_rect = self.box_surf.get_rect(center= (self.x, self.y))

    def draw(self):
        self.window.blit(self.box_surf, self.text_rect)

# =================================================================================================
class SimpleBoxText(BoxText):
    def __init__(self, x, y, text, font, fgcolor, bgcolor):
        super().__init__(x, y, None, None, text, font, fgcolor, bgcolor, infl= False, border= 0)
