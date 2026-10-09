import os
import tkinter
from datetime import datetime

from calculator import Calculator
from history import History, day_label

# ============================================================
# BUTTONS
# ============================================================
button_values = [
    ["⌫", "AC", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ".", "="]
]
# later add reverse number layout option

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["⌫", "AC", "%"]
bottom_symbols = ["+/-"]

row_count = len(button_values)
column_count = len(button_values[0])

# ============================================================
# KEYBOARD SUPPORT
# ============================================================
key_map = {
    "/": "÷",
    "*": "×",
    "-": "-",
    "+": "+",
    "=": "=",
    "%": "%",
    ".": ".",
}

# ============================================================
# COLOR SCHEME
# ============================================================
color_light_grey = "#d4d4d2"
color_black = "#1c1c1c"
color_dark_grey = "#505050"
color_blue = "#1e90ff"
color_white = "white"
# later add alt color scheme

# ============================================================
# WINDOW SETUP
# ============================================================
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)
# later let program remember last screen position before close

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, foreground=color_white, anchor="e", width=column_count)
# later reduce size of lable, if value exceeds screen size, reduce text size

label.grid(row=0, column=0, columnspan=column_count, sticky="we")

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
            width=column_count-1, height=1,
            command=lambda value=value: button_clicked(value))

        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_grey)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_blue)
        else:
            button.config(foreground=color_white, background=color_dark_grey)

        button.grid(row=row+1, column=column)

history_button = tkinter.Button(frame, text="History", font=("Arial", 18),
    foreground=color_white, background=color_dark_grey,
    command=lambda: open_history())
history_button.grid(row=row_count+1, column=0, columnspan=column_count, sticky="we")

frame.pack()

# ============================================================
# VARIABLES
# ============================================================
calc = Calculator()  # all the math and button logic lives in calculator.py

# history: past 7 days are saved (see history.py)
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
HISTORY_DAYS = 7
history = History(HISTORY_FILE, HISTORY_DAYS)

history_window = None
history_list = None
history_rows = []  # one item per listbox row: the entry, or None for day headers

# ============================================================
# FUNCTIONS
# ============================================================
# ==== Program logic ====
def button_clicked(value):
    finished = calc.press(value)
    label["text"] = calc.display
    if finished:
        history.add(*finished)  # (expression, result)

# ==== Key assign ====
def on_key(event):
    key = event.char
    keysym = event.keysym

    if key in "0123456789" and key != "":
        button_clicked(key)
    elif key in key_map:
        button_clicked(key_map[key])
    elif keysym in ("Return", "KP_Enter"):
        button_clicked("=")
    elif keysym == "BackSpace":
        button_clicked("⌫")
    elif keysym in ("Escape", "Delete"):
        button_clicked("AC")

window.bind("<Key>", on_key)

# ==== History window ====
def clear_history():
    history.clear()
    refresh_history_list()

def refresh_history_list():
    global history_rows
    history.prune()
    history_list.delete(0, tkinter.END)
    history_rows = []

    last_day = None
    for entry in reversed(history.entries):  # newest first
        stamp = datetime.fromisoformat(entry["time"])
        if stamp.date() != last_day:
            last_day = stamp.date()
            history_list.insert(tkinter.END, day_label(last_day))
            history_list.itemconfig(history_list.size() - 1, foreground=color_light_grey,
                selectforeground=color_light_grey, selectbackground=color_black)
            history_rows.append(None)
        history_list.insert(tkinter.END, f"{stamp:%H:%M}   {entry['expression']} = {entry['result']}")
        history_rows.append(entry)

    if not history_rows:
        history_list.insert(tkinter.END, "No calculations yet")
        history_rows.append(None)

def history_selected(event):
    selection = history_list.curselection()
    if not selection:
        return
    entry = history_rows[selection[0]]
    if entry is not None:
        calc.display = entry["result"]  # double-click recalls the result
        label["text"] = calc.display

def open_history():
    global history_window, history_list

    if history_window is not None and history_window.winfo_exists():
        history_window.lift()
        refresh_history_list()
        return

    history_window = tkinter.Toplevel(window)
    history_window.title("History (last 7 days)")
    history_window.resizable(False, False)

    history_list = tkinter.Listbox(history_window, font=("Arial", 14), width=34, height=15,
        background=color_black, foreground=color_white, selectbackground=color_blue,
        activestyle="none", borderwidth=0, highlightthickness=0)
    scrollbar = tkinter.Scrollbar(history_window, command=history_list.yview)
    history_list.config(yscrollcommand=scrollbar.set)
    history_list.bind("<Double-Button-1>", history_selected)

    clear_button = tkinter.Button(history_window, text="Clear history", font=("Arial", 14),
        foreground=color_black, background=color_light_grey, command=clear_history)

    history_list.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    clear_button.grid(row=1, column=0, columnspan=2, sticky="we")

    refresh_history_list()

window.mainloop()
