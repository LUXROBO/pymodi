import modi
import time


if __name__ == "__main__":
        
    print('Program Start')
    bundle = modi.MODI()
    button = bundle.buttons[0]
    gyro = bundle.gyros[0]
  
    while button.double_clicked() != True:
        print('dX, dY, Dz, aX aY aZ gX gY gZ', 
                gyro.pitch(),
                gyro.roll(),
                gyro.yaw(),
                gyro.acceleration_x(),
                gyro.acceleration_y(),
                gyro.acceleration_z(),
                gyro.angular_vel_x(),
                gyro.angular_vel_y(),
                gyro.angular_vel_z(),
                bundle._recv_q.qsize()
            )
        # time.sleep(0.1)
    print('Program End')