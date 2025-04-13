# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Game State-Machine
# =======================================================================================

#import pygame
from setup.settings import *

from setup.utils import circulate, char_replace, plural

# =======================================================================================
class StateMachine:
    def __init__(self, manager):
        self.manager_ref = manager
        self.puzzle = manager.puzzle
        self.timers = manager.timers
        self.players = manager.players
        self.wheel = manager.wheel
        self.keyboard = manager.keyboard

        self.btn_ref = None

    # -----------------------------------------------------------------------------------
    def set_btn_ref(self, ref):
        self.btn_ref = ref

    # -----------------------------------------------------------------------------------
    # Wait for a ~4 sec autotimer
    # whilst displaying the game image and the logo.
    # Once the timer ends, change phase to "Setup"
    def Intro(self):
        if not self.timers['Intro'].isRunning():
            self.manager_ref.next_phase = "Setup" 

    # -----------------------------------------------------------------------------------
    # Wait for a ~4 sec autotimer
    # whilst displaying the game image and the logo.
    # Once the timer ends, change phase to "Setup"
    def AdBreak(self, next):
        if not self.timers['Intro'].isRunning():
            self.manager_ref.next_phase = next

    # -----------------------------------------------------------------------------------
    # TODO: If a setup file exist, load it as default values
    # Display the Setup layout (nb player, names, color & avatars)
    # Use keyboard & mouse events to let the users change their name&avatar
    # If "Let's play" is clicked then TODO : save setup file
    # and change phase to "Toss Up Rules"
    def Setup(self):
        for n in range(MAX_PLAYERS):
            if self.btn_ref.setup_buttons[n].check_clicked() and \
                    not self.timers['debounce'].isRunning():
               self.timers['debounce'].activate()
               self.btn_ref.setup_buttons[self.manager_ref.nb_players - 1].unselect()
               self.manager_ref.nb_players = n + 1
               self.btn_ref.setup_buttons[n].select()

            for side in ['left', 'right']:
                if self.btn_ref.avatar_sel_buttons[str(n) + '_' + side].check_clicked() and \
                        not self.timers['debounce'].isRunning():
                    self.timers['debounce'].activate()
                    idx = self.manager_ref.avatars_list.index(self.players[n].avatar)
                    idx = idx - 1 if side == 'left' else idx + 1
                    idx = circulate(idx, 0, len(self.manager_ref.avatars_list) - 1)
                    self.players[n].avatar = self.manager_ref.avatars_list[idx]

        if self.btn_ref.play_button.check_clicked() and not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.manager_ref.next_phase = "Toss Up Rules"

    # -----------------------------------------------------------------------------------
    # Display the toss up rules and the keys:
    #       Player1 "A", Player 2 "C", Player3 "N", Player4 "P".
    # << "Every second, one letter will be is displayed. As soon as you
    # think you know the answer, you click your assigned keyboard key
    # and you complete the puzzle.
    # If it is incorrect you can no longer participate to this puzzle.
    # If it is correct you win some money.
    # Click "Let's go" to begin" >>
    # If space is pressed change phase to "Toss Up 1"
    def Toss_up_Rules(self):
        if self.btn_ref.play_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.manager_ref.next_phase = "Toss Up 1"
            self.manager_ref.paused = True

    # -----------------------------------------------------------------------------------
    # Display the game board, the category
    # Display the avatars, etc, total money of the player and their assigned letter
    # Every second a random letter is revealed
    # If someone press their key then go to "Solve"
    #  
    # Depending on result from solve, resume (without the player who stopped the game because he lost)
    # or player wins (add to total-money depending on time left 2000, 1000 or 500)
    # and change phase
    # Note: if full puzzle is revealed then stop, nobody wins, phase also moves to next
    def Toss_up(self):
        #pick up a puzzle in the dB if not already
        if not self.puzzle.picked_puzzle:
            self.puzzle.game_name = self.manager_ref.phase
            self.puzzle.pick()
            self.manager_ref.paused = True # to read the category before starting by pressing SPACE

        #if not paused, reset "answered" flag
        if not self.manager_ref.paused:
            self.puzzle.answered = False

        #if not paused, uncover one letter every second
        if not self.puzzle.finished and not self.manager_ref.paused and not self.timers['TossUp'].isRunning():
            self.timers['TossUp'].activate()
            letter, r, c = self.puzzle.tossup_order.pop()
            self.puzzle.offuscated[r] = char_replace(self.puzzle.offuscated[r], c, letter)

        # one of the players has stopped the Toss up to complete the puzzle
        if self.manager_ref.playing != None:
            for letter in ALPHA:
                if self.keyboard.keys[letter].isEnabled() and \
                        self.keyboard.keys[letter].check_clicked() and \
                        not self.timers['debounce'].isRunning():
                    #debounce
                    self.timers['debounce'].activate()
                    # get keyboard button pressed by player and place it at first empty place
                    if len(self.puzzle.found_first_empty) == 0:
                        break
                    row, col = self.puzzle.found_first_empty
                    char_key = (self.keyboard.keys[letter].get_value())
                    self.puzzle.undo_list.append([row, col]) 
                    self.puzzle.offuscated[row] = char_replace(self.puzzle.offuscated[row], col, char_key)
            
            #player clicked on Delete
            if self.keyboard.delete_button.check_clicked() and \
                    not self.timers['debounce'].isRunning():
                self.timers['debounce'].activate()
                self.puzzle.undo()

            #player clicked on Validate Button to register the solution
            elif self.keyboard.validate_button.check_clicked() and \
                    not self.timers['debounce'].isRunning():
                #debounce
                self.timers['debounce'].activate()
                # is the puzzle solved?
                isSolved = self.puzzle.check()
                # if answer is Wrong
                if not isSolved:
                    # undo all
                    self.puzzle.undo_all()
                    # ban player
                    self.players[self.manager_ref.playing].ban()
                else:
                    #get goints in tot_money
                    amount = self.puzzle.get_price()
                    self.players[self.manager_ref.playing].add_to_total(amount)
                    # and go to next phase (where we'll need to reset bans, puzzle, etc.)
                    self.puzzle.finished = True

                self.puzzle.answered = True
                self.manager_ref.paused = True
                self.manager_ref.playing = None

        #if puzzle fully revealed then ban all
        # pause and go to next phase upon pressing ENTER
        if not self.puzzle.finished and self.puzzle.tossup_complete() and not self.manager_ref.paused:
            for n in range(self.manager_ref.nb_players):
                self.players[n].ban()
            self.puzzle.finished = True
            self.manager_ref.paused = True
            self.manager_ref.playing = None
        
        #if puzzle finished and unpaused: go to next phase
        if self.puzzle.finished and not self.manager_ref.paused:
            self.puzzle.reset()
            #unban all
            for n in range(self.manager_ref.nb_players):
                self.players[n].unban()
            if self.manager_ref.phase == "Toss Up 1":
                self.manager_ref.next_phase = "Toss Up 2"
            elif self.manager_ref.phase == "Toss Up 2":
                self.timers['Intro'].activate()
                self.manager_ref.next_phase = "Break"
            elif self.manager_ref.phase == "Toss Up 3":
                if self.manager_ref.nb_players < 4:
                    self.manager_ref.next_phase = "Final Spin"
                else:
                    self.manager_ref.next_phase = "Play Puzzle 3"

    # -----------------------------------------------------------------------------------
    def next_player(self):
        self.manager_ref.playing = (self.manager_ref.playing + 1) % self.manager_ref.nb_players
        self.manager_ref.wedge_value = None
        self.wheel.locked = False

    # -----------------------------------------------------------------------------------
    # If not yet, pick up a puzzle in the dB
    # For puzzle n° N, player n° N begins
    # Display the game board, the category
    # Display the avatars, etc, total money, highlighting current playing player
    # show buttons : 
    #     Free Play, if the player has one
    #     Solve, 
    #     Buy voyel (-250€) (unavailable if player does not have the money for it),
    #     Spin
    # if solved, then winner adds their money to total, everyone money gotes to 0
    # go to next phase (Puzzle 2, Toss Up 3 Puzzle 4, Final)
    def Play_Puzzle(self):
        if not self.puzzle.picked_puzzle:
            self.puzzle.game_name = self.manager_ref.phase
            self.puzzle.pick()
            self.timers['message'].deactivate()
            self.manager_ref.message = list()
            self.manager_ref.game_nb = int(self.manager_ref.phase[-1])  # last char of phase is player n° N (1 to 4) 
            self.manager_ref.playing = self.manager_ref.game_nb - 1     # so playing n° 0 to 3
            self.wheel.choose_wheel(self.manager_ref.playing)
            for n in range(self.manager_ref.nb_players):
                self.players[n].unban()
                self.players[n].curr_money = 0

        # If we have a message, launch a timer, display the message until the timer has expired
        if len(self.manager_ref.message) > 0 and not self.timers['message'].isRunning():
            self.timers['message'].activate()
            
        # Click the spin button
        if self.btn_ref.spin_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.wheel.unlock()
            self.manager_ref.wedge_value = None
            self.manager_ref.prev_phase = self.manager_ref.phase
            self.timers['message'].deactivate()
            self.manager_ref.next_phase = "Spin"

        # Click the Buy a voyel button
        if self.btn_ref.buy_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.manager_ref.next_phase = "Buy"

        # CLick the try to solve button
        if self.btn_ref.solve_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.manager_ref.next_phase = "Solve"

        # if back from spin the wheel, do what is needed upon the wedge value
        if self.manager_ref.wedge_value != None:
            match self.manager_ref.wedge_value:
                case "BANKRUPT":
                    self.players[self.manager_ref.playing].bankrupt()
                    self.manager_ref.message = ['BANKRUPT :(', 'blue']
                    self.next_player()
                case "PASS":
                    self.manager_ref.message = ['PASS...', 'blue']
                    self.next_player()
                case "FREE PLAY":
                    pass # TODO
                case _:
                    self.players[self.manager_ref.playing].wedge_int = int(self.manager_ref.wedge_value.split()[0]) # convert the string (eg "550 €") into an integer (550)
                    self.manager_ref.prev_phase = self.manager_ref.phase
                    self.manager_ref.next_phase = "Choose"

    # -----------------------------------------------------------------------------------
    #display player solving name & avatar
    #display puzzle, category and consonants alphabet (available leters highlighted, already choosen and voyels darkened)
    #player choose 1 letter;
    #if none of that letter : pass : return to puzzle with next player
    #else display all of that letter, nb*amount adds to current money
    #then phase to puzzle
    def Choose_Letter(self, buy= False):
        for letter in ALPHA:
            if self.keyboard.keys[letter].isEnabled() and \
                    self.keyboard.keys[letter].check_clicked() and \
                    not self.timers['debounce'].isRunning():
                #debounce
                self.timers['debounce'].activate()
                # what key was clicked?
                char_key = (self.keyboard.keys[letter].get_value())
                # add it to chosen list
                self.puzzle.add_chosen(char_key)
                # is that letter in the puzzle?
                nb_picked_letter = self.puzzle.how_many(char_key)
                
                #if buy mode, take away voyel cost from curr_money amount
                if buy:
                    self.players[self.manager_ref.playing].add_to_curr(self.manager_ref.voyel_cost * -1)
                #if not: pass
                if nb_picked_letter < 1:
                    self.next_player()
                    self.manager_ref.message = [" There's no \"" + char_key + "\" ! ", 'red']
                #if yes, uncover every of that letter (get number to calculate points)
                else:
                    if not buy:
                        self.players[self.manager_ref.playing].add_to_curr(nb_picked_letter * self.players[self.manager_ref.playing].wedge_int)
                    msg = " There " + plural('is ', nb_picked_letter, 'are ', replace= True) + str(nb_picked_letter) + " \"" + char_key + "\" ! "
                    self.manager_ref.message = [msg, 'green']
                    self.puzzle.solve_one_letter(char_key)
                    self.manager_ref.wedge_value = None
                    self.wheel.locked = False
                #then go back to puzzle_play
                self.manager_ref.next_phase = "Play Puzzle"
                break

    # -----------------------------------------------------------------------------------
    #display player solving name & avatar
    #display puzzle, category and voyels alphabet (available leters highlighted, already bought lettersz darkened)
    #player choose 1 letter to buy;
    #if none of that letter : pass : return to puzzle with next player
    #else display all of that letter, sub 250 from current money
    #then phase to puzzle
    def Buy(self):
        self.Choose_Letter(buy= True)

    # -----------------------------------------------------------------------------------
    #display board, category, player solving name & avatar
    #display full alphabet (including voyels) and Pass & Delete
    #(alphabet bg color = player color)
    #player click the letters to complete the puzzle; Pass becomes "Solve"
    #when full puzzle is completed
    #note : there is a 1 minute timer
    #if player is right: wins : display avatar name and money earned
    #else - for toss up solve : player can no longer play that puzzle
    #for puzzle solve : pass
    #then phase resumes where it was
    def Solve(self):
        for letter in ALPHA:
            #has a player clicked on a letter?
            if self.keyboard.keys[letter].isEnabled() and \
                    self.keyboard.keys[letter].check_clicked() and \
                    not self.timers['debounce'].isRunning():
                #debounce
                self.timers['debounce'].activate()
                # get keyboard button pressed by player and place it at first empty place
                if len(self.puzzle.found_first_empty) == 0:
                    break
                row, col = self.puzzle.found_first_empty
                char_key = (self.keyboard.keys[letter].get_value())
                self.puzzle.undo_list.append([row, col]) 
                self.puzzle.offuscated[row] = char_replace(self.puzzle.offuscated[row], col, char_key)
            
        #player clicked on Delete
        if self.keyboard.delete_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.puzzle.undo()

        #player clicked on Validate Button to register the solution
        elif self.keyboard.validate_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            #debounce
            self.timers['debounce'].activate()
            # is the puzzle solved?
            isSolved = self.puzzle.check()
            # if answer is Wrong, undo and Pass
            if not isSolved:
                # undo all
                self.puzzle.undo_all()
                # message : incorrect
                #self.manager_ref.message = ["That\'s not correct !", 'red']
                # pass player
                self.next_player()
                self.puzzle.finished = False
            else:
                #get goints in tot_money
                self.players[self.manager_ref.playing].bank()
                # and go to next phase (where we'll need to reset bans, puzzle, etc.)
                self.puzzle.finished = True
                #self.manager_ref.message = ["Well Done !", 'blue']

            self.puzzle.answered = True
            self.manager_ref.paused = True

        #if puzzle finished and unpaused: go to next phase
        if self.puzzle.finished and not self.manager_ref.paused and self.puzzle.answered:
            self.puzzle.reset()
            ####print(self.manager_ref.game_nb,  self.manager_ref.next_phase, self.manager_ref.nb_players )
            match self.manager_ref.game_nb:
                case 1 :
                    self.manager_ref.next_phase = "Play Puzzle 2"
                
                case 2:
                    if self.manager_ref.nb_players == 1:
                        self.manager_ref.next_phase = "Play Puzzle 3"
                    else:
                        self.manager_ref.playing = None
                        self.manager_ref.next_phase = "Toss Up 3"

                case 3:
                    if self.manager_ref.nb_players == 1:
                        self.manager_ref.next_phase = "Final Spin"
                    else:
                        self.manager_ref.next_phase = "Play Puzzle 4"
            
                case 4:
                    self.manager_ref.next_phase = "Final Spin"

        elif not self.puzzle.finished and not self.manager_ref.paused and self.puzzle.answered:
            self.puzzle.answered = False
            self.manager_ref.next_phase = "Play Puzzle"
            
    # -----------------------------------------------------------------------------------
    # player chooses force and rolls wheel
    #if bankrupt : lose money and pass, if lose a turn : pass (goto next player)
    #if free play : adds a button, when used : voyels are also freee, and consonant earns 500 if any or 0 if non but without passing turn
    # or a wrong solve does not pass. Once used, disapeares. Cannot be saved for another puzzle
    #if amount: phase move to "Choose"
    def Spin(self):
        self.wheel.update()

        if self.btn_ref.wheelspin_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.wheel.launch()

        if self.btn_ref.wheelok_button.check_clicked() and \
                not self.timers['debounce'].isRunning():
            self.timers['debounce'].activate()
            self.manager_ref.next_phase = "Play Puzzle"

    # -----------------------------------------------------------------------------------
    #a random aount is selected (as if wheel spun)
    #a puzzle is selected
    #player with most total money starts:
    #   choose 1 letter (amongst all 26 if not yet choosen)
    #   if none pass, else selected_amont * nb goes to current money
    #then can solve or pass
    #once solved, tally total mony the player with the most money go to Bonus round
    def Final_Spin(self):
        pass

    # -----------------------------------------------------------------------------------
    #a puzzle is choosen from the db (must not contain too many letters)
    #all RSTLN and Es are revealed
    #player choose 3 consonnant + 1 voyel
    #try to solve and win big price (chosen randomly)
    def Bonus(self):
        given_letter = BONUS_LETTERS
        pass
   
    # -----------------------------------------------------------------------------------
    # display final results & stats
    # save high scores
    # play again or quit
    def Scores(self):
        pass

