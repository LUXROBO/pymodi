# import modi
import os


clear_cmd = 'clear'
if os.name == 'nt':
    clear_cmd = 'cls'


def clear():
    os.system(clear_cmd)


def check_response(answer: str):
    response = input(">>> ")
    while response != answer:
        print(f"Write below code precisely.\n>>> {answer}\n\nEnter below:")
        response = input(">>> ")


if __name__ == "__main__":
    clear()
    print("=" * 50)
    print(f"= {'Welcome to the PyMODI Tutor':^46} =")
    print("=" * 50)
    print("\nPyMODI is a very powerful tool that can control the\n"
          "MODI modules using python scripts. As long as you learn\n"
          "how to use built-in functions of PyMODI, you can easily\n"
          "control MODI modules. This interactive CUI tutorial will\n"
          "guide you through the marvelous world of PyMODI.\n")
    input("Press ENTER")
    clear()

    print('-' * 50)
    print(f"{'Lesson 1.1: Making MODI':^50}")
    print("First, you should import modi. Type\n"
          "import modi")

    check_response('import modi')

    clear()
