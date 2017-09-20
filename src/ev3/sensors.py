import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
import IR_control as remoteControl
import ev3control.master as master
from ev3control.messages import *
import time
from data_collection import DataCollector

ir = remoteControl.InfraredSensor()

#Set IR sensor to remote control mode
ir.mode = "IR-REMOTE"

sensors_names_dict = {"IR_control":ir}

# Make dict where key is sensor name and value
# is a list of all properties of this sensor
items_to_publish = {sensor: [] for sensor in list(sensors_names_dict.keys())}
for sensor_name in list(items_to_publish.keys()):
    sensor = sensors_names_dict[sensor_name]
    for member, dtype in sensor.__class__.__dict__.items():
        if isinstance(dtype, property):
           items_to_publish[sensor_name].append(member)


def addSensorDevices(client,topic):
#Use same names as in sensors_names_dict
    
    #Add remote controller
    master.publish_cmd(client,topic, AddDeviceMessage("IR_control", "remoteControl.InfraredSensor()"),1)
    master.publish_cmd(client,topic, SetAttrMessage("IR_control", "mode","IR-REMOTE"),1)
    master.publish_cmd(client,"data_collect",AddDeviceMessage("data_collector","DataCollector()"),1)
    print("added data")
