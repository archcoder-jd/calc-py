import tkinter

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

# color scheme
colo_light_grey = "#d4d4d2"
color_black = "#1c1c1c"
color_dark_grey = "#505050"
color_blue = "#1e90ff"
color_white = "white"
# later add alt color scheme

# window setup
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
            button.config(foreground=color_black, background=colo_light_grey)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_blue)
        else:
            button.config(foreground=color_white, background=color_dark_grey)

        button.grid(row=row+1, column=column)

frame.pack()

#A+B A-B, A*B, A/B
A = "0"
operator = None
B = None

def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None

def remove_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols, top_symbols, bottom_symbols, label, A, B, operator

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "÷":
                    label["text"] = remove_decimal(numA / numB)
                elif operator == "×":
                    label["text"] = remove_decimal(numA * numB)
                elif operator == "-":
                    label["text"] = remove_decimal(numA - numB)
                elif operator == "+":
                    label["text"] = remove_decimal(numA + numB)

                clear_all()
                
        elif value in "÷×-+":
            if operator is None:
                A = label["text"]
                label["text"] ="0"
                B = "0"

            operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_decimal(result)
        elif value == "⌫":
            text = label["text"]
            if len(text) > 1 and not (len(text) == 2 and text[0]) == "-":
                label["text"] = text[:-1]
            else:
                label["text"] = "0"

    elif value in bottom_symbols:
        if value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_decimal(result)
            
    else: #
        if value == ".":
            if value not in label["text"]:
                label["text"] += value # append digit
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value # replace 0
            else:
                label["text"] += value # append digit

    # keyboard support
    key_map = {
        "/": "÷",
        "*": "×",
        "-": "-",
        "+": "+",
        "=": "=",
        "%": "%",
        ".": ".",
    }

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

window.mainloop()