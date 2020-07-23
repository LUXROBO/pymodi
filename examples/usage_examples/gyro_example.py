import modi

"""
Example script for the usage of gyro module
Make sure you connect 1 gyro module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    gyro = bundle.gyros[0]

    while True:
        print(f"Pitch: {gyro.pitch:<10}"
              f"Roll: {gyro.roll:<10}"
              f"Yaw: {gyro.yaw:<10}"
              f"Vel x: {gyro.angular_vel_x:<10}"
              f"Vel y: {gyro.angular_vel_y:<10}"
              f"Vel z: {gyro.angular_vel_z:<10}"
              f"Acc x: {gyro.acceleration_x:<10}"
              f"Acc y: {gyro.acceleration_y:<10}"
              f"Acc z: {gyro.acceleration_z:<10}", end='\r')
