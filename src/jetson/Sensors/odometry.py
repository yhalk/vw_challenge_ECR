class Odometry():

      def __init__(self):  
          self._dst_traveled = None
          self._angle_turned = None


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



