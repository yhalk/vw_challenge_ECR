#! /usr/bin/env python3
import os
import cv2
import csv
import time
import config
import ev3control.slave as slave
import IR.IR_control as remoteControl 
import Sensors.sensors_simple as sensors  
import Vision.frcnn as frcnn
import datetime 
from Vision.vision_commands import *
from communication import comm_init,get_behaviours_and_params

from hello_world import *


#Subscirbe to topics for listening and publishing
client,listening = comm_init(topics_to_listen=config.topics_to_listen, qos_listen=config.qos_listen, topics_to_publish=config.topics_to_publish ,qos_pub=config.qos_pub, listening={}, log=0)

#Create object detector
predictor = frcnn.ObjectPredictor()

print("Client is set up, will start listening now!")

#Wait until listeners have been set up, and then start waiting for values
while (listening=={}):
   print("ss")
   client.loop_read()
client.loop_start()

camera_sensor = sensors.camera

behaviours,params = get_behaviours_and_params(config.behaviour_json, config.params_json)
while(1):
    
    #image = grab_camera_image(camera_sensor)
    
    behaviours,params = get_behaviours_and_params(config.behaviour_json, config.params_json)
    if behaviours!={}:
       for i in list(behaviours.keys()):
           eval(behaviours[i])(params[i])
      
    #Start reading json for behaviour execution
    time.sleep(0.1)
   
client.loop_stop()








"""

#Counter for the image names
data_counter = 0
#Counter for the dataset batch names
run = 0

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


<<<<<<< HEAD
=======


was in loop:

see_and_tell(predictor=predictor,client=client,topic="vision",img=cam_data['onBoardCamera'])
    time.sleep(1)

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
>>>>>>> f4b346205f06949ce8475eea2a6823452481b640


was in loop:

see_and_tell(predictor=predictor,client=client,topic="vision",img=cam_data['onBoardCamera'])
    time.sleep(1)
    data_counter = data_counter + 1


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
