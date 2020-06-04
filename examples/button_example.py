import modi
import time

"""
Example script for the usage of button module
Make sure you connect 1 button module to your
network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    button = bundle.buttons[0]

    while True:
        if button.get_pressed():
            print("pressed       ", end='\r')
        else:
            print("not pressed   ", end='\r')
        if button.get_double_clicked():
            print("double clicked", end='\r')
            break
        time.sleep(0.02)



