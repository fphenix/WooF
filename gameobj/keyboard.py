# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Visual Keyboard Class
# =======================================================================================

from setup.settings import *
from gameobj.button import Button

class Keyboard:
    def __init__(self, fonts):
        self.fonts = fonts
        self.keys = {}
        
        self.init()

    def init(self):
       #Keyboard
        for letter in ALPHA:
            self.keys[letter] = Button(
                x= 0, y= 0,
                width=50, height=60,
                text= letter,
                font= self.fonts['large'],
            )

        #delete button
        self.delete_button = Button(
            x= 0, y= 0,
            width= 120, height= 60,
            text= "<DEL",
            font= self.fonts['normal']
        )
        self.delete_button.disable()

        #validate answer button
        self.validate_button = Button(
            x= 0, y= 0,
            width= 120, height= 60,
            text= "Ok!",
            font= self.fonts['normal']
        )
        self.validate_button.disable()

    # -----------------------------------------------------------------------------------
    # Can display 'Full' for the Full alphabet
    #          Or 'Conso' for Consonants (and 'Y')
    #          Or 'Voyel' for A, E, I, O and U
    def Display(self, mode= 'Full', exclude= list(), del_en= False, solve_en= False):
        split_at = len(ALPHA) // 2
        for idx, letter in enumerate(ALPHA):
            row = 0 if idx < split_at else 1
            self.keys[letter].set_pos(x= 300 + (idx % split_at) * 60, y= 610 + 70 * row)
            if (mode == 'Full' and (letter in exclude)) \
                    or (mode == 'Conso' and (letter not in CONSON or letter in exclude)) \
                    or (mode == 'Voyel' and (letter not in VOYELS or letter in exclude)):
                self.keys[letter].disable()
            else:
                self.keys[letter].enable()
            
            self.keys[letter].draw()

        # Only display the Del and Solve buttons in Full mode, else bail out
        if not mode == 'Full':
            return
        
        #Display the Del button (shaded if nothing to undo)
        self.delete_button.set_pos(1130, 610)
        if del_en:
            self.delete_button.enable()
        else:
            self.delete_button.disable()
        self.delete_button.draw()

        #Display the Solve button (shaded if puzzle not completed with an answer)
        if solve_en:
            self.validate_button.enable()
        else:
            self.validate_button.disable()
        self.validate_button.set_pos(1130, 680)
        self.validate_button.draw()
