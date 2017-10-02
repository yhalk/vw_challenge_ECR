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

#Subscribe to topics for listening and publishing
client,listening = comm_init(topics_to_listen=config.topics_to_listen, qos_listen=config.qos_listen, topics_to_publish=config.topics_to_publish, qos_pub=config.qos_pub, listening={}, log=0)


def get_vision_attr(listening):

    distance = getattr(listening["Vision"], "distance")
    #print("DISTANCE " +str(distance))
    angle = getattr(listening["Vision"], "angle")
    #print("ANGLE " +str(angle))
    class_name = getattr(listening["Vision"], "class_name")
    #print("CLASS " +str(class_name))

    return distance, angle, class_name    


def set_odometry_attr(dst,angle,grasp):
    odometer = publishable_names_dict["Odometer"]
    setattr(odometer,"dst_traveled",dst)
    setattr(odometer,"angle_turned",angle)
    setattr(odometer,"grasp",grasp)
    if (dst==None and angle==None):
       setattr(odometer,"moved",0)
    elif (abs(dst-0.0)>=-0.00000001):
       setattr(odometer,"moved",1)
       print("set moved")


counter = 0
while(1):
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



"""

channel_prev = -1
cmd_prev = -1
#If IR return list is != [0,0,0,0]
valid = 0
#Values to transmit for data collection
a,b,grip,lift,timestamp = -1,-1,-1,-1,-1



was in loop:



#Read IR controller input
   (channel,cmd,valid) = get_IR_cmd(sensors_names_dict["IR_control"])
   if (int(channel)!=2):
      if (int(channel)!=3 and int(channel)!=-1):
         a,b,lift,grip = ir_ctrl.ir_to_control(actuators_l,int(channel),int(cmd))
         timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
         data_collector.set_data(a,b,lift,grip,timestamp)
         print("ffff "+repr(getattr(data_collector,'data')))
      else:
          print("ch3")
          _,_,_,_ = ir_ctrl.ir_to_control(actuators_l,int(channel),int(cmd))
   

   time.sleep(1)
   #Publish sensor readings  --- CHECK QUALITY OF SERVICE LEVEL FOR SENSOR VALUES
   for sensor, property_names in items_to_publish.items():
        for property_name in property_names:
           if ((sensor=="IR_control") and (property_name=="cmd" or property_name=="channel") and (valid==1) and int(cmd)==9 and int(channel)==2):  #publish only for data collection atm
              master.publish_cmd(client,topic,SetAttrMessage(sensor, property_name, str(cmd)))
              master.publish_cmd(client,topic,SetAttrMessage(sensor, property_name, str(channel)))
              print(repr(getattr(data_collector,'data')))
              master.publish_cmd(client,topic_data,SetAttrMessage("data_collector","data",repr(data_collector.get_data())))
           else:
              pass
    
   #Get and set actuator properties
   client.loop_read()   

"""
