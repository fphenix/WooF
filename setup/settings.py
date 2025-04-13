# =======================================================================================
# fPhenix 2025 : Wheel Of Fortune
# Game Settings CONSTANTS
# =======================================================================================

from math import pi as PI

TITLE = "A Wheel of Fortune Game by fphenix"

MAX_PLAYERS = 4

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MUSIC_VOLUME = 1

START_PHASE = "Play Puzzle 1"  # "Intro" 
INTRO_SCREEN_DUR = 3500 # 3500 ms
TOSS_UP_DUR = 1000 # ms

MB_LEFT = 0
MB_RIGHT = 2
MB_MID = 1

TXT_RETLN = "\n"
TXT_SPACE = " "

VOYEL_COST = 250
VOYEL_COST_FINAL = 500

TOSSUP_PRICES = [(14, 2000), (8, 1000), (1, 500)] # list of (threshold, amount)

ALPHA  = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
CONSON = list("BCDFGHJKLMNPQRSTVWXYZ")
VOYELS = list("AEIOU")
BONUS_LETTERS = list("RSTNLE")

BTN_BG_COLOR        = (255, 255, 255)
BTN_BG_COLOR_ACTIVE = (0, 0, 255)
BTN_BG_COLOR_SHADED = (128, 128, 128)

BTN_FG_COLOR        = (0, 0, 0)
BTN_FG_COLOR_ACTIVE = (255, 255, 0)
BTN_FG_COLOR_SHADED = (192, 192, 192)

BOARD_ROWS_LENGTH = [12, 14, 14, 12]

PLAYERS_COLORS = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)] # 0:red, 1:yellow, 2:green, 3:blue
PLAYERS_WHEEL_OFFSET = [7, 1, 19, 13]
PLAYERS_TOSSUP_KEYS = ["A", "C", "N", "P"]

WHEEL_NB_WEDGES = 24
WHEEL_FONT_SIZE = 28
WHEELS = [
    ["BANKRUPT", 650,         400, 300, "PASS",  600, 350, 450, 700, 300,        650, 1000, 300, 200,    600, 500,  800, 550, 400,        300, 900,  500, 700, 900],
    ["BANKRUPT", 100,         350, 700,    100, 1000, 200, 150, 250, 500, "BANKRUPT", 1500, 150, 250, "PASS", 400, 600, 100,   50,        300, 250,  300, 150, 200],
    ["BANKRUPT", 500,         800, 550,    400,  300, 900, 500, 300, 900, "BANKRUPT", 2000, 600, 300, "PASS", 800, 1500, 450, 700,        200, 600, 1000, 300, 600],
    ["BANKRUPT", 650, "FREE PLAY", 700, "PASS",  800, 550, 650, 500, 900, "BANKRUPT", 2500, 400, 300,    700, 600,  650, 500, 700, "BANKRUPT", 600,  550, 500, 600]
]
WHEEL_POINTER_OFFSET = 40

WHEEL_DAMPENER = 0.995 # 0.98
WHEEL_FORCE = 5
WHEEL_FORCE_SPAN = 2
WHEEL_STOP = 0.15

WEDGE_COLORS = {
    "BANKRUPT"  : (40, 40, 40),
    "PASS"      : (238, 238, 238),
    "FREE PLAY" : (255, 255, 172),
    "50 €"      : (96, 32, 16),
    "100 €"     : (190, 72, 10),
    "150 €"     : (180, 120, 0),
    "200 €"     : (230, 72, 5),
    "250 €"     : (255, 166, 166),
    "300 €"     : (160, 70, 128),
    "350 €"     : (224, 100, 115),
    "400 €"     : (128, 172, 172),
    "450 €"     : (64, 100, 170),
    "500 €"     : (50, 80, 110),
    "550 €"     : (0, 170, 50),
    "600 €"     : (128, 212, 32),
    "650 €"     : (255, 255, 64),
    "700 €"     : (255, 190, 0),
    "800 €"     : (255, 128, 16),
    "900 €"     : (255, 0, 0),
    "1000 €"    : (150, 150, 160),
    "1500 €"    : (255, 232, 140),
    "2000 €"    : (90, 40, 125),
    "2500 €"    : (110, 160, 200)
}

ONE_REVOLUTION = PI * 2
FORCE_ANGLE_STEP = 0.02
FORCE_ANGLE_MIN = 0
FORCE_ANGLE_MAX = ONE_REVOLUTION
