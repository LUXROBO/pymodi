import os

from textwrap import fill
from textwrap import dedent


class UsageInstructor:
    """
    Usage Instructor teaches basic module usage of PyMODI.
    It mainly teachs what methods are available for each module.
    """

    row_len = 79

    def __init__(self):
        self.bundle = None
        self.led = None
        self.button = None

    @staticmethod
    def clear():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        os.system(clear_cmd)

    def print_wrap(self, msg):
        message = fill(dedent(msg), self.row_len).lstrip()
        print(message)

    def print_topic(self, module_type):
        print('-' * self.row_len)
        topic = f"Usage Manual {module_type}"
        print(f"{topic:^{self.row_len}}")
        print('-' * self.row_len)

    def run_usage_manual(self):
        self.clear()
        print("=" * self.row_len)
        print(f"= {'Welcome to PyMODI Usage Manual':^{self.row_len - 4}} =")
        print("=" * self.row_len)

        selection = dedent(
            """
            Modules available for usage:
            1. Button
            2. Dial
            3. Env
            4. Gyro
            5. Ir
            6. Mic
            7. Ultrasonic
            8. Display
            9. Led
            10. Motor
            11. Speaker
            """
        )
        print(selection)
        module_nb = int(input(
            "Enter the module index (0 to exit) and press ENTER: "
        ))
        self.clear()

        if not (0 <= module_nb <= 11):
            print("ERROR: invalid module index")
            os._exit(0)

        run_selected_manual = {
            0: os._exit(0),
            1: self.run_button_manual,
            2: self.run_dial_manual,
            3: self.run_env_manual,
            4: self.run_gyro_manual,
            5: self.run_ir_manual,
            6: self.run_mic_manual,
            7: self.run_ultrasonic_manual,
            8: self.run_display_manual,
            9: self.run_led_manual,
            10: self.run_motor_manual,
            11: self.run_speaker_manual,
        }.get(module_nb)
        run_selected_manual()

    #
    # Usage manuals for each module
    #
    def run_button_manual(self):
        self.print_topic("Button")

        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            button = bundle.button[0]

            while True:
                if button.clicked:
                    print(f"Button({button.id}) is clicked!")
                if button.double_clicked:
                    print(f"Button({button.id}) is double clicked!")
                if button.pressed:
                    print(f"Button({button.id}) is pressed!")
                if button.toggled:
                    print(f"Button({button.id}) is toggled!")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_dial_manual(self):
        self.print_topic("Dial")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            dial = bundle.dials[0]

            while True:
                print(f"Dial ({dial.id}) degree: {dial.degree}")
                print(f"Dial ({dial.id}) turnspeed: {dial.turnspeed}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_env_manual(self):
        self.print_topic("Env")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            env = bundle.envs[0]

            while True:
                print(f"Env ({env.id}) temperature: {env.temperature}")
                print(f"Env ({env.id}) humidity: {env.humidity}")
                print(f"Env ({env.id}) brightness: {env.brightness}")
                print(f"Env ({env.id}) red: {env.red}")
                print(f"Env ({env.id}) green: {env.green}")
                print(f"Env ({env.id}) blue: {env.blue}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_gyro_manual(self):
        self.print_topic("Gyro")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            gyro = gy = bundle.gyros[0]

            while True:
                print(f"Gyro ({gy.id}) roll: {gy.roll}")
                print(f"Gyro ({gy.id}) pitch: {gy.pitch}")
                print(f"Gyro ({gy.id}) yaw: {gy.yaw}")
                print(f"Gyro ({gy.id}) angular_vel_x: {gy.angular_vel_x}")
                print(f"Gyro ({gy.id}) angular_vel_y: {gy.angular_vel_y}")
                print(f"Gyro ({gy.id}) angular_vel_z: {gy.angular_vel_z}")
                print(f"Gyro ({gy.id}) acceleration_x: {gy.acceleration_x}")
                print(f"Gyro ({gy.id}) acceleration_y: {gy.acceleration_y}")
                print(f"Gyro ({gy.id}) acceleration_z: {gy.acceleration_z}")
                print(f"Gyro ({gy.id}) vibration: {gy.vibration}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_ir_manual(self):
        self.print_topic("Ir")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            ir = bundle.irs[0]

            while True:
                print(f"Ir ({ir.id}) proximity: {ir.proximity}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_mic_manual(self):
        self.print_topic("Mic")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            mic = bundle.mics[0]

            while True:
                print(f"Mic ({mic.id}) volume: {mic.volume}")
                print(f"Mic ({mic.id}) frequency: {mic.frequency}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_ultrasonic_manual(self):
        self.print_topic("Ultrasonic")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            ultrasonic = us = bundle.ultrasonics[0]

            while True:
                print(f"Ultrasonic ({us.id}) distance: {us.distance}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_display_manual(self):
        self.print_topic("Display")
        print(dedent(
            """
            import modi

            bundle = modi.MODI()
            display = bundle.displays[0]

            # Set text to display, you can check the text being displayed
            display.text = "Hello World!"

            # Check what text has been displayed currently (in program)
            print(f"Display ({display.id}) text: {display.text})
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_led_manual(self):
        self.print_topic("Led")
        print(dedent(
            """
            import modi
            import time

            bundle = modi.MODI()
            led = bundle.leds[0]

            # Turn the led on for a second
            led.rgb = 255, 255, 255
            time.sleep(1)

            # Turn the led off for a second
            led.rgb = 0, 0, 0
            time.sleep(1)

            # Turn red on for a second
            led.rgb = 255, 0, 0
            time.sleep(1)

            led.rgb = 0, 0, 0

            # Turn green on for a second
            led.rgb = 0, 255, 0
            time.sleep(1)

            led.rgb = 0, 0, 0

            # Turn blue on for a second
            led.rgb = 0, 0, 255
            time.sleep(1)

            led.rgb = 0, 0, 0
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_motor_manual(self):
        self.print_topic("Motor")
        print(dedent(
            """
            import modi
            import time

            bundle = modi.MODI()
            motor = bundle.motors[0]

            motor.degree = 0, 0
            time.sleep(1)

            motor.degree = 10, 45
            time.sleep(1)

            first_degree, second_degree = motor.degree
            print(f"motor ({motor.id}) first degree: {first_degree}")
            print(f"motor ({motor.id}) second degree: {second_degree}")

            motor.speed = 20, 50
            time.sleep(1)

            first_speed, second_speed = motor.speed
            print(f"motor ({motor.id}) first speed: {first_speed}")
            print(f"motor ({motor.id}) second speed: {second_speed}")
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()

    def run_speaker_manual(self):
        self.print_topic("Speaker")
        print(dedent(
            """
            import modi
            import time

            bundle = modi.MODI()
            speaker = bundle.speakers[0]

            speaker.volume = 50
            time.sleep(1)

            speaker.frequency = 1000
            time.sleep(1)

            speaker.tune = 600, 1200
            time.sleep(1)
            """
        ))
        input("Press ENTER to exit: ")
        self.run_usage_manual()
