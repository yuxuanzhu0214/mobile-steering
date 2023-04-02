import vgamepad as vg
from mapping import *


def update_gamepad(button_inputs, gamepad):
    if button_inputs[DPAD_UP]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    if button_inputs[DPAD_DOWN]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        
    if button_inputs[DPAD_LEFT]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        
    if button_inputs[DPAD_RIGHT]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

    if button_inputs[START]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        
    if button_inputs[BACK]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    
    if button_inputs[LEFT_THUMB]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

    if button_inputs[RIGHT_THUMB]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

    if button_inputs[LEFT_SHOULDER]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

    if button_inputs[RIGHT_SHOULDER]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

    if button_inputs[GUIDE]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)

    if button_inputs[A]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    if button_inputs[B]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

    if button_inputs[X]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

    if button_inputs[Y]:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    

    gamepad.left_trigger_float(value_float=button_inputs[LEFT_TRIG])
    gamepad.right_trigger_float(value_float=button_inputs[RIGHT_TRIG])
    gamepad.left_joystick_float(x_value_float=button_inputs[LEFT_JOY_X], y_value_float=button_inputs[LEFT_JOY_Y])
    gamepad.right_joystick_float(x_value_float=button_inputs[RIGHT_JOY_X], y_value_float=button_inputs[RIGHT_JOY_Y])
    return gamepad


def update_button_test():
    gamepad = vg.VX360Gamepad()

    button_inputs = {
    # value of 0(not pressed) to 1(pressed)
    DPAD_UP: 0,
    DPAD_DOWN: 0,
    DPAD_LEFT: 0,
    DPAD_RIGHT: 0,
    START: 0,
    BACK: 0,
    LEFT_THUMB: 0,
    RIGHT_THUMB: 0,
    LEFT_SHOULDER: 0,
    RIGHT_SHOULDER: 0,
    GUIDE: 0,
    A: 0,
    B: 0,
    X: 0,
    Y: 0,
    # value between 0 to 255
    LEFT_TRIG: 0,
    RIGHT_TRIG: 0,
    # value between -32768 and 32767
    LEFT_JOY_X: 0,
    LEFT_JOY_Y: 0,
    RIGHT_JOY_X: 0,
    RIGHT_JOY_Y: 0
    }
    gamepad = update_gamepad(button_inputs, gamepad)
    gamepad.update()
    print("test complete")

        

