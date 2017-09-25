#! /usr/bin/env python3

from functools import partial
import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
from sensors import sensors_names_dict, items_to_publish, addSensorDevices
import time
import ev3control.master as master
import ev3control.slave as slave
from ev3control.messages import *
from IR_control import get_IR_cmd
from actuators_simple import ev3_actuators
import data_collection
import datetime
from vision_commands import * 
import ir_to_control_ev3 as ir_ctrl
import low_level_ctrl as ctrl

def on_log(client, userdata, level, buf):
   print("EV3 log: ",buf)

actuators = {}
#Set up EV3 client
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
client.on_message = partial(slave.process_message, actuators)
client.subscribe("actuators",qos=2)  
client.subscribe("vision")
topic = "sensors"
topic_data = "data_collect"

#client.on_log = on_log

client.loop_start()


    
#camera_feedback = actuators['Vision'] 
while (actuators=={}):
     client.loop_read()
     


while(1):
    
   #Get and set actuator properties
   client.loop_read()   

   print("EV3 work in progress..."+str(counter))
   counter = counter + 1
   time.sleep(0.2)
   
client.disconnect()

