import time
import tkinter as tk
import tkinter.font as tk_font
from functools import partial
import os
from pathlib import  Path

import tobii_research as tr

import constant


def get_time_stamp():
    return int((time.time() - constant.START_TIME) * 1000)


def color_widget(widget, color):
    if constant.PLATFORM == "Darwin":
        widget['highlightbackground'] = color
    else:
        widget['bg'] = color


def key_press(key):
    global is_typing

    log_key_event('Key Press', key)
    if key == 'Enter':
        load_new_phrase()
        input_entry.delete(0, 'end')
        switch_typing(False)
    else:
        switch_typing(True)
        if key == 'Back':
            input_entry.delete(len(input_entry.get()) - 1)
        elif key == 'Space':
            input_entry.insert('end', ' ')
        else:
            input_entry.insert('end', key.lower())

def switch_typing(value):
    global is_typing
    global typing_time_stamp
    global overall_typing_time

    if is_typing != value:
        is_typing = value
        if is_typing:
            typing_time_stamp = get_time_stamp()
        else:
            overall_typing_time += get_time_stamp() - typing_time_stamp
            print(overall_typing_time)
            if overall_typing_time >= constant.TYPING_TIME:
                finish()


def setup_input():
    font_input = tk_font.Font(size=20)
    label = tk.Label(frame, fg=constant.COLOR_HIGHLIGHT, bg=constant.COLOR_BACKGROUND, font=font_input)
    label.pack(side='top', pady=(15, 0))

    entry = tk.Entry(frame, width=40, bg=constant.COLOR_HIGHLIGHT, justify='center', fg='black',
                     insertbackground='black',
                     font=font_input)
    entry.pack(side='top', pady=(0, 15))
    entry.focus_set()
    return label, entry


def setup_input2():
    global input_entry
    global input_label
    global dwell_time_label

    input_frame = tk.Frame(frame, bg=constant.COLOR_BACKGROUND)
    input_frame.pack(side='top', fill='both', pady=(0, 15))

    left_frame = tk.Frame(input_frame, bg=constant.COLOR_BACKGROUND)
    left_frame.pack(side='left')

    font_input = tk_font.Font(size=20)
    input_label = tk.Label(left_frame, fg=constant.COLOR_HIGHLIGHT, bg=constant.COLOR_BACKGROUND, font=font_input,
                           text='Find a dwell time which suits you')
    input_label.pack(side='top', padx=(6, 0), anchor='w', pady=(15, 0))

    input_entry = tk.Entry(left_frame, width=40, bg=constant.COLOR_HIGHLIGHT, fg='black',
                           insertbackground='black',
                           font=font_input)
    input_entry.pack(side='top', padx=(6, 0))
    input_entry.focus_set()

    dwell_time_frame = tk.Frame(input_frame, bg=constant.COLOR_BACKGROUND)
    dwell_time_frame.pack(side='right', anchor='s')

    minus_button = tk.Button(dwell_time_frame, text='-50ms', width=4, height=2, bd=0, highlightthickness=0,
                             font=font_input, bg=constant.COLOR_BACKGROUND, fg=constant.COLOR_HIGHLIGHT,
                             command=partial(change_dwell_time, -50))
    dwell_time_label = tk.Label(dwell_time_frame, fg=constant.COLOR_HIGHLIGHT, bg=constant.COLOR_BACKGROUND,
                                font=font_input, text=str(constant.START_DWELL_TIME) + 'ms')
    plus_button = tk.Button(dwell_time_frame, text='+50ms', width=4, height=2, bd=0, highlightthickness=0,
                            font=font_input, bg=constant.COLOR_BACKGROUND, fg=constant.COLOR_HIGHLIGHT,
                            command=partial(change_dwell_time, 50))
    minus_button.pack(side='left', padx=(0, 7))
    dwell_time_label.pack(side='left', padx=(0, 7))
    plus_button.pack(side='left')
    color_widget(minus_button, constant.COLOR_NEUTRAL)
    color_widget(plus_button, constant.COLOR_NEUTRAL)


def setup_log_files():
    global file_path

    participant_number = str(len(os.listdir(constant.LOG_FILE_FOLDER)))

    for i in range(3 - len(participant_number)):
        participant_number = '0' + participant_number

    participant_number = 'P' + participant_number

    file_path = constant.LOG_FILE_FOLDER / participant_number
    os.mkdir(file_path)

    log_file_keys = open(file_path / constant.LOG_FILE_KEYS, 'w')
    log_file_keys.write('time, event, related key, current phrase, current input\n')
    log_file_keys.close()

    log_file_gaze = open(file_path / constant.LOG_FILE_GAZE, 'w')
    log_file_gaze.write(', gaze point, , gaze point validity, , pupil size, , pupil validity\n')
    log_file_gaze.write('time, X, Y, L, R, L, R, L, R\n')
    log_file_gaze.close()


def change_dwell_time(change_value):
    global dwell_time
    dwell_time += change_value
    dwell_time_label['text'] = str(dwell_time) + 'ms'


# Load Phrases
def load_phrases():
    file_phrases = open(constant.FILE_PHRASES, 'r')
    loaded_phrases = file_phrases.readlines()
    file_phrases.close()
    return loaded_phrases


def setup_keyboard():
    font_keys = tk_font.Font(size=24)

    for i in range(0, len(constant.KEYS_QWERTY)):
        store_key_row = tk.Canvas(frame, bg=constant.COLOR_BACKGROUND, highlightthickness=0)
        store_key_row.pack(anchor='center')

        # Placeholder to indent key rows according to physical layout
        placeholder = tk.Canvas(store_key_row, width=(56 * i - 33), height=50, bg=constant.COLOR_BACKGROUND,
                                highlightthickness=0)
        placeholder.pack(side='left', fill='y')

        for k in constant.KEYS_QWERTY[i]:
            k = k.capitalize()
            store_key = tk.Button(store_key_row, text=k, width=4, height=3, bd=0, highlightthickness=0, font=font_keys,
                                  command=partial(key_press, k), fg=constant.COLOR_HIGHLIGHT)

            if k == 'Enter' or k == 'Back':
                store_key.pack(side='right', padx=(20, 0), pady=(0, 3))
            else:
                store_key.pack(side='left', anchor='w', padx=(0, 3), pady=(0, 3))
            color_widget(store_key, constant.COLOR_NEUTRAL)

            if k == 'Space':
                store_key['width'] = 12


def setup_eyetracker():
    found_eyetrackers = tr.find_all_eyetrackers()
    found_eyetrackers[0].subscribe_to(tr.EYETRACKER_GAZE_DATA, check_gaze, as_dictionary=True)


def load_new_phrase():
    global phrases
    log_key_event('New Phrase', None)

    new_phrase = phrases.pop(0)
    new_phrase = new_phrase[0:len(new_phrase) - 1]
    input_label['text'] = new_phrase


def log_gaze_event(gaze_data):
    file = open(file_path / constant.LOG_FILE_GAZE, 'a')
    gaze_point = get_gaze_point_on_screen(gaze_data)
    file.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}\n'.format(
        get_time_stamp(), gaze_point[0], gaze_point[1],
        gaze_data['left_gaze_point_validity'], gaze_data['right_gaze_point_validity'],
        gaze_data['left_pupil_diameter'], gaze_data['right_pupil_diameter'],
        gaze_data['left_pupil_validity'], gaze_data['right_pupil_validity']))
    file.close()


def log_key_event(event, related_key):
    file = open(file_path / constant.LOG_FILE_KEYS, 'a')
    file.write(
        '{0}, {1}, {2}, {3}, {4}\n'.format(get_time_stamp(), event, related_key, input_label['text'],
                                           input_entry.get()))
    file.close()


def get_gaze_point_on_screen(gaze_data):
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    x_on_screen = ((left[0] + right[0]) / 2) * canvas.winfo_width()
    y_on_screen = ((left[1] + right[1]) / 2) * canvas.winfo_height()
    return x_on_screen, y_on_screen


def check_gaze(gaze_data):
    global selected_widget
    global selection_time
    global key_pressed

    log_gaze_event(gaze_data)
    gaze_point = get_gaze_point_on_screen(gaze_data)

    hovered_widget = root.winfo_containing(gaze_point[0], gaze_point[1])
    if not key_pressed:
        if type(hovered_widget) == tk.Button:
            if hovered_widget == selected_widget:
                if (get_time_stamp() - selection_time) > dwell_time:
                    # key press
                    selected_widget.invoke()
                    key_pressed = True
                    color_widget(selected_widget, constant.COLOR_PRESSED)
            else:
                if selected_widget:
                    # Deselect previously selected key
                    color_widget(selected_widget, constant.COLOR_NEUTRAL)
                    log_key_event('Key Deselected', selected_widget['text'])
                # Select new key
                selected_widget = hovered_widget
                color_widget(selected_widget, constant.COLOR_HOVERED)
                log_key_event('Key Selected', selected_widget['text'])
                selection_time = get_time_stamp()
        else:
            # Deselect previously selected key
            color_widget(selected_widget, constant.COLOR_NEUTRAL)
            log_key_event('Key Deselected', selected_widget['text'])
    elif get_time_stamp() - selection_time >= dwell_time + constant.PAUSE_TIME:
        # End selection pause
        key_pressed = False
        color_widget(selected_widget, constant.COLOR_NEUTRAL)
        log_key_event('Pause Ended', selected_widget['text'])
        selected_widget = None


def finish():
    # found_eyetrackers = tr.find_all_eyetrackers()
    # found_eyetrackers[0].unsubscribe_from(tr.EYETRACKER_GAZE_DATA, check_gaze)
    root.destroy()


# Variables
selected_widget = None
selection_time = None
key_pressed = False
file_path = ''
dwell_time = constant.START_DWELL_TIME
is_typing = False
overall_typing_time = 0
typing_time_stamp = 0

input_label = None
input_entry = None
dwell_time_label = None


# Setup Tkinter
root = tk.Tk()
root.title("Gaze Typing")
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root, highlightthickness=0, bg=constant.COLOR_BACKGROUND)
canvas.pack(fill='both', expand=True)
frame = tk.Frame(canvas, bg=constant.COLOR_BACKGROUND)
frame.pack(fill="none", expand=True)

# setup_input()
setup_input2()

setup_log_files()
phrases = load_phrases()
# load_new_phrase()
setup_keyboard()
# setup_eyetracker()

root.mainloop()
