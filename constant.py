import time
import platform
from pathlib import Path

COLOR_NEUTRAL = 'grey5'
COLOR_HOVERED = 'yellow'
COLOR_PRESSED = 'red'
COLOR_BACKGROUND = 'grey0'
COLOR_HIGHLIGHT = 'white'
START_DWELL_TIME = 700
PAUSE_TIME = 200
START_TIME = time.time()
TYPING_TIME = 600000
LOG_FILE_GAZE = 'LogGaze.csv'
LOG_FILE_KEYS = 'LogKeys.csv'
LOG_FILE_FOLDER = Path('Log_Files/')
FILE_PHRASES = 'phrases.txt'
PLATFORM = platform.system()

KEYS_QWERTY = [  # Key rows
    ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'back'),
    ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'),
    ('z', 'x', 'c', 'v', 'b', 'n', 'm', 'space', 'enter')
]
