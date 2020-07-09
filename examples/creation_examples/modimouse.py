import modi
import mouse

if __name__ == "__main__":
    bundle = modi.MODI()
    gyro, button = bundle.gyros[0], bundle.buttons[0]
    speed = 5
    while True:
        if button.double_clicked:
            break
        if button.clicked:
            mouse.click()
        x, y = -gyro.angular_vel_z, -gyro.angular_vel_x
        mouse.move(speed * x, speed * y, absolute=False, duration=0.1)
