import modi
import time

from random import randint


"""
PyMODI implementation of random crocodile at, 
https://www.youtube.com/
watch?v=wAaL0S4GKjA&list=PLXpISlr9BpDupLigOm20FgyzuI4gION44&index=6&t=75s
"""
if __name__ == '__main__':
    bundle = modi.MODI()
    button = bundle.buttons[0]
    motor = bundle.motors[0]
    print('Starting rand_croc creation!')

    motor.set_degree(50, 50)
    while True:
        time.sleep(0.1)

        motor.set_degree(50, 50)

        if button.get_clicked():
            rand_res = randint(1, 2)
            print(f'rand_res: {rand_res}')
            if rand_res == 1:
                motor.set_degree(40, 60)
                time.sleep(1)
            else:
                motor.set_degree(60, 40)
                time.sleep(1)

        if button.get_double_clicked():
            print('Finishing rand_croc creation..')
            break
