class Odometry():

      def __init__(self):  
          self._dst_traveled_angle_turned = None,None
          self._moved = None
          self._grasp = None

      def get_dst_traveled_angle_turned(self):
          return self._dst_traveled_angle_turned

      def set_dst_traveled_angle_turned(self,value):
          self._dst_traveled_angle_turned = value

      dst_traveled_angle_turned = property(get_dst_traveled_angle_turned,set_dst_traveled_angle_turned,'dst_traveled_angle_turned')


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
