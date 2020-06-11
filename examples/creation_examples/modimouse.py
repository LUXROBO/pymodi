import modi
import mouse

if __name__ == "__main__":
    bundle = modi.MODI(2)
    gyro, button = bundle.gyros[0], bundle.buttons[0]
    speed = 5
    while True:
        if button.get_double_clicked():
            break
        if button.get_clicked():
            mouse.click()
        x, y = -gyro.get_angular_vel_z(), -gyro.get_angular_vel_x()
        mouse.move(speed * x, speed * y, absolute=False, duration=0.1)
