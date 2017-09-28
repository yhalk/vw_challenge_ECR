import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
import IR.IR_control as remoteControl
import ev3control.master as master
from ev3control.messages import *
import time
from MotionCtrl.actuators_simple import actuators
from Sensors.odometry_ev3 import Odometry

#Set IR sensor to remote control mode
ir = remoteControl.InfraredSensor()
ir.mode = "IR-REMOTE"

#Get odometer
odometer = Odometry()

publishable_names_dict = { "IR_control":ir,
                            config.LARGE_MOTOR_A:actuators[0],
                            config.LARGE_MOTOR_B:actuators[1],
                            config.LARGE_MOTOR_D:actuators[2],
                            config.MEDIUM_MOTOR:actuators[3],
                            "odometer":odometer
                          }

# Make dict where key is sensor name and value
# is a list of all properties of this sensor
items_to_publish = {pub: [] for pub in list(publishable_names_dict.keys())}
for pub_name in list(items_to_publish.keys()):
    pub_obj = publishable_names_dict[pub_name]
    for member, dtype in pub_obj.__class__.__dict__.items():
        if isinstance(dtype, property):
           items_to_publish[pub_name].append(member)


def addSensorDevices(client,topic,qos):
#Use same names as in sensors_names_dict
    
    #Add remote controller
    master.publish_cmd(client,topic, AddDeviceMessage("IR_control", "remoteControl.InfraredSensor()"),1,qos=qos)
    master.publish_cmd(client,topic, SetAttrMessage("IR_control", "mode","IR-REMOTE"),1,qos=qos)
    
