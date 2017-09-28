from sensors_simple import IMU, IMU2
import numpy as np
import time

def main():
    #imu = IMU()
    #imu = IMU2(address = 0x68)
    imu2 = IMU2(address = 0x69)
    f = open('live_sensor_output.txt', 'w')
    #for i in range(100):
    previous_measurement = imu2.read()[5:]
    begin = 0
    while True:
        sensor_values = imu2.read()
        pitch = sensor_values[0]
        roll = sensor_values[1]
        gyro = sensor_values[2:5]
        accel = sensor_values[5:]
        #print('imu2 pitch ' + str(pitch))
        if np.power((previous_measurement[0] - accel[0]),2) > 1e-3:
            print(np.power((previous_measurement[0] - accel[0]),2))
            begin = time.time()
        elif begin != 0:
            end = time.time()
            print('moving time: ' + str(end - begin))
            begin = 0
        previous_measurement = accel
        print('imu2 accel '+str(accel))
        time.sleep(0.5)
        f.write(str(accel)+'\n')
        #print('imu2 gyro ' + str(gyro))

if __name__ == '__main__':
    main()
