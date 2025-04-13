# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Game Display
# =======================================================================================

import pygame
from setup.settings import *

from gameobj.button import Button
from gameobj.boxtext import BoxText, SimpleBoxText

# =======================================================================================
class Screens:
    def __init__(self, manager):
        self.manager_ref = manager
        self.puzzle = manager.puzzle
        self.timers = manager.timers
        self.players = manager.players
        self.wheel = manager.wheel
        self.keyboard = manager.keyboard

        self.window = pygame.display.get_surface()
        self.fonts = manager.fonts

        self.setup_buttons = list()
        self.avatar_sel_buttons = {}

        self.Init_Buttons()
        self.Init_Labels()

    # -----------------------------------------------------------------------------------
    def Init_Buttons(self):
        #Let's play button
        self.play_button = Button(
            x= 1000, y= 40,
            width= 400, height= 50,
            text= " Let's Go ! ",
            font= self.fonts['large'],
            border= 5
        )

        #Solve button (try to fill in the blanks to win the puzzle)
        self.solve_button = Button(
            x= 1040, y= 640,
            width= 350, height= 60,
            text= "Solve",
            font= self.fonts['normal']
        )

        #buy button
        self.buy_button = Button(
            x= 240, y= 640,
            width= 350, height= 60,
            text= "Buy Voyel (- " + str(self.manager_ref.voyel_cost) + "€)",
            font= self.fonts['normal']
        )
        self.buy_button.disable()

        #spin button
        self.spin_button = Button(
            x= 640, y= 640,
            width= 350, height= 60,
            text= "Spin",
            font= self.fonts['normal']
        )

        #wheel spin button
        self.wheelspin_button = Button(
            x= 1100, y= 500,
            width= 250, height= 80,
            text= "Spin!",
            font= self.fonts['normal']
        )

        #wheel Ok button
        self.wheelok_button = Button(
            x= 1100, y= 600,
            width= 250, height= 80,
            text= "Ok!",
            font= self.fonts['normal']
        )

        #nb players 1 2 3 4 buttons
        for n in range(MAX_PLAYERS):
            self.setup_buttons.append(
                Button(
                    x= 350 + n * 60, y= 60,
                    width= 40, height= 60,
                    text= str(n + 1),
                    font= self.fonts['large']
                )
            )
            if n == (self.manager_ref.nb_players - 1):
                self.setup_buttons[n].select()
            else:
                self.setup_buttons[n].unselect()

            #avatar selection left/right button for all players
            for side in ["left", "right"]:
                self.avatar_sel_buttons[str(n) + '_' + side] = Button(
                    x= 0, y= 0,
                    width= 40, height= 180,
                    text= "<" if side == "left" else ">",
                    font= self.fonts['large']
                )


    # -----------------------------------------------------------------------------------
    def Init_Labels(self):
        self.category_label = None
        fg_color = 'black'
        bg_color = (255, 255, 192)

        #Intro screen label
        margin_horiz, margin_vertic = 40, 50
        offset_h, offset_v = 0, 70
        self.intro_label = BoxText(
            x= offset_h + WINDOW_WIDTH // 2,
            y= offset_v + WINDOW_HEIGHT // 2,
            w= margin_horiz, h= margin_vertic,
            text= 'Un jeu par fPhénix ; 2025',
            font= self.fonts['intro'],
            fgcolor= fg_color, bgcolor= bg_color,
            infl= True
        )

        #label "Nb Players"
        margin_horiz, margin_vertic = 40, 20
        self.nbplayers_label = BoxText(
            x= 180, y= 60,
            w= margin_horiz, h= margin_vertic,
            text= 'Nb Player(s) :',
            font= self.fonts['intro'],
            fgcolor= fg_color, bgcolor= bg_color,
            infl= True
        )

        #label "Space to Start"
        self.spc_start_label = SimpleBoxText(
            x= WINDOW_WIDTH // 2, y= 50,
            text= ' <SPACE> to Start ',
            font= self.fonts['large'],
            fgcolor= 'black', bgcolor= "white"
        )

        #label "Space to Start"
        self.next_label = SimpleBoxText(
            x= WINDOW_WIDTH // 2, y= 50,
            text= ' <ENTER> to continue ',
            font= self.fonts['large'],
            fgcolor= 'black', bgcolor= "white"
        )

        self.correct_label = SimpleBoxText(
            x= WINDOW_WIDTH // 2, y= WINDOW_HEIGHT - 60,
            text= ' That is CORRECT! ',
            font= self.fonts['large'],
            fgcolor= 'black', bgcolor= "green"
        )

        self.nop_label = SimpleBoxText(
            x= WINDOW_WIDTH // 2, y= WINDOW_HEIGHT - 60,
            text= ' No, That\'s not it! ',
            font= self.fonts['large'],
            fgcolor= 'black', bgcolor= "red"
        )

    # -----------------------------------------------------------------------------------
    def Prepa_Rules(self):
        #text rules
        rules = "Commençons par des parties \"Flash\":" + (TXT_RETLN * 2)
        rules += "Chaque second une lettre du puzzle s'affiche." + TXT_RETLN
        rules += "Dès que vous pensez l'avoir résolu appuyez sur votre" + TXT_RETLN
        rules += "touche afin de compléter le puzzle." + TXT_RETLN
        rules += "Attention! : si ce n'est pas correct, vous ne pourrez" + TXT_RETLN
        rules += "plus participer à ce puzzle!" + TXT_RETLN
        rules += "Mais plus vous résolvez le puzzle rapidement, plus" + TXT_RETLN
        rules += "vous gagnez d'argent." + (TXT_RETLN * 2)
        #rules += "Vos touches:" + TXT_RETLN
        for n, player in enumerate(self.players):
            name = player.name
            rules += (TXT_SPACE * 5) + " * " + name
            rules += " :  Touche '" + self.players[n].key + "'" + TXT_RETLN
            if n >= self.manager_ref.nb_players - 1:
                break
        
        self.rules_label = BoxText(
            x= WINDOW_WIDTH // 2,
            y= WINDOW_HEIGHT // 2,
            w= WINDOW_WIDTH * 0.75,
            h= WINDOW_HEIGHT * 0.90,
            text= rules,
            font= self.manager_ref.fonts['intro'],
            fgcolor= 'black', bgcolor= 'white'
        )

    # -----------------------------------------------------------------------------------
    def display_bg(self, bg):
        self.window.blit(self.manager_ref.images[bg], (0, 0))

    # -----------------------------------------------------------------------------------
    def Intro(self):
        #bg image
        self.display_bg('intro_bg')
        #label "a game by fphenix"
        self.intro_label.draw()

    # -----------------------------------------------------------------------------------
    def AdBreak(self):
        self.Intro()

    # -----------------------------------------------------------------------------------
    def Setup(self):
        #bg image
        self.display_bg('bg')
        #label nb players:
        self.nbplayers_label.draw()
        #Play button
        self.play_button.draw()
        #FR/EN dB
        # TODO
        #buttons 1 to 4 and avatar boxes
        for n in range(MAX_PLAYERS):
            self.setup_buttons[n].draw()
            if n < self.manager_ref.nb_players:
                x, y = 120 + (WINDOW_WIDTH // 2) * (n % 2), 140 + 300 * (n // 2)
                self.players[n].Player_Etiquette_Big(x, y)
                #avatar slectors buttons
                self.avatar_sel_buttons[str(n) + '_' +  'left'].set_pos(x + 70, y + 130)
                self.avatar_sel_buttons[str(n) + '_' + 'right'].set_pos(x + 330, y + 130)
                self.avatar_sel_buttons[str(n) + '_' +  'left'].draw()
                self.avatar_sel_buttons[str(n) + '_' + 'right'].draw()
        self.Prepa_Rules()

    # -----------------------------------------------------------------------------------
    def Toss_up_Rules(self):
        #rules
        self.rules_label.draw()
        #Play button
        self.play_button.set_pos(910, 660)
        self.play_button.draw()

    # -----------------------------------------------------------------------------------
    def Toss_up(self):
        self.rules_label = None
        self.window.blit(pygame.transform.smoothscale(self.manager_ref.images['puzzle'], (900, 600)), ((WINDOW_WIDTH - 900) // 2, 0))
        
        # To avoid a glitch when switching to a new puzzle, we ship the displaying
        # of the puzzle if none has been picked yet
        if not self.puzzle.picked_puzzle:
            return
        
        #players small avatar boxes
        for n in range(self.manager_ref.nb_players):
            #if a player has paused the game, show only his, skip other's etiquettes
            if self.manager_ref.playing != None:
                if self.manager_ref.playing != n:
                    continue
            #else don't show banned players
            elif self.players[n].banned:
                continue
            #else show etiquette
            self.players[n].Player_Etiquette_Small(10 + 1050 * (n % 2), 40 + 290 * (n // 2), tossup= True)
        
        # Display puzzle
        self.puzzle.Display_Puzzle(solving= True)

        #if TossUp game paused
        if self.manager_ref.paused and self.manager_ref.playing == None:
            if self.puzzle.answered:
                if self.puzzle.solved:
                    self.correct_label.draw()
                else:
                    self.nop_label.draw()
            #if paused (but not by a playing player, only at start or after a wrong answer), show "Space to start"
            if not self.puzzle.finished:
                self.spc_start_label.draw()
            #if puzzle fully displayed (no player won or not), show "Enter to continue"
            else:
                self.next_label.draw()

        # if a player has stopped the toss up to fill in an answer: display keyboard
        if self.manager_ref.playing != None:
            self.keyboard.Display('Full', del_en= len(self.puzzle.undo_list) > 0, solve_en= self.puzzle.filled())

    # -----------------------------------------------------------------------------------
    def Play_Puzzle(self):
        self.window.blit(pygame.transform.smoothscale(self.manager_ref.images['puzzle'], (900, 600)), ((WINDOW_WIDTH - 900) // 2, 0))
        
        if not self.puzzle.picked_puzzle:
            return

        #players small avatar boxes
        for n in range(self.manager_ref.nb_players):
            #only show current player etiquette in clear, others will be shaded
            selected = (n == self.manager_ref.playing)
            shaded = not selected
            self.players[n].Player_Etiquette_Small(15 + 1045 * (n % 2), 40 + 290 * (n // 2), selected= selected, shaded= shaded)

        # Display puzzle
        self.puzzle.Display_Puzzle()

        # If we have a message, launch a timer, display the message until the timer has expired
        if self.timers['message'].isRunning():
            msg_label = SimpleBoxText(
                x= WINDOW_WIDTH // 2, y= 60,
                text= self.manager_ref.message[0],
                font= self.fonts['large'],
                fgcolor= 'white', bgcolor= self.manager_ref.message[1]
            )
            msg_label.draw()
        else:
            self.manager_ref.message = list()

        #if not back from spin the wheel, we need to display the Buy/Spin/Solve buttons
        if not self.wheel.locked:
            self.solve_button.draw()
            self.spin_button.draw()
            if self.players[self.manager_ref.playing].curr_money < self.manager_ref.voyel_cost or \
                    self.puzzle.all_voyels_bought():
                self.buy_button.disable()
            else:
                self.buy_button.enable()
            self.buy_button.draw()

    # -----------------------------------------------------------------------------------
    def Choose_Letter(self, buy= False, solve= False, no_keyboard= False):
        self.window.blit(pygame.transform.smoothscale(self.manager_ref.images['puzzle'], (900, 600)), ((WINDOW_WIDTH - 900) // 2, 0))
        
        if not self.puzzle.picked_puzzle:
            return

        #players small avatar boxes
        for n in range(self.manager_ref.nb_players):
            #show etiquette
            selected = (n == self.manager_ref.playing)
            shaded = not selected
            self.players[n].Player_Etiquette_Small(15 + 1045 * (n % 2), 40 + 290 * (n // 2), selected= selected, shaded= shaded)

        # Display puzzle
        self.puzzle.Display_Puzzle(solving= solve)

        if no_keyboard:
            return

        # Keyboard
        if solve:
            self.keyboard.Display('Full', exclude= self.puzzle.chosen_letters, del_en= len(self.puzzle.undo_list) > 0, solve_en= self.puzzle.filled())
        else:
            kmode = 'Conso' if not buy else 'Voyel'
            self.keyboard.Display(kmode, exclude= self.puzzle.chosen_letters)

        if not buy and not solve:
            #Display amount from the wedge
            wedge_amount_label = SimpleBoxText(
                x= 120, y= 650,
                text= self.manager_ref.wedge_value,
                font= self.fonts['large'],
                fgcolor= 'white', bgcolor= "black"
            )
            wedge_amount_label.draw()

    # -----------------------------------------------------------------------------------
    def Buy(self):
        self.Choose_Letter(buy= True)

    # -----------------------------------------------------------------------------------
    def Solve(self):
        #if game paused
        if self.manager_ref.paused:
            self.Choose_Letter(no_keyboard= True)
            
            #if self.puzzle.answered:
            if self.puzzle.solved:
                self.correct_label.draw()
            else:
                self.nop_label.draw()

            self.next_label.draw()
            
        else:
            self.Choose_Letter(solve= True)

    # -----------------------------------------------------------------------------------
    def Spin(self):
        #draw wire
        self.wheel.draw_wire(self.manager_ref.playing)
        #display the player's etiquette
        self.players[self.manager_ref.playing].Player_Etiquette_Small(1000, 100, selected= True)

        #draw the wheel
        self.wheel.draw()

        #print out the value of the wedge pointed by the player's pointer
        pointed_wedge_txt = self.wheel.get_wedge_content(PLAYERS_WHEEL_OFFSET[self.manager_ref.playing])
        pointed_wedge_surf = self.fonts['large'].render(pointed_wedge_txt, True, PLAYERS_COLORS[self.manager_ref.playing])
        pointed_wedge_rect = pointed_wedge_surf.get_rect(center= (1100, 400))
        self.window.blit(pointed_wedge_surf, pointed_wedge_rect)

        #TODO: force selector
        # self.wheel.draw_force_select(1050,440)

        #Spin button to spin the wheel
        if not self.wheel.locked:
            self.wheelspin_button.draw()
        #then replaced by a "OK" button to go back to the Puzzle with the wedge value we got
        elif not self.wheel.spinning:
            self.manager_ref.wedge_value = pointed_wedge_txt
            self.wheelok_button.draw()

    # -----------------------------------------------------------------------------------
    def Scores(self):
        pass