import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
import ev3control.master as master
from ev3control.messages import *




#Set up actuators to receive values for their properties
actuators = [
    ev3.LargeMotor(config.LARGE_MOTOR_A),
    ev3.LargeMotor(config.LARGE_MOTOR_B),
    ev3.LargeMotor(config.LARGE_MOTOR_D),
    ev3.MediumMotor(config.MEDIUM_MOTOR),
]


def addActuatorDevices(client,topic,qos):
#Use same names as in actuators_and_names_dict

    #Motors
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outA)', "ev3.LargeMotor()"),1,qos)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outA)', "address","outA"),1,qos)
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outB)', "ev3.LargeMotor()"),1,qos)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outB)', "address","outB"),1,qos)
    master.publish_cmd(client, topic,AddDeviceMessage('LargeMotor(outD)', "ev3.LargeMotor()"),1,qos)
    master.publish_cmd(client, topic,SetAttrMessage('LargeMotor(outD)', "address","outD"),1,qos)
    master.publish_cmd(client, topic,AddDeviceMessage('MediumMotor(outC)', "ev3.MediumMotor()"),1),qos
    master.publish_cmd(client, topic,SetAttrMessage('MediumMotor(outC)', "address","outD"),1,qos)

