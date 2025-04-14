# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Manager file (assets imports, timers, main events loop, top level variables
# top level state machine)
# =======================================================================================

import pygame
from random import uniform

from setup.settings import *

from setup.support import import_avatars, import_img
from setup.support import import_csv_database
#from setup.support import_audio
#from setup.utils import clamp_between

from gameobj.timer import Timer
from gameobj.sm import StateMachine
from gameobj.screens import Screens
from gameobj.puzzle import Puzzle
from gameobj.wheel import Wheel
from gameobj.player import Player
from gameobj.keyboard import Keyboard

# =======================================================================================
class Manager:
    def __init__(self, main_dir):
        pygame.init()
        #pygame.init() includes the call to pygame.font.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.avatars = import_avatars(main_dir)
        self.avatars_list = list()
        for key in self.avatars.keys():
            self.avatars_list.append(key)

        self.images = {
            'intro_bg': import_img(main_dir, 'Intro.jpg'),
            'bg': import_img(main_dir, 'bg.png'),
            'puzzle': import_img(main_dir, 'puzzle.jpg'),
            'logo': import_img(main_dir, 'Logo.png')
        }
        self.fonts = {
            'intro': pygame.font.SysFont('Lucida Calligraphy', 32),
            'player': pygame.font.SysFont('Segoe UI Black', 32),
            'wheel': pygame.font.SysFont('Courier New', 30),
            'tiny' : pygame.font.SysFont("Courier New", size= 16, bold= True),
            'small' : pygame.font.SysFont("Courier New", size= 20, bold= True),
            'normal' : pygame.font.SysFont("Courier New", size= 28, bold= True),
            'large' : pygame.font.SysFont("Courier New", size= 48, bold= True)
        }
        #self.audio = import_audio(main_dir)
        self.lang = "EN" # "FR"
        self.puzzles_dB = import_csv_database(main_dir, 'GG_dB')
        self.puzzle = Puzzle(self.puzzles_dB, self.fonts, self)
        self.wheel = Wheel(
            centerx= 500, centery= WINDOW_HEIGHT // 2,
            radius= 300,
            start_angle= uniform(0.0, 359.999),
            logo= self.images['logo'],
            fonts= self.fonts
        )
        self.keyboard = Keyboard(self.fonts)

        self.nb_players = 4 # TODO : Get it from save file
        # TODO : Get it from save file
        # Name, avatar, curr_money, tot_money
        self.players = [
            Player(0, 'Eme', 'unicorn', self.fonts, self.avatars),
            Player(1, 'Aym', 'monster', self.fonts, self.avatars),
            Player(2, 'Pris', 'mandala', self.fonts, self.avatars),
            Player(3, 'Fred', 'indiana', self.fonts, self.avatars)
        ]
        self.playing = None

        self.phase = START_PHASE
        self.next_phase = self.phase
        self.prev_phase = self.phase

        self.voyel_cost = VOYEL_COST

        #timers
        self.timers = {
            'Intro': Timer(duration= INTRO_SCREEN_DUR, autostart= True), #ms
            'TossUp': Timer(duration= TOSS_UP_DUR), #ms
            'debounce': Timer(250), # 1/4 sec debounce
            'message': Timer(3000), # 3 sec message
            'answer': Timer(45000) # 45 sec to give answer
        }

        self.paused = False

        self.game_statemachine = StateMachine(self)
        self.game_screens = Screens(self)
        #give game_screens ref to game_state_machine so it know about the buttons
        self.game_statemachine.set_btn_ref(self.game_screens)

        self.game_nb = 0
        self.wedge_value = None # text

        self.message = list()  # [string, bgcolor]

    # -----------------------------------------------------------------------------------
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    # -----------------------------------------------------------------------------------
    def update(self):
        self.phase = self.next_phase
        match self.phase:
            case 'Intro':
                self.game_statemachine.Intro()
            case 'Setup':
                self.game_statemachine.Setup()
            case "Toss Up Rules":
                self.game_statemachine.Toss_up_Rules()
            case "Toss Up 1" | "Toss Up 2" | "Toss Up 3":
                self.game_statemachine.Toss_up()
            case "Break":
                self.game_statemachine.AdBreak("Play Puzzle 1")
            case "Play Puzzle" | "Play Puzzle 1" | "Play Puzzle 2" | "Play Puzzle 3" | "Play Puzzle 4":
                self.game_statemachine.Play_Puzzle()
            case "Spin":
                self.game_statemachine.Spin()
            case "Choose":
                self.game_statemachine.Choose_Letter()
            case "Buy":
                self.game_statemachine.Buy()
            case "Solve":
                self.game_statemachine.Solve()
            #case "Final Spin":
            #    self.game_statemachine.Final_Spin()
            #case "Bonus":
            #    self.game_statemachine.Bonus()
            case "Scores":
                self.game_statemachine.Scores()

        self.update_timers()

    # -----------------------------------------------------------------------------------
    def draw_screen(self, dt= 0):
        match self.phase:
            case 'Intro':
                self.game_screens.Intro()
            case 'Setup':
                self.game_screens.Setup()
            case "Toss Up Rules":
                self.game_screens.Toss_up_Rules()
            case "Toss Up 1" | "Toss Up 2" | "Toss Up 3":
                self.game_screens.Toss_up()
            case "Break":
                self.game_screens.AdBreak()
            case "Play Puzzle" | "Play Puzzle 1" | "Play Puzzle 2" | "Play Puzzle 3" | "Play Puzzle 4":
                self.game_screens.Play_Puzzle()
            case "Spin":
                self.game_screens.Spin()
            case "Choose":
                self.game_screens.Choose_Letter()
            case "Buy":
                self.game_screens.Buy()
            case "Solve":
                self.game_screens.Solve()
            #case "Final Spin":
            #    self.game_screens.Final_Spin()
            #case "Bonus":
            #    self.game_screens.Bonus()
            case "Scores":
                self.game_screens.Scores()

    # -----------------------------------------------------------------------------------
    def draw(self):
        self.window.fill((30, 30, 30))
        
        self.draw_screen()

        pygame.display.update()    # flip() refresh immedialty, update refresh once per frame and with update can refresh only part of the screen

    # -----------------------------------------------------------------------------------
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if self.phase == 'Toss Up 1' or self.phase == 'Toss Up 2' or self.phase == 'Toss Up 3':
                    if event.type == pygame.KEYDOWN:
                        #check for Space or RETURN key to unpause and continue
                        if self.paused:  
                            if event.key == pygame.K_SPACE and not self.puzzle.finished:
                                self.paused = False
                            if event.key == pygame.K_RETURN and self.puzzle.finished:
                                self.paused = False
                        # check for players' "pause" keys during TossUps (A, C, N, P)
                        else: 
                            for n in range(self.nb_players):
                                if event.key == ord(self.players[n].key.lower()):
                                    self.playing = n
                                    self.paused = True

                if self.phase == 'Solve':
                    if event.type == pygame.KEYDOWN:
                        #check for Space or RETURN key to unpause and continue
                        if self.paused:  
                            if event.key == pygame.K_SPACE:
                                self.paused = False
                            if event.key == pygame.K_RETURN:
                                self.paused = False


                if self.phase == "Spin":
                    # TODO: Force selector
                    # if pygame.mouse.get_pressed()[MB_LEFT]:
                    #     self.wheel.force_angle += FORCE_ANGLE_STEP
                    # elif pygame.mouse.get_pressed()[MB_RIGHT]:
                    #     self.wheel.force_angle -= FORCE_ANGLE_STEP
                    # self.wheel.force_angle = clamp_between(self.wheel.force_angle, FORCE_ANGLE_MIN, FORCE_ANGLE_MAX)
                    pass

            self.update()
            self.draw()
