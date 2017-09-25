#! /usr/bin/env python3
import os
import cv2
import csv
import time
from functools import partial
import paho.mqtt.client as mqtt
import jetson_config_i as config
import ev3control.slave as slave
from ir_to_control import ir_to_control,data_collection_and_camera
import IR_control as remoteControl ##Needed if included in sensors_simple??
from actuators_simple import addActuatorDevices
import sensors_simple   
from data_collection import DataCollector
#import frcnn
import datetime 
from vision_commands import *


imu = sensors_simple.IMU()

   
 
def on_log(client, userdata, level, buf):
   print("Jetson log: ",buf)

sensors = {}
#Set up client to receive sensor values and send actuator commands
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
client.on_message = partial(slave.process_message, sensors)
client.subscribe("sensors",qos=2)            
client.subscribe("data_collect",qos=2)
topic="actuators"
#client.on_log = on_log


#Add actuators for which we publish values to the EV3 list of receiving actuator values
addActuatorDevices(client,topic)
addVisionDevices(client,topic="vision")

#predictor = frcnn.ObjectPredictor()


print("Client is set up, will start listening now!")


while (sensors=={}):
   client.loop_read()


client.loop_start()

#Counter for the image names
data_counter = 0
#Counter for the dataset batch names
run = 0
"""
#Flag for setting data recording on (1) or off (0)
record = 0
#Path for saving data, will be set from storing function
path = None
fileID = None
writer = None
channel = -1
cmd = -1
motA,motB,gripC,gripD = -1,-1,-1,-1
channel_prev = sensors["IR_control"].get_channel()
cmd_prev = sensors["IR_control"].get_cmd()
"""


while(1):
    #cam_data = sensors_simple.camera.read()    
    #see_and_tell(predictor=predictor,client=client,topic="vision",img=cam_data['onBoardCamera'])
    #time.sleep(1)
    channel = getattr(sensors["IR_control"],'channel')
    cmd = getattr(sensors["IR_control"],'cmd')
    print(channel)
    print(cmd)
    if (int(channel)==0 and int(cmd)==9):
          print("CHANGE RUN")
    for _ in range(10):
        time.sleep(0.2)
        imu_data = imu.read()
        print("imu data: {}".format(imu_data))

    data_counter = data_counter + 1
    #time.sleep(0.2)
   
client.loop_stop()


"""
channel = sensors["IR_control"].get_channel()
    cmd = sensors["IR_control"].get_cmd()
    cam_data = sensors_simple.camera.read()
    
    #Decode IR input and issue command
    if (int(channel)==2):
          print("data collect")
          print(sensors["data_collector"].get_data())
          img_name = "./image_rec"+str(data_counter)+".jpg"
          data_counter = data_counter + 1
          a = datetime.datetime.now()
          #predictor.detect_known_objects(cam_data['onBoardCamera'])
          #print(predictor.ret_detected_objects)
          b = datetime.datetime.now()
          delta = b - a
          print("identifying objects in 1 took:", int(delta.total_seconds() * 1000)) # milliseconds
          
          cv2.imshow(img_rec)
          cv2.waitKey(20)
          
          #record,fileID,path,run,writer = data_collection_and_camera(int(cmd),run,sensors["IR_control"],path,fileID)
    elif (int(channel)==0 or int(channel)==1 or int(channel)==3):
          motA,motB,gripC,gripD = ir_to_control(client,topic,sensors)
    else:
          print("Invalid channel")
          pass

    if (channel==3) and (motA==0) and (motB==0) and (gripC==0) and (gripD==0):
          print("Emergency stop")
          if fileID!=None:
             fileID.close()
          break  # remove for possibility of recovery
        
    #Save data if selected
    if (record==1):
       #Directory ./data/runX/ must have been created already
       img_name = "./run_"+str(run)+"/image"+str(data_counter)+".jpg"  
       cv2.imwrite(img_name,cam_data['onBoardCamera'])
       #save sensor + actuators values
       if fileID!=None:
           data_to_save = [img_name,str(motA),str(motB),str(gripC),str(gripD)]
           #writer.writerow(data_to_save)
       else:
           print("Something went wrong with csv opening")
           pass

"""
