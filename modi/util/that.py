import time
from typing import Tuple

from modi.module.module import Module


def update_screen(pos: Tuple[int, int],
                  vel: Tuple[int, int], bar: int,
                  display: Module) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Update the screen of the display module after moving the ball

    :param pos: Position of the ball
    :param vel: Velocity of the ball
    :param bar: Position of the bar
    :param display: Reference to display module
    :return: Tuple[Tuple[int, int], Tuple[int, int]]
    """
    display.set_variable(0, pos[0], pos[1])
    display.set_variable(1, bar, 60)
    pos = (pos[0] + vel[0], pos[1] + vel[1])
    if pos[0] < 0 or pos[0] > 40:
        vel = (-vel[0], vel[1])
    if pos[1] < 0 or pos[1] > 55:
        vel = (vel[0], -vel[1])
    if pos[1] < 0:
        pos = (pos[0], 0)
    if pos[0] < 0:
        pos = (0, pos[1])
    return pos, vel


def initialize(display: Module, led: Module, speaker: Module,
               dial: Module) -> int:
    """Initialize the movment of the ball

    :param display: Display module
    :param led:  Led module
    :param speaker: Speaker module
    :param dial: Dial module
    :return: Score
    """
    ball_pos = (20, 30)
    ball_vel = (1, -1)
    led.set_rgb(0, 50, 0)
    score = 0
    while True:
        bar_pos = int(50 * dial.get_degree() / 100)
        ball_pos, ball_vel = update_screen(ball_pos, ball_vel, bar_pos,
                                           display)
        time.sleep(0.02)
        if ball_pos[1] > 55 and (ball_pos[0] > bar_pos + 10
                                 or ball_pos[0] < bar_pos - 10):
            led.set_rgb(50, 0, 0)
            break
        elif ball_pos[1] > 55:
            speaker.set_tune(700, 100)
            time.sleep(0.1)
            speaker.set_volume(0)
            score += 1
        display.clear()
    return score


def check_complete(bundle):
    """Check the connected modules and initialize

    :param bundle: MODI object
    :return: None
    """
    module_names = [type(module).__name__ for module in bundle.modules]
    expected_names = ["Button", "Dial", "Led", "Speaker", "Display"]
    if len(module_names) != len(expected_names):
        return
    else:
        for name in expected_names:
            if name not in module_names:
                return

    display = bundle.displays[0]
    button = bundle.buttons[0]
    led = bundle.leds[0]
    dial = bundle.dials[0]
    speaker = bundle.speakers[0]
    
    button.get_pressed()
    time.sleep(0.1)
    if not button.get_pressed():
        return
    cmd = input("You have found an easter egg!\nContinue??(y/n)")
    if cmd.lower() != 'y':
        return
    display.set_text("Press\nButton")
    running = True
    while running:
        while True:
            if button.get_double_clicked():
                running = False
                display.clear()
                break
            elif button.get_clicked():
                display.set_text("PONG!!")
                break
            time.sleep(0.02)
        if not running:
            break
        time.sleep(1)
        point = initialize(display, led, speaker, dial)
        time.sleep(3)
        display.set_text("Score: {0}".format(point))
        time.sleep(2)
        display.set_text("Re: Click / No: Double Click")
