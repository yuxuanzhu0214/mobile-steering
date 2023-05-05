import RPi.GPIO as GPIO
import time


class Button_Matrix():
    def __init__(self, rows, cols):
        self.button_map = [0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0]
        self.rows = rows
        self.cols = cols
        GPIO.setmode(GPIO.BCM)
        for row in self.rows:
            GPIO.setup(row, GPIO.OUT, initial=GPIO.LOW)
        for col in self.cols:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def print_button_map(self):
        for r in range(len(self.rows)):
            for c in range(len(self.cols)):
                i = r * 4 + c
                print(self.button_map[i], end=" ")
            print()
        print()

    def press_button(self, button_index, debug=False):
        if self.button_map[button_index] == 0:
            self.button_map[button_index] = 1
            if debug:
                self.print_button_map()

    def release_button(self, button_index, debug=False):
        if self.button_map[button_index] == 1:
            self.button_map[button_index] = 0
            if debug:
                self.print_button_map()

    def scan_buttons(self):
        for r in range(len(self.rows)):
            GPIO.output(self.rows[r], GPIO.HIGH)
            for c in range(len(self.cols)):
                button_index = r * 6 + c
                if GPIO.input(self.cols[c]) == GPIO.HIGH:
                    self.press_button(button_index, debug=debug)
                if GPIO.input(self.cols[c]) == GPIO.LOW:
                    self.release_button(button_index, debug=debug)
            GPIO.output(self.rows[r], GPIO.LOW)


# button_map = [0, 0, 0, 0,
#               0, 0, 0, 0,
#               0, 0, 0, 0,
#               0, 0, 0, 0]

# pin_Row_1 = 23
# pin_Row_2 = 27
# pin_Row_3 = 22
# pin_Row_4 = 17
# rows = [pin_Row_1, pin_Row_2, pin_Row_3, pin_Row_4]

# pin_Col_1 = 12
# pin_Col_2 = 5
# pin_Col_3 = 6
# pin_Col_4 = 24
# cols = [pin_Col_1, pin_Col_2, pin_Col_3, pin_Col_4]

# GPIO.setmode(GPIO.BCM)
# for row in rows:
#     GPIO.setup(row, GPIO.OUT, initial=GPIO.LOW)
# # GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH) # Row 4
# # GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH) # Row 2
# # GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH) # Row 3
# # GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH) # Row 1
# for col in cols:
#     GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# # GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Col 4
# # GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Col 2
# # GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Col 3
# # GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Col 1




debug = True

pin_Row_1 = 23
pin_Row_2 = 27
rows = [pin_Row_1, pin_Row_2]

pin_Col_1 = 12
pin_Col_2 = 5
pin_Col_3 = 6
pin_Col_4 = 24
pin_Col_5 = 22
pin_Col_6 = 17
cols = [pin_Col_1, pin_Col_2, pin_Col_3, pin_Col_4, pin_Col_5, pin_Col_6]

# B = Button_Matrix(rows, cols)


