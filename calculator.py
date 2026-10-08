# the calculator logic

# ============================================================
# CONSTANTS
# ============================================================
DIGITS = "0123456789"
OPERATORS = ("÷", "×", "-", "+")


# ============================================================
# HELPERS
# ============================================================
def remove_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)


# ============================================================
# CALCULATOR
# ============================================================
class Calculator:
    def __init__(self):
        self.display = "0"        # what the screen shows
        self.first_number = "0"   # the number typed before the operator
        self.operator = None      # ÷ × - + once one has been pressed

    # ==== Public ====
    def press(self, value):
        """Handle one button press.

        Returns (expression, result) when the press finished a calculation,
        for example ("2 + 3", "5"). Returns None otherwise.
        """
        if self.display == "Error":
            if value in ("AC", "⌫", ".") or value in DIGITS:
                self._clear_operation()
                self.display = "0"
            else:
                return None

        if value == "=":
            return self._equals()
        elif value in OPERATORS:
            self._set_operator(value)
        elif value == "AC":
            self._clear_operation()
            self.display = "0"
        elif value == "%":
            self.display = remove_decimal(float(self.display) / 100)
        elif value == "⌫":
            self._backspace()
        elif value == "+/-":
            self.display = remove_decimal(float(self.display) * -1)
        elif value == ".":
            if "." not in self.display:
                self.display += "."
        elif value in DIGITS:
            if self.display == "0":
                self.display = value  # replace 0
            else:
                self.display += value  # append digit
        return None

    # ==== Private ====
    def _clear_operation(self):
        self.first_number = "0"
        self.operator = None

    def _equals(self):
        if self.operator is None:
            return None

        second_number = self.display
        num_a = float(self.first_number)
        num_b = float(second_number)
        expression = f"{self.first_number} {self.operator} {second_number}"

        try:
            if self.operator == "÷":
                result = remove_decimal(num_a / num_b)
            elif self.operator == "×":
                result = remove_decimal(num_a * num_b)
            elif self.operator == "-":
                result = remove_decimal(num_a - num_b)
            else:
                result = remove_decimal(num_a + num_b)
        except ZeroDivisionError:
            self.display = "Error"
            self._clear_operation()
            return None  # no history entry for an error

        self.display = result
        self._clear_operation()
        return expression, result

    def _set_operator(self, value):
        if self.operator is None:
            self.first_number = self.display
            self.display = "0"
        self.operator = value

    def _backspace(self):
        text = self.display
        if len(text) > 1 and not (len(text) == 2 and text[0] == "-"):
            self.display = text[:-1]
        else:
            self.display = "0"