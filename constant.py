import time
import platform

COLOR_NEUTRAL = 'grey5'
COLOR_HOVERED = 'yellow'
COLOR_PRESSED = 'red'
COLOR_BACKGROUND = 'grey0'
COLOR_HIGHLIGHT = 'white'
START_DWELL_TIME = 700
PAUSE_TIME = 500
START_TIME = time.time()
LOG_FILE_GAZE = '/LogGaze.csv'
LOG_FILE_KEYS = '/LogKeys.csv'
LOG_FILE_PATH = 'Log_Files/'
FILE_PHRASES = 'phrases.txt'
PLATFORM = platform.system()
TOTAL_TIME = 11000

KEYS_QWERTY = [  # Key rows
    ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'back'),
    ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'),
    ('z', 'x', 'c', 'v', 'b', 'n', 'm', 'space', 'enter')
]
