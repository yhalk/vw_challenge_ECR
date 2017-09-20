import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3

#Set up actuators to receive values for their properties
ev3_actuators = [
    ev3.LargeMotor(config.LARGE_MOTOR_A),
    ev3.LargeMotor(config.LARGE_MOTOR_B),
    ev3.LargeMotor(config.LARGE_MOTOR_D),
    ev3.MediumMotor(config.MEDIUM_MOTOR),
]


