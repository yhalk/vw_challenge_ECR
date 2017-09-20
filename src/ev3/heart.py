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

def on_log(client, userdata, level, buf):
   print("EV3 log: ",buf)

actuators = {}
#Set up EV3 client
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
client.on_message = partial(slave.process_message, actuators)
client.subscribe("actuators",qos=2)  
topic = "sensors"
client.on_log = on_log

#client.loop_start()

while (actuators=={}):
     client.loop_read()
     

#Add sensors for which we publish values to the Jetson list of receiving sensor values
addSensorDevices(client,topic)


actuators['LargeMotor(outA)'] = ev3_actuators[0]
actuators['LargeMotor(outB)'] = ev3_actuators[1]
actuators['LargeMotor(outD)'] = ev3_actuators[2]
actuators['MediumMotor(outC)'] = ev3_actuators[3]

print(actuators)

counter = 0
channel_prev = -1
cmd_prev = -1
#If IR return list is != [0,0,0,0]
valid = 0

while(1):
   #Read IR controller input
   (channel,cmd,valid) = get_IR_cmd(sensors_names_dict["IR_control"])

   #Publish sensor readings
   for sensor, property_names in items_to_publish.items():
        for property_name in property_names:
           if ((sensor=="IR_control") and (property_name=="cmd") and (valid==1)):
              master.publish_cmd(client,topic,SetAttrMessage(sensor, property_name, str(cmd)))
           elif ((sensor=="IR_control") and (property_name=="channel") and (valid==1)):
              master.publish_cmd(client,topic,SetAttrMessage(sensor, property_name, str(channel)))
           else:
              pass
    
   #Get and set actuator properties
   client.loop_read()   

   print("EV3 work in progress..."+str(counter))
   counter = counter + 1
   time.sleep(0.2)
   
client.disconnect()

