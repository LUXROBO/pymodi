import modi
import time


if __name__ == "__main__":
        
    print('Program Start')
    bundle = modi.MODI()
    # button1 = bundle.buttons[0]
    # button2 = bundle.buttons[1]
    gyro = bundle.gyros[0]
  
    while True:
        print('aX aY aZ gX gY gZ', 
               gyro.acceleration_x(),
               gyro.acceleration_y(),
               gyro.acceleration_z(),
               gyro.angular_vel_x(),
               gyro.angular_vel_y(),
               gyro.angular_vel_z(),
               bundle._recv_q.qsize()
            )
        # time.sleep(0.5)
        time.sleep(0.01)
    time.sleep(20)

    print('Program End')