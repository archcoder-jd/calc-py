# calc-py

A desktop calculator built with Python and Tkinter. Click the buttons or use your keyboard, and look back at your calculations from the past 7 days.

## Features

- **Everyday calculations:** add, subtract, multiply and divide, plus percent (`%`), sign toggle (`+/-`), backspace (`⌫`) and clear (`AC`)
- **Keyboard support:** type numbers and operators directly, no mouse needed
- **History:** every completed calculation is saved and shown in a History window, grouped by day
  - Double-click an entry to bring its result back onto the display
  - Clear the list with one button
  - Entries older than 7 days are removed automatically
- **Error handling:** dividing by zero shows `Error` instead of crashing, and you can carry on with `AC`, `⌫` or by typing a new number
- **No dependencies:** uses only Python's standard library

## Getting started

### Requirements

- Python 3.7 or newer
- Tkinter, which comes with the standard Python installers for Windows and macOS. On some Linux distributions you may need to install it separately, for example `sudo apt install python3-tk`.

### Run it

```bash
git clone https://github.com/archcoder-jd/calc-py.git
cd calc-py
python main.py
```

On some systems the command is `python3` instead of `python`.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| `0`-`9`, `.` | Enter numbers |
| `+` `-` `*` `/` | Add, subtract, multiply, divide |
| `%` | Percent (divides the number on screen by 100) |
| `Enter` or `=` | Calculate |
| `Backspace` | Delete the last digit |
| `Esc` or `Delete` | Clear everything (`AC`) |

## History

Click the **History** button under the keypad to open the list of past calculations, newest first. Calculations are saved in a `history.json` file next to `main.py`. The file is created automatically, kept out of Git, and trimmed to the last 7 days each time the app saves or loads it.

## Project structure

```
calc-py/
├── main.py        # the whole app: interface, calculator logic, history
├── LICENSE
└── README.md
```

## Roadmap

Ideas I'm planning to add:

- Natural-language percentages, such as `46% of 200` and `46 of 200 =%`
- Reverse number layout option
- An alternative color scheme
- Remember the window position between sessions
- Shrink the display text when a number is too long to fit

## License

Released under the [MIT License](LICENSE).