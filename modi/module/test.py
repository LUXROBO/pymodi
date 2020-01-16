import modi
import time

def init_MR(bundle):
  print('modules list\n', bundle.modules)
  motor = bundle.motors[0]
  return len(bundle.modules), motor

bundle = modi.MODI()
time.sleep(1)
module_num, motor = init_MR(bundle)
time.sleep(1)
print('MODI Connected!')

motor.speed(50,-50)
time.sleep(3)
motor.speed(0,0)