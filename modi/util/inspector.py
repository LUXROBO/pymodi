import os
import time

from textwrap import fill
from textwrap import dedent


class Inspector:
    """
    Inspector diagnoses malfunctioning STM32 modules (all modules but network)
    """

    row_len = 79

    def __init__(self):
        self.bundle = None

    @staticmethod
    def clear():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        os.system(clear_cmd)

    def print_wrap(self, msg):
        message = fill(dedent(msg), self.row_len).lstrip()
        print(message)

    def print_module_page(self, module, i, nb_modules):
        print('-' * self.row_len)
        module_to_inspect = f"| Diagnosing {module.module_type} ({module.id})"
        progress = f"({i+1} / {nb_modules}) |"
        s = f"{module_to_inspect:<{self.row_len}}"
        s = progress.join(s.rsplit(' '*len(progress), 1))
        print(s)
        print('-' * self.row_len)

    def inspect(self, module, i, nb_modules):
        self.print_module_page(module, i, nb_modules)

        inspect_module = {
            # inspection method for input modules
            "button": self.inspect_button,
            "dial": self.inspect_dial,
            "env": self.inspect_env,
            "gyro": self.inspect_gyro,
            "ir": self.inspect_ir,
            "mic": self.inspect_mic,
            "ultrasound": self.inspect_ultrasound,

            # inspection method for input modules
            "display": self.inspect_display,
            "led": self.inspect_led,
            "motor": self.inspect_motor,
            "speaker": self.inspect_speaker,
        }.get(module.module_type)
        inspect_module(module, i, nb_modules)

        self.clear()

    def inspect_button(self, button):
        pass

    def inspect_dial(self, dial):
        pass

    def inspect_env(self, env):
        pass

    def inspect_gyro(self, gyro):
        pass

    def inspect_ir(self, ir):
        pass

    def inspect_mic(self, mic):
        pass

    def inspect_ultrasound(self, ultrasound):
        pass

    def inspect_display(self, display):
        pass

    def inspect_led(self, led, i, nb_modules):
        self.print_wrap(
            """
            LED module has red, green and blue as its property. We will inspect
            these properties each.
            """
        )
        input("\nPress ENTER to continue: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect RED, We have set LED's RED to its maximum intensity.
            """
        )
        led.rgb = 255, 0, 0
        input("\nIf you see strong red from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect GREEN, We have set LED's GREEN to its maximum intensity.
            """
        )
        led.rgb = 0, 255, 0
        input("\nIf you see strong green from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect BLUE, We have set LED's BLUE to its maximum intensity.
            """
        )
        led.rgb = 0, 0, 255
        input("\nIf you see strong blue from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        input(dedent(
            f"""
            It looks like the LED module ({led.id}) is properly functioning!
            To inspect next module, press ENTER to continue:
            """
        ))

    def inspect_motor(self, motor, i, nb_modules):
        self.print_wrap(
            """
            Motor module has degree (i.e. position), speed and torque as its
            property. We will inspect position property of the module.
            """
        )
        print()
        self.print_wrap(
            """
            Before continuing, we have set motors' initial position to zero
            (your motor module may have moved a bit), so be clam :)
            """
        )
        input("\nPress ENTER to continue: ")
        self.clear()
        motor.degree = 0, 0

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            """
            Firstly, in order to inspect position property, we have rotated 360
            degree of the first motor.
            """
        )
        motor.first_degree = 100
        time.sleep(1.5)
        input("\nIf the first motor has rotated 360 degrees, press ENTER: ")
        print()
        self.print_wrap(
            """
            Secondly, in order to inspect position property, we have rotated
            360 degree of the second motor.
            """
        )
        motor.second_degree = 100
        time.sleep(1.5)
        input("\nIf the second motor has rotated 360 degrees, press ENTER: ")
        self.clear()

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            f"""
            It looks like the motor module ({motor.id}) is properly
            functioning!
            """
        )
        input("\nTo inspect next module, press ENTER to continue: ")

    def inspect_speaker(self, speaker, i, nb_modules):
        self.print_wrap(
            """
            Speaker module has tune as its property, tune is composed of
            frequency and volume. Thus inspecting the tune property consists of
            inspecting frequency and volume properties.
            """
        )
        self.clear()

        self.print_module_page(speaker, i, nb_modules)
        self.print_wrap(
            """
            To inspect tune property, we have set frequency of 880 and volume
            of 50.
            """
        )
        speaker.tune = 880, 50
        input(dedent(
            "\nPress ENTER if you hear a gentle sound from the speaker module!"
        ))
        speaker.tune = 880, 0
        self.clear()

    #
    # Main methods are defined below
    #
    def run_inspection(self):
        self.clear()
        print("=" * self.row_len)
        print(f"= {'This is PyMODI Module Inspector':^{self.row_len - 4}} =")
        print("=" * self.row_len)

        self.print_wrap(
            """
            PyMODI provides a number of tools that can be utilized in different
            purpose. One of them is the STM32 module (all modules but network)
            inspector which diagnoses any malfunctioning MODI module.
            """
        )

        nb_modules = int(input(dedent(
            """
            Connect network module to your local machine, attach other modi
            modules to the network module. When attaching modi modules, make
            sure that you provide sufficient power to the modules. Using modi
            battery module is a good way of supplying the power to the modules.

            Type the number of modi modules (integer value) that are connected
            to the network module (note that the maximum number of modules is
            20) and press ENTER:
            """.rstrip() + " "
        )))
        self.clear()

        if not (1 <= nb_modules <= 20):
            print(f"ERROR: {nb_modules} is invalid for the number of modules")
            os._exit(0)

        print("Importing modi package and creating a modi bundle object...\n")
        import modi
        self.bundle = modi.MODI()

        stm32_modules = \
            [m for m in self.bundle.modules if m.module_type != "Network"]
        nb_modules_detected = len(stm32_modules)
        if nb_modules != nb_modules_detected:
            self.print_wrap(
                f"""
                You said that you have attached {nb_modules} modules but PyMODI
                detects only {nb_modules_detected} number of modules! Look at
                the printed log above regarding module connection and check
                which modules have not been printed above.
                """
            )
            os._exit(0)

        input(dedent(
            """
            It looks like all stm modules have been initialized properly! Let's
            diagnose each module, one by one!

            Press ENTER to continue:
            """.rstrip() + " "
        ))
        self.clear()

        # Let's inspect each stm module!
        for i, module in enumerate(stm32_modules):
            self.inspect(module, i, nb_modules)
