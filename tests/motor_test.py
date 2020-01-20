import modi
import time


bundle = modi.MODI()
print("MODI Connected!")
motor = bundle.motors[0]

# Channel 0, 1 -> Top/Bottom
# Mode 0, 1, 2 -> Torque, Speed, Position / 현재 Torque 구현되어있지 않음
for i in range(5):
    # 0번 top motor의 스피드를 100으로 고정할때
    motor.motor_ch_ctrl(0, 1, 100)

    # 1번 bot motor의 스피드를 50으로 고정할때
    motor.motor_ch_ctrl(0, 1, 50)

    # 0번 top motor의 앵글을

    time.sleep(0.7)
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
