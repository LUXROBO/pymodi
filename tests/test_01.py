import modi
import time


if __name__ == "__main__":

    print("Program Start")
    bundle = modi.MODI()

    # lcd = bundle.displays[0]
    # lcd.text("hi")
    # time.sleep(1)
    # lcd.variable(10.15, 0, 0)
    # time.sleep(5)
    # speaker = bundle.speakers[0]
    # led = bundle.leds[0]
    # ultra = bundle.ultrasonics[0]
    # mic = bundle.mics[0]
    # ir = bundle.irs[0]
    # env = bundle.envs[0]
    # dial = bundle.dials[0]
    button = bundle.buttons[0]
    gyro = bundle.gyros[0]
    # motor = bundle.motors[0]
    print(
        "dX, dY, Dz, aX aY aZ gX gY gZ",
        gyro.pitch(),
        gyro.roll(),
        gyro.yaw(),
        gyro.acceleration_x(),
        gyro.acceleration_y(),
        gyro.acceleration_z(),
        gyro.angular_vel_x(),
        gyro.angular_vel_y(),
        gyro.angular_vel_z(),
        button.pressed(),
        bundle._serial_read_q.qsize(),
    )
    while button.double_clicked() != True:
        # for i in range(0, 100, 2):
        # speaker.tune(i * 10, 30)
        # led.rgb(i, 100 - i, i)
        # print("Ultrasonic,", ultra.distance())
        # print("MIC Volume", mic.volume())
        # print("IR proximity", ir.distance())
        # print(
        #     "dX, dY, Dz, aX aY aZ gX gY gZ",
        #     gyro.pitch(),
        #     gyro.roll(),
        #     gyro.yaw(),
        #     gyro.acceleration_x(),
        #     gyro.acceleration_y(),
        #     gyro.acceleration_z(),
        #     gyro.angular_vel_x(),
        #     gyro.angular_vel_y(),
        #     gyro.angular_vel_z(),
        #     button.pressed(),
        #     bundle._serial_read_q.qsize(),
        # )
        # print(
        #     "temp, humidity, brightness, red, green, blue",
        #     env.temperature(),
        #     env.humidity(),
        #     env.brightness(),
        #     env.red(),
        #     env.green(),
        #     env.blue(),
        # )
        time.sleep(0.01)
    # motor.speed(0.0, 0.0)
    time.sleep(0.1)
    bundle.exit()
    print("Program End")
