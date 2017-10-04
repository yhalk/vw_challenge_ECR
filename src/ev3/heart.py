#! /usr/bin/env python3

from functools import partial
import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
from Sensors.sensors import publishable_names_dict, items_to_publish, addSensorDevices
import time
import ev3control.master as master
import ev3control.slave as slave
from ev3control.messages import *
from IR.ir_to_control_ev3 import IR_controller
import datetime
from communication import comm_init, get_behaviours_and_params, publish_all
from threading import Thread
from MotionCtrl import simple_behaviors
from MotionCtrl import low_level_ctrl as ctrl
import os.path
import os


#Subscribe to topics for listening and publishing
client,listening = comm_init(topics_to_listen=config.topics_to_listen, qos_listen=config.qos_listen, topics_to_publish=config.topics_to_publish, qos_pub=config.qos_pub, listening={}, log=0)


def get_vision_attr(listening):

    distance_angle = getattr(listening["Vision"], "distance_angle")
    #print("DISTANCE_ANGLE" +str(distance_angle))
    if (type(distance_angle).__name__=='str'):
       d = distance_angle.strip('(')
       d2 = d.strip(')')
       r = d2.split(',')
       angle = r[1]
       distance = r[0]
    else:
       angle = None
       distance = None
    class_name = getattr(listening["Vision"], "class_name")
    #print("CLASS " +str(class_name))

    return distance, angle, class_name    


def set_odometry_attr(dst,angle,grasp):
    odometer = publishable_names_dict["Odometer"]
    setattr(odometer,"dst_traveled_angle_turned",(dst,angle))
    setattr(odometer,"grasp",grasp)
    if (dst==None and angle==None):
       setattr(odometer,"moved",0)
    elif (abs(dst-0.0)>=-0.00000001):
       setattr(odometer,"moved",1)
       print("set moved")


counter = 0
while(1):
   if os.path.isfile('vision/vision_flag'):
      #stop the motors here and wait for messages
      print("break")
      ctrl.stop_actuator(stop_action='hold')
      os.remove('vision/vision_flag')
   else:
      print("not seen")

   print("EV3 work in progress..."+str(counter))
   kill = IR_controller()
   if kill:
      break
   print(listening)
   client.loop()
   if ("Vision" in list(listening.keys())):
      distance, angle, class_name = get_vision_attr(listening)   
      print(distance, angle, class_name)
      if (distance!=None and angle!=None):
         if "box" in class_name:
             dst_traveled,angle_turned,grasp = simple_behaviors.move_to_box_and_release(float(distance), float(angle))
         elif "object" in class_name:
             dst_traveled,angle_turned,grasp = simple_behaviors.move_and_grasp_object(float(distance), float(angle))
         else:
             dst_traveled,angle_turned,grasp = simple_behaviors.move_to(float(distance), float(angle))
             
         set_odometry_attr(dst_traveled,angle_turned,grasp)

   publish_all(client,config.topics_to_publish)   
   counter = counter + 1
   time.sleep(1)
   
client.disconnect()

