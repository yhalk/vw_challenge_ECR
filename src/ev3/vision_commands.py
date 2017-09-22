import ev3control.master as master
import frcnn 
import cv2
from ev3control.messages import *


class VisualFeedback():

    def __init__(self):
        self._distance = None
        self._angle = None
        self._class_name = None

    def get_distance(self):
        return self._distance

    def set_distance(self,value):
        self._distance = value

    distance = property(get_distance,set_distance,'distance')

    
    def get_angle(self):
        return self._angle

    def set_angle(self,value):
        self._angle = value

    angle = property(get_angle,set_angle,'angle')

    def get_class_name(self):
        return self._class_name

    def set_class_name(self,value):
        self._class_name = value

    class_name = property(get_class_name,set_class_name,'class_name')


