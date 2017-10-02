import ev3control.master as master
from ev3control.messages import *

class Odometry():

      def __init__(self):
          self._dst_traveled = None
          self._angle_turned = None
          self._moved = None
          self._grasp = None

      def get_dst_traveled(self):
          return self._dst_traveled

      def set_dst_traveled(self,value):
          self._dst_traveled = value

      dst_traveled = property(get_dst_traveled,set_dst_traveled,'dst_traveled')


      def get_angle_turned(self):
          return self._angle_turned

      def set_angle_turned(self,value):
          self._angle_turned = value

      angle_turned = property(get_angle_turned,set_angle_turned,'angle_turned')


      def get_moved(self):
          return self._moved

      def set_moved(self,value):
          self._moved = value

      moved = property(get_moved,set_moved,'moved')

      def get_grasp(self):
          return self._grasp

      def set_grasp(self,value):
          self._grasp = value

      grasp = property(get_grasp,set_grasp,'grasp')


def addOdometryDevices(client,topic,qos):

    master.publish_cmd(client, topic,AddDeviceMessage('Odometer', "Odometry()"),1,qos=qos)

