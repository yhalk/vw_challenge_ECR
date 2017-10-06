#! /usr/bin/env python3
import os
import cv2
import csv
import time
import config
import ev3control.slave as slave
import IR.IR_control as remoteControl 
import Sensors.sensors_simple as sensors  
import Vision.frcnn_clustering as frcnn
import datetime 
from Vision.vision_commands import *
from communication import comm_init,get_behaviours_and_params
from behaviours.box_detection.detect_box import detect_box
from behaviours.timing import timing
from behaviours.explore.explore import explore
from hello_world import *
from behaviours.debug import debug
from behaviours.object_detection.detect_object import detect_object
from init_state_machine import run_state_machine

#Subscirbe to topics for listening and publishing
client,listening = comm_init(topics_to_listen=config.topics_to_listen, qos_listen=config.qos_listen, topics_to_publish=config.topics_to_publish ,qos_pub=config.qos_pub, listening={}, log=0)

client.loop_start()
#Create object detector
predictor = frcnn.ObjectPredictor()

print("Client is set up, will start listening now!")

DST_EXPLORE = 0
ANGLE_EXPLORE = 30

camera_sensor = sensors.camera
dst = 0.0
angle = 0.0
behaviours,params = get_behaviours_and_params(config.behaviour_json, config.params_json)
while(1):
       #client.loop()
       behaviours,params = get_behaviours_and_params(config.behaviour_json, config.params_json)
       obj = params["stateM"]["object_class"]
       box_id = params["stateM"]["box_id"]
       dst,angle = run_state_machine(obj,box_id,camera_sensor,predictor,client,listening,dst,angle,DST_EXPLORE,ANGLE_EXPLORE)
       #print("brain")
       #print(dst,angle)
       """
       behaviours,params = get_behaviours_and_params(config.behaviour_json, config.params_json)
       if behaviours!={}:
          #If behaviour needs image, make sure image is passed as argument to behaviour
          for i in list(behaviours.keys()):
              image = grab_camera_image(camera_sensor)
              if (i!="sleep"):
                 if ("camera" in list(params[i].keys())):
                    eval(behaviours[i])(params[i],image,client)
                 elif ("object_detector" in list(params[i].keys())):
                    eval(behaviours[i])(params[i],image,predictor,client)
                 elif ("param_dependent" in list(params[i].keys())):
                    eval(behaviours[i])(params[i],config.params_json,client)
                 else:
                    eval(behaviours[i])(params[i],client)
                   
       
       while (getattr(listening['Odometer'],'moved')!="1"):
              client.loop()
              a = getattr(listening['Odometer'],'moved')
              if (a=="1"):
                  break
              print("read and sleep")
              eval(behaviours["sleep"])(params["sleep"])
       """
 
client.loop_stop()


