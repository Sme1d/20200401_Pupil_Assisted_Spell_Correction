import time
import platform

COLOR_NEUTRAL = "slate gray"
COLOR_HOVERED = "yellow"
COLOR_PRESSED = "red"
DWELL_TIME = 700
PAUSE_TIME = 500
START_TIME = time.time()
LOG_FILE_GAZE = 'Log_Files/LogGaze.csv'
LOG_FILE_KEYS = 'Log_Files/LogKeys.csv'
FILE_PHRASES = 'phrases.txt'
PLATFORM = platform.system()
TOTAL_TIME = 5000

KEYS_QWERTY = [  # Key rows
    ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'back'),
    ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'),
    ('z', 'x', 'c', 'v', 'b', 'n', 'm', 'space', 'enter')
]
