import modi
import time
import os
import sys


if __name__ == "__main__":

    print("Program Start")
    print("main.getpid():", os.getpid())
    bundle = modi.MODI()
    button = bundle.buttons[0]
    gyro = bundle.gyros[0]

    while button.double_clicked() != True:
        # for _ in range(10):
        # print('dX, dY, Dz, aX aY aZ gX gY gZ',
        #         gyro.pitch(),
        #         gyro.roll(),
        #         gyro.yaw(),
        #         gyro.acceleration_x(),
        #         gyro.acceleration_y(),
        #         gyro.acceleration_z(),
        #         gyro.angular_vel_x(),
        #         gyro.angular_vel_y(),
        #         gyro.angular_vel_z(),
        #         # bundle._recv_q.qsize()
        #     )
        pass
        # print('i am alive')
        # time.sleep(0.1)
    bundle.end()
    print("Program End")
    time.sleep(1)

