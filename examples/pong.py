import modi
import time

"""
Example script for simple pong game using dial and display module
Connect Network - Display - Dial
"""


def update_screen(pos, vel, bar):
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


def game():
    ball_pos = (20, 30)
    ball_vel = (1, -1)
    led.set_rgb(0, 50, 0)
    score = 0
    while True:
        bar_pos = int(50 * dial.get_degree() / 100)
        ball_pos, ball_vel = update_screen(ball_pos, ball_vel, bar_pos)
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


if __name__ == "__main__":
    bundle = modi.MODI(5)
    display = bundle.displays[0]
    dial = bundle.dials[0]
    button = bundle.buttons[0]
    led = bundle.leds[0]
    speaker = bundle.speakers[0]

    display.set_text("Press\nButton")

    while True:
        while True:
            if button.get_pressed():
                display.set_text("PONG!!")
                break
            time.sleep(0.02)
        time.sleep(1)
        point = game()
        time.sleep(3)
        display.set_text("Game Over\nScore: " + str(point))
        time.sleep(2)
        display.set_text("Press Button to restart")





