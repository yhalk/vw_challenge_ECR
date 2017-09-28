import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3
import ctypes
import numpy as np
import sys
import cv2
from mpu6050.mpu6050 import MPU6050
import smbus
from odometry import Odometry

class Sensor(object):
    def __init__(self, *args, **kwargs):
        pass

    def read(self):
        raise ValueError('This function must be implemented by ')

class IMU2(Sensor):
    def __init__(self, bus='/dev/i2c-1', address=0x68):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.mpu = MPU6050(self.bus,self.address, 'IMU')

    def read(self):
        '''
            Reads the current values from the IMU using the mpu library
            Returns:
            tuple containing: pitch, roll, gyro x,y,z, accel x,y,z these values are scaled and NOT raw
        '''
        return self.mpu.read_all()

class IMU(Sensor):
    def __init__(self, path_to_shared_lib_mpu='/home/nvidia/jetson-robot/IOInterface/jetson/Sensors/mpu/libmpu.so', bus_filename='/dev/i2c-1', bus_adresses=[0x68, 0x69]):
        bus_filename = bus_filename.encode('ascii')
        self.libmpu = ctypes.cdll.LoadLibrary(path_to_shared_lib_mpu)

        self.file_descriptors = [self.libmpu.initIMU(bus_filename, bus_adress) for bus_adress in bus_adresses]
        self.data_c_arrays = [(ctypes.c_int16*7)() for _ in range(len(bus_adresses))]
        self.name = 'imu'
        self.data_sources = ["temperature", "acceleration", "gyro"]

    def read(self):
        data_dict = {}
        for idx, (file_descriptor, data_c_array) in enumerate(zip(self.file_descriptors, self.data_c_arrays)):
            self.libmpu.readIMU(file_descriptor, data_c_array)
            data_np_array = np.array(data_c_array)
            data_dict['temperature_{}'.format(idx)] = data_np_array[0] / 340.0 + 36.53
            data_dict['acceleration_{}'.format(idx)] = np.array([int(data_np_array[1]),
                                                                 int(data_np_array[2]),
                                                                 int(data_np_array[3]),
                                                                 ])
            data_dict['gyro_{}'.format(idx)] = np.array([int(data_np_array[4]),
                                                         int(data_np_array[5]),
                                                         int(data_np_array[6]),
                                                         ])
        return data_dict

    def read_sensor_nr(self, sensor_nr):
        # TODO: Ask Max, if the magic values for temperature conversion are correct.
        data_dict = {}
        self.libmpu.readIMU(self.file_descriptors[sensor_nr], self.data_c_arrays[sensor_nr])
        data_np_array = np.array(self.data_c_arrays[sensor_nr])
        data_dict['temperature'] = data_np_array[0] / 340.0 + 36.53
        data_dict['acceleration'] = np.array([int(data_np_array[1]), int(data_np_array[2]), int(data_np_array[3])])
        data_dict['gyro'] = np.array([int(data_np_array[4]), int(data_np_array[5]), int(data_np_array[6])])
        return data_dict

    def get_data_sources(self):
        return self.data_sources


class OnBoardCamera(Sensor):
    def __init__(self):
        self.name = 'onBoardCamera'
        self.cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)(1280), height=(int)(720),format=(string)I420, framerate=(fraction)2/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

    def read(self):
        if self.cap.isOpened():
            ret_val, frame = self.cap.read();
        else:
            raise ValueError('Camera not opened. Sorry this message is not really helpful, blame openCV :-) ')
        return {'onBoardCamera':frame}



#Create camera sensor object
camera = OnBoardCamera()

