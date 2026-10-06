import tkinter

button_values = [
    ["AC", "√", "%", "÷"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ".", "="]
]

right_symbols = ["÷", "x", "-", "+", "="]
top_symbols = ["AC", "√", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

#color scheme
colo_light_grey = "#d4d4d2"
color_black = "#1c1c1c"
color_dark_grey = "#505050"
color_blue = "#1e90ff"
color_white = "white"

#window setup
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, foreground=color_white, anchor="e")

label.grid(row=0, column=0, columnspan=column_count, sticky="we")

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
            width=column_count-1, height=1,
            command=lambda value=value: button_clicked(value))
        button.grid(row=row+1, column=column)

frame.pack()

def button_clicked(value):
    pass

window.mainloop()