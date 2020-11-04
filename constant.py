import time
import platform

COLOR_NEUTRAL = "grey"
COLOR_HOVERED = "yellow"
COLOR_PRESSED = "red"
DWELL_TIME = 700
PAUSE_TIME = 500
START_TIME = time.time()
FILE_NAME = 'testfile.csv'
PLATTFORM = platform.system()
KEYS = [# Key rows
    ('escape', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?', '!'),
    ('q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü'),
    ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä'),
    ('y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', 'backspace', 'enter'),
    " "]