import ev3control.master as master
from ev3control.messages import *


class VisualFeedback():

    def __init__(self):
        self._distance_angle = None,None
        self._class_name = None
        self._uuid = None

    def get_distance_angle(self):
        return self._distance_angle

    def set_distance_angle(self,value):
        self._distance_angle = value

    distance_angle = property(get_distance_angle,set_distance_angle,'distance_angle')


    def get_class_name(self):
        return self._class_name

    def set_class_name(self,value):
        self._class_name = value

    class_name = property(get_class_name,set_class_name,'class_name')

    """
    def get_uuid(self):
        return self._uuid

    def set_uuid(self,value):
        self._uuid = value

    uuid = property(get_uuid,set_uuid,'uuid')
    """

