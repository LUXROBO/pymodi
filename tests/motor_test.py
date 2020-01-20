import modi
import time


def init_MR(bundle):
    print("modules list\n", bundle.modules)
    motor = bundle.motors[0]
    return len(bundle.modules), motor


bundle = modi.MODI()
time.sleep(1)
module_num, motor = init_MR(bundle)
time.sleep(1)
print("MODI Connected!")

for i in range(5):
    motor.speed(25, 0)
    time.sleep(0.7)
    motor.speed(0, 0)
    time.sleep(1)
    motor.speed(25, 0)
    time.sleep(0.5)
    motor.speed(0, 0)
    motor.speed(-25, 0)
    time.sleep(1.2)
    motor.speed(0, 0)
    time.sleep(1)
