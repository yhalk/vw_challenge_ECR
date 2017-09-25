import paho.mqtt.client as mqtt
import jetson_config_i as config
import ev3dev.ev3 as ev3
import ev3control.master as master
from ev3control.messages import *

"""
Motors A,D are motion motors
Motor B is lifting motor
Motor C is clamp motor

"""

def addActuatorDevices(client,topic):
#Use same names as in actuators_and_names_dict
    
    #Motors
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outA)', "ev3.LargeMotor()"),1)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outA)', "address","outA"),1)
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outB)', "ev3.LargeMotor()"),1)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outB)', "address","outB"),1)
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outD)', "ev3.LargeMotor()"),1)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outD)', "address","outD"),1)
    master.publish_cmd(client, topic,AddDeviceMessage('MediumMotor(outC)', "ev3.MediumMotor()"),1)
    master.publish_cmd(client, topic,SetAttrMessage('MediumMotor(outC)', "address","outD"),1)
