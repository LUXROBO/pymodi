import os
from textwrap import fill
import time
import cv2

clear_cmd = 'clear'
if os.name == 'nt':
    clear_cmd = 'cls'

row = 70


def clear():
    os.system(clear_cmd)


def printr(msg: str):
    message = fill(msg, row)
    print(message)


def print_lesson(lesson, title):
    print('-' * row)
    topic = f"Lesson {lesson}: {title}"
    print(f"{topic:^{row}}")
    print('-' * row)


def check_response(answer: str, give_answer: bool = True, guide: str = ">>> "):
    response = input(guide)
    nb_wrong = 1
    while response != answer:
        if give_answer:
            print(f"Write below code precisely.\n>>> {answer}\n")
        elif nb_wrong > 2:
            warning = cv2.resize(cv2.imread('./soon.png'), (300, 500))
            cv2.imshow('You still don\'t get it?', warning)
            cv2.waitKey()
            cv2.destroyAllWindows()
            print(f"The answer is {answer}. Type it below.")
        else:
            print("Try again!")
        response = input(guide)
        nb_wrong += 1
    return response


class Tutor:

    @staticmethod
    def run_lesson1():
        print_lesson(1, "Making MODI")
        printr('First, you should import modi. Type import modi')

        check_response('import modi')
        import modi
        printr("Great! Now you can use all the features of modi\n")
        printr("To control the modules, make a MODI object that contains"
               " all the connected modules. Once you create it, it will "
               "automatically find all the modules connected. When creating "
               "the MODI object, you should specify the number of modules "
               "currently connected to the network module.\n")
        input("\nPress ENTER")
        clear()
        printr("\nNow, prepare real MODI modules. Connect a network module "
               "to your device. Then, connect a Button module "
               "and an Led module.\nSince you have 2 module connected to the "
               "network module, make a MODI object by typing "
               "bundle = modi.MODI(2)")

        check_response('bundle = modi.MODI(2)')
        bundle = modi.MODI(2)
        print()
        printr('Great! The "bundle" is your MODI object. With it, you can '
               'control all the modules connected to your device.')
        input("\nYou have completed this lesson.\nPress ENTER")
        return bundle

    @staticmethod
    def run_lesson2(bundle):
        # Lesson 2
        clear()
        print_lesson(2, "Accessing modules")
        printr("In the previous lesson, you created a MODI object. Let's "
               "figure out how we can access modules connected to it.")
        printr('"bundle.modules" is a method to get all the modules connected '
               'to the device. Type: bundle.modules')
        check_response('bundle.modules')
        print(bundle.modules)
        print()
        printr("\nYou can see two modules connected to the device. "
               "You can access each module by the same method we use "
               "with an array.")
        printr("\nYou can also access modules by types. "
               "Type: bundle.leds")

        check_response('bundle.leds')
        print(bundle.leds)
        print()
        printr('\nThere is one led module connected. Make an led variable by'
               ' accessing the first led module. Type: led = bundle.leds[0]')

        check_response('led = bundle.leds[0]')
        led = bundle.leds[0]
        print()
        printr("Super! You can now do whatever you want with these modules."
               " If you have different modules connected, you can access "
               "the modules in a same way, just typing bundle.<module_name>s")

        input("\nYou have completed this lesson.\nPress ENTER")
        return bundle, led

    @staticmethod
    def run_lesson3(bundle, led):
        clear()
        print_lesson(3, "Controlling modules")
        printr("Now you know how to access individual modules. \n"
               "Let's make an object named \"button\" as well for your button "
               "module. You know how to do it.")

        check_response('button = bundle.buttons[0]', False)
        button = bundle.buttons[0]
        print()

        printr("Perfect. With your button module and led module, we can either"
               " get data from the module or send command to the module")

        printr('get_pressed is a method of a button module which returns'
               ' whether the button is pressed or note.'
               '\nCheck the state of button by typing'
               ' button.get_pressed()')

        check_response('button.get_pressed()')
        print(button.get_pressed())
        print()

        printr("Now see if the same command returns True when "
               "pressing the button.")

        check_response('button.get_pressed()')
        print(button.get_pressed())
        print()

        printr("Good. Now, let's send a command to the led.\n"
               "set_rgb() is a method of an led module. Let there be light "
               "by typing led.set_rgb(0, 0, 255)")

        response = check_response('led.set_rgb(0, 0, 255)')
        exec(response)
        print()

        printr("Perfect! You will see the blue light from the led module.")

        input("\nYou have completed this lesson.\nPress ENTER")
        return bundle, led, button

    @staticmethod
    def run_lesson4(bundle, led, button):
        clear()
        print_lesson(4, "Your First PyMODI Project")
        printr("Let's make a project that blinks led when button is pressed.")
        printr("In an infinite loop, we want our led to light up when button "
               "is pressed, and turn off when not pressed. Complete the "
               "following code based on the description.")

        input("\nPress ENTER when you're ready!")
        clear()
        print(">>> while True:")
        print("...     # Check if button is pressed")
        check_response('button.get_pressed():', give_answer=False,
                       guide="...     if ")
        print("...         # Set Led color to green")
        check_response('led.set_rgb(0, 255, 0)', give_answer=False,
                       guide="...         ")
        print("...     elif button.get_double_clicked():")
        print("...         break")
        print("...     else:")
        print("...         # Turn off the led. i.e. set color to (0, 0, 0)")
        check_response('led.set_rgb(0, 0, 0)', give_answer=False,
                       guide="...         ")

        printr("Congrats!! Now let's see if the code works as we want.\n"
               "Press the button to light up the led. Double click the button "
               "to break out of the loop")

        while True:
            if button.get_pressed():
                led.set_rgb(0, 255, 0)
            elif button.get_double_clicked():
                break
            else:
                led.set_off()
            time.sleep(0.02)

        printr("\nIt looks great! "
               "Now you know how to use PyMODI to control modules."
               "\nYou can look up more functions at "
               "pymodi.readthedocs.io/en/latest\n"
               )

        input("\nYou have completed the tutorial.\nPress ENTER to exit")
        bundle._com_proc.terminate()

    def start(self):
        # Intro
        clear()
        print("=" * row)
        print(f"= {'Welcome to the PyMODI Tutor':^{row - 4}} =")
        print("=" * row)
        printr("\nPyMODI is a very powerful tool that can control the "
               "MODI modules using python scripts. As long as you learn "
               "how to use built-in functions of PyMODI, you can easily "
               "control MODI modules. This interactive CUI tutorial will "
               "guide you through the marvelous world of PyMODI.")

        print("Tutorial includes:\n"
              "1. Making MODI\n"
              "2. Accessing Modules\n"
              "3. Controlling Modules\n"
              "4. Your First PyMODI Project")

        lesson_nb = int(input("\nEnter the lesson number and press ENTER: "))
        clear()

        if lesson_nb > 1:
            import modi
            print("Preparing the MODI module...")
            input(
                "Connect buttton and led module to your device and press "
                "ENTER")
            bundle = modi.MODI(2)

        if lesson_nb > 2:
            led = bundle.leds[0]
            button = bundle.buttons[0]

        if lesson_nb <= 1:
            bundle = self.run_lesson1()
        if lesson_nb <= 2:
            bundle, led = self.run_lesson2(bundle)
        if lesson_nb <= 3:
            bundle, led, button = self.run_lesson3(bundle, led)
        if lesson_nb <= 4:
            self.run_lesson4(bundle, led, button)
