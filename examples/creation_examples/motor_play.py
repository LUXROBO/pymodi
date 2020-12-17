import modi
import keyboard


if __name__ == '__main__':
    bundle = modi.MODI(
        conn_type='ble',
        network_uuid="YOUR_NETWORK_MODULE_UUID"
    )
    motor = bundle.motors[0]
    network = bundle.networks[0]

    while True:
        if keyboard.is_pressed('down'):
            motor.speed = 100, -100
        elif keyboard.is_pressed('up'):
            motor.speed = -100, 100
        elif keyboard.is_pressed('left'):
            motor.speed = 100, 100
        elif keyboard.is_pressed('right'):
            motor.speed = -100, -100
        else:
            motor.speed = 0, 0
