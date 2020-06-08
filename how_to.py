# import modi
import os
from textwrap import fill

clear_cmd = 'clear'
if os.name == 'nt':
    clear_cmd = 'cls'

row = 70


def clear():
    os.system(clear_cmd)


def printr(msg: str):
    message = fill(msg, row)
    print(message)


def check_response(answer: str):
    response = input(">>> ")
    while response != answer:
        print(f"Write below code precisely.\n>>> {answer}\n\nEnter below:")
        response = input(">>> ")


if __name__ == "__main__":
    clear()
    print("=" * row)
    print(f"= {'Welcome to the PyMODI Tutor':^{row - 4}} =")
    print("=" * row)
    printr("\nPyMODI is a very powerful tool that can control the "
           "MODI modules using python scripts. As long as you learn "
           "how to use built-in functions of PyMODI, you can easily "
           "control MODI modules. This interactive CUI tutorial will "
           "guide you through the marvelous world of PyMODI.")
    input("\nPress ENTER")
    clear()

    print('-' * 50)
    print(f"{'Lesson 1.1: Making MODI':^50}")
    print("First, you should import modi. Type\n"
          "import modi")

    check_response('import modi')

    clear()
