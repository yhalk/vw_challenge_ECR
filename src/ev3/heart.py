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
 
import ir_to_control_ev3 as ir_ctrl

def on_log(client, userdata, level, buf):
   print("EV3 log: ",buf)

actuators = {}
#Set up EV3 client
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
client.on_message = partial(slave.process_message, actuators)
client.subscribe("actuators",qos=2)  
topic = "sensors"
topic_data = "data_collect"

client.on_log = on_log

#client.loop_start()


while (actuators=={}):
     client.loop_read()
     

#Add sensors for which we publish values to the Jetson list of receiving sensor values
#Add also data collector atm
addSensorDevices(client,topic)

"""
actuators['LargeMotor(outA)'] = ev3_actuators[0]
actuators['LargeMotor(outB)'] = ev3_actuators[1]
actuators['LargeMotor(outD)'] = ev3_actuators[2]
actuators['MediumMotor(outC)'] = ev3_actuators[3]
"""
actuators_l = [ev3_actuators[0],ev3_actuators[1],ev3_actuators[2],ev3_actuators[3]]
print(actuators_l)

counter = 0
channel_prev = -1
cmd_prev = -1
#If IR return list is != [0,0,0,0]
valid = 0
#Values to transmit for data collection
a,b,grip,lift,timestamp = -1,-1,-1,-1,-1

data_collector = data_collection.DataCollector()

while(1):
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
   
   print(getattr(camera_feedback,'distance'))
   print(getattr(camera_feedback,'angle')) 
   print(getattr(camera_feedback,'class_name'))
   
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

   print("EV3 work in progress..."+str(counter))
   counter = counter + 1
   time.sleep(0.2)
   
client.disconnect()

