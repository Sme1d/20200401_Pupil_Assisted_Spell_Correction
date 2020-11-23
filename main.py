import time
import tkinter as tk
import tkinter.font as tk_font
from functools import partial

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
    if key == 'Enter':
        load_new_phrase()
        text_entry.delete(0, 'end')
    elif key == 'Back':
        text_entry.delete(len(text_entry.get()) - 1)
    elif key == 'Space':
        text_entry.insert('end', ' ')
    else:
        text_entry.insert('end', key.lower())


def setup_log_files():
    log_file_keys = open(constant.LOG_FILE_KEYS, 'w')
    log_file_keys.write('time, event, related key, current phrase, current input\n')
    log_file_keys.close()

    log_file_gaze = open(constant.LOG_FILE_GAZE, 'w')
    log_file_gaze.write(', gaze point, , gaze point validity, , pupil size, , pupil validity\n')
    log_file_gaze.write('time, X, Y, L, R, L, R, L, R\n')
    log_file_gaze.close()


# Load Phrases
def load_phrases():
    file_phrases = open(constant.FILE_PHRASES, 'r')
    loaded_phrases = file_phrases.readlines()
    file_phrases.close()
    return loaded_phrases


def setup_keyboard():
    for i in range(0, len(constant.KEYS_QWERTY)):
        store_key_row = tk.Canvas(frame, bg=constant.COLOR_BACKGROUND, highlightthickness=0)
        store_key_row.pack(anchor='center')

        # Placeholder to indent key rows according to physical layout
        placeholder = tk.Canvas(store_key_row, width=(56 * i - 33), height=50, bg=constant.COLOR_BACKGROUND, highlightthickness=0)
        placeholder.pack(side='left', fill='y')
        #color_widget(placeholder, constant.COLOR_BACKGROUND)

        for k in constant.KEYS_QWERTY[i]:
            k = k.capitalize()
            store_key = tk.Button(store_key_row, text=k, width=5, height=3, bd=0, highlightthickness=0, font=font_keys,
                                  command=partial(key_press, k))

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
    new_phrase = new_phrase[0:len(new_phrase) - 3]
    text_label['text'] = new_phrase


def log_gaze_event(gaze_data):
    file = open(constant.LOG_FILE_GAZE, 'a')
    gaze_point = get_gaze_point_on_screen(gaze_data)
    file.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}\n'.format(
        get_time_stamp(), gaze_point[0], gaze_point[1],
        gaze_data['left_gaze_point_validity'], gaze_data['right_gaze_point_validity'],
        gaze_data['left_pupil_diameter'], gaze_data['right_pupil_diameter'],
        gaze_data['left_pupil_validity'], gaze_data['right_pupil_validity']))
    file.close()


def log_key_event(event, related_key):
    file = open(constant.LOG_FILE_KEYS, 'a')
    file.write(
        '{0}, {1}, {2}, {3}, {4}\n'.format(get_time_stamp(), event, related_key, text_label['text'],
                                           text_entry.get()))
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
                if (get_time_stamp() - selection_time) > constant.DWELL_TIME:
                    # key press
                    selected_widget.invoke()
                    key_pressed = True
                    color_widget(selected_widget, constant.COLOR_PRESSED)
                    log_key_event('Key Press', selected_widget['text'])
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
    elif get_time_stamp() - selection_time >= constant.DWELL_TIME + constant.PAUSE_TIME:
        # End selection pause
        key_pressed = False
        color_widget(selected_widget, constant.COLOR_NEUTRAL)
        log_key_event('Pause Ended', selected_widget['text'])
        selected_widget = None


def finish():
    #found_eyetrackers = tr.find_all_eyetrackers()
    #found_eyetrackers[0].unsubscribe_from(tr.EYETRACKER_GAZE_DATA, check_gaze)
    root.destroy()


# Variables
selected_widget = None
selection_time = None
key_pressed = False

# Setup Tkinter
root = tk.Tk()
root.title("Gaze Typing")
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root, highlightthickness=0, bg=constant.COLOR_BACKGROUND)
canvas.pack(fill='both', expand='yes')

# Setup Input
font_keys = tk_font.Font(size=24)
font_input = tk_font.Font(size=20)

frame = tk.Frame(canvas, bg=constant.COLOR_BACKGROUND)
frame.pack(fill="none", expand=True)

text_label = tk.Label(frame, width=50, fg='white', bg=constant.COLOR_BACKGROUND, font=font_input)
text_label.pack(side='top', padx=(10, 0), pady=(15, 0))
text_entry = tk.Entry(frame, bg='white', justify='center', fg='black',
                      insertbackground='black',
                      font=font_input)
text_entry.pack(side='top', padx=(2, 0), pady=(0, 15))
text_entry.focus_set()

setup_log_files()
phrases = load_phrases()
load_new_phrase()
setup_keyboard()
#setup_eyetracker()

# Finish application after defined time
root.after(constant.TOTAL_TIME, finish)
root.mainloop()
