# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Puzzle Class
# =======================================================================================

from random import shuffle, choice
from setup.utils import rotate_list
from setup.utils import char_replace

from setup.settings import *

from gameobj.boxtext import BoxText

# -----------------------------------------------------------------------------------
class Puzzle:
    def __init__(self, dB, fonts, manager):
        self.dB = dB
        self.fonts = fonts
        self.manager_ref = manager

        self.reset()

    # -----------------------------------------------------------------------------------
    def reset(self):
        self.curr_category = ""
        self.curr_puzzle = ""

        self.game_name = ""

        self.offuscated = list()
        self.clear_text = list()
        self.tossup_order = list()

        self.chosen_letters = list()
        self.voyels_bought = 0

        self.undo_list = list()

        self.picked_puzzle = False
        self.category_label = None
        self.gamename_label = None

        self.answered = False
        self.solved = False
        self.finished = False

    # -----------------------------------------------------------------------------------
    # chose a puzzle from the dB
    def pick(self):
        self.picked_puzzle = True
        self.curr_category, self.curr_puzzle = choice(self.dB)
        print(self.curr_puzzle)
        self.Prepa_Category()
        self.Prep_Board()
        self.tossup_shuffle()

    # -----------------------------------------------------------------------------------
    # return the category (string) of the chosen puzzle
    def get_category(self):
        return self.curr_category

    # -----------------------------------------------------------------------------------
    # return the chosen puzzle (string)
    def get_puzzle(self):
        return self.curr_puzzle

    # -----------------------------------------------------------------------------------
    # returns how many of the letter 'letter' there is in the puzzle
    def how_many(self, letter):
        return self.curr_puzzle.count(letter)

    # -----------------------------------------------------------------------------------
    # replace all letters with '_' leaving other characters alone
    def offuscate(self, text):
        return ''.join([letter if letter not in ALPHA else '_' for letter in text])
    
    # -----------------------------------------------------------------------------------
    # Add to the chosen letters list
    def add_chosen(self, letter):
        self.chosen_letters.append(letter)
        if letter in VOYELS:
            self.voyels_bought += 1

    # -----------------------------------------------------------------------------------
    # Check if some voyels remain to be chosen (False) or if all have been bought (True)
    def all_voyels_bought(self):
        return (len(VOYELS) - self.voyels_bought) == 0

    # -----------------------------------------------------------------------------------
    # uncover all letters 'letter'
    def solve_one_letter(self, letter):
        for row, clr in enumerate(self.clear_text):
            for idx, c in enumerate(list(clr)):
                if c == letter:
                    self.offuscated[row] = char_replace(self.offuscated[row], idx, letter)
    
    # -----------------------------------------------------------------------------------
    # compare puzzle and answer to check if the answer if correct
    def check(self):
        for clr, hid in zip(self.clear_text, self.offuscated):
            if clr != hid:
                ###print(clr, "vs", hid)
                return False
        self.finished = True
        self.solved = True
        return True

    # -----------------------------------------------------------------------------------
    # check the offuscated lines to see if a character '_' remains
    # This allows to check that a full answer has been given, without checking if it is correct.
    def filled(self):
        for rowtxt in self.offuscated:
            if rowtxt.find('_') >= 0:
                return False
        return True

    # -----------------------------------------------------------------------------------
    # undo the last letter entered while fill in the puzzle
    def undo(self):
        if len(self.undo_list) > 0:
            row, col = self.undo_list.pop()
            self.offuscated[row] = char_replace(self.offuscated[row], col, '_')

    # -----------------------------------------------------------------------------------
    # undo all that has been done while filling in the puzzle
    def undo_all(self):
        while len(self.undo_list) > 0:
            row, col = self.undo_list.pop()
            self.offuscated[row] = char_replace(self.offuscated[row], col, '_')
    
    # -----------------------------------------------------------------------------------
    # is there any letters left to complete the Toss Up?
    def tossup_complete(self):
        return not len(self.tossup_order) > 0
    
    # -----------------------------------------------------------------------------------
    # During a won toss Up, how much money did we earn?
    def get_price(self):
        for threshold, price in TOSSUP_PRICES:
            if len(self.tossup_order) >= threshold:
                return price
        return 0

    # -----------------------------------------------------------------------------------
    # Used for Toss-Ups to shuffle the letters that will be revealed every second
    def tossup_shuffle(self):
        puzzle = self.clear_text
        letter_list = list()
        for row in range(len(BOARD_ROWS_LENGTH)):
            for col in range(BOARD_ROWS_LENGTH[row]):
                if puzzle[row][col] in ALPHA:
                    letter_list.append(list((puzzle[row][col], row, col)))
        shuffle(letter_list)
        self.tossup_order = letter_list
    
    # -----------------------------------------------------------------------------------
    # Generate the Category surface/text
    def Prepa_Category(self):
        self.category_label = BoxText(
            x= WINDOW_WIDTH // 2 + 20,   # self.window.get_width() // 2 + 20
            y= WINDOW_HEIGHT // 2 + 180, # self.window.get_height() // 2 + 180
            w= 580, h= 50,
            text= self.curr_category,
            font= self.fonts['normal'],
            fgcolor= 'black', bgcolor= 'white',
            infl= False
        )

        self.gamename_label = BoxText(
            x= WINDOW_WIDTH // 2,
            y= WINDOW_HEIGHT // 2 + 140,
            w= 300, h= 30,
            text= self.game_name,
            font= self.fonts['tiny'],
            fgcolor= 'white', bgcolor= 'black',
            infl= False
        )

    # -----------------------------------------------------------------------------------
    # algo to convert the string puzzle into a board puzzle (distributed and centered)
    def Prep_Board(self):
        # preparing board
        row_count = 0
        temp = ""
        row_text = ["", "", "", ""]
        for word in self.get_puzzle().split():
            if len(row_text[row_count]) == 0:
                temp = word
            else:
                separator = "" if row_text[row_count][-1] == "-" else " " # if last char of word ends with a '-' no need for a space afterwards
                temp = row_text[row_count] + separator + word

            if len(temp) > BOARD_ROWS_LENGTH[row_count]:
                row_count += 1
                row_text[row_count] += word
                temp = ""
            else:
                row_text[row_count] = temp

        # vertic center justify
        if len(row_text[1]) == 0 or len(row_text[2]) == 0:
            row_text = rotate_list(row_text, 1)

        # horiz center justify
        self.offuscated = ["", "", "", ""]
        for row, _txt in enumerate(row_text):
            padding = (BOARD_ROWS_LENGTH[row] - len(row_text[row])) // 2   # int div by 2
            row_text[row] = ("*" * padding) + row_text[row]
            row_text[row] = row_text[row] + ("*" * (BOARD_ROWS_LENGTH[row] - len(row_text[row])))
            self.offuscated[row] = self.offuscate(row_text[row])

        self.clear_text = row_text
        return([self.clear_text, self.offuscated])

    # -----------------------------------------------------------------------------------
    def Display_Puzzle(self, solving= False):
        #display the puzzle cells
        self.found_first_empty = list()
        for row in range(len(BOARD_ROWS_LENGTH)):
            for col in range(BOARD_ROWS_LENGTH[row]):
                #skip spaces and unused cells
                if self.offuscated[row][col] == "*" or self.offuscated[row][col] == " ":
                    continue

                #else add one blank cell
                offset = 1 if row == 0 or row == 3 else 0

                #Add all uncovered letters and none-alpha characters
                cell_text = ""
                if self.offuscated[row][col] != "_":
                    cell_text = self.offuscated[row][col]

                cell = BoxText(
                    x= 300 + (col+offset) * 49 + 16,
                    y= 143 + row * 71 + 36,
                    w= 34, h= 55,
                    text= cell_text,
                    font= self.fonts['large'],
                    fgcolor= 'black', bgcolor= 'white', sel_bgcolor = 'blue'
                )
        
                if solving:
                    #if a player tries to solve the puzzle, the first hidden letter is selected
                    #so that the keyboard key can fill it in
                    if len(self.found_first_empty) == 0 and cell_text == "" and self.manager_ref.playing != None:
                        self.found_first_empty = [row, col]
                        cell.select()
                    else:
                        cell.unselect()

                cell.draw()

        #Display category
        self.category_label.draw()
        self.gamename_label.draw()
