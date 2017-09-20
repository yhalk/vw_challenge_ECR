import ev3control.master as master
import IR_control as remoteControl
import ev3dev.ev3 as ev3
from ev3control.messages import *
import csv
import os

REMOTE_NONE = 0
REMOTE_RED_UP = 1
REMOTE_RED_DOWN = 2
REMOTE_BLUE_UP = 3
REMOTE_BLUE_DOWN = 4
REMOTE_RED_UP_AND_BLUE_UP = 5
REMOTE_RED_UP_AND_BLUE_DOWN = 6
REMOTE_RED_DOWN_AND_BLUE_UP = 7
REMOTE_RED_DOWN_AND_BLUE_DOWN = 8
REMOTE_BAECON_MODE_ON = 9
REMOTE_RED_UP_AND_RED_DOWN = 10
REMOTE_BLUE_UP_AND_BLUE_DOWN = 11


def motor_control(actuators,cmd): 
    speedA = 0
    speedB = 0
    print("motor_ctrl")
    if (cmd==REMOTE_RED_UP):
        speedA = -100
        actuators[0].run_forever(speed_sp=speedA)
        actuators[2].run_forever(speed_sp=-speedA)
    elif (cmd==REMOTE_RED_DOWN):
        speedA = 100
        actuators[0].run_forever(speed_sp=speedA)
        actuators[2].run_forever(speed_sp=-speedA)
    elif (cmd==REMOTE_BLUE_UP):
        speedB = -100
        actuators[2].run_forever(speed_sp=speedB)
        actuators[0].run_forever(speed_sp=-speedB)
    elif (cmd==REMOTE_BLUE_DOWN):
        speedB = 100
        actuators[2].run_forever(speed_sp=speedB)
        actuators[0].run_forever(speed_sp=-speedB)
    elif (cmd==REMOTE_RED_UP_AND_BLUE_UP):
        speedA = 100
        actuators[0].run_forever(speed_sp=speedA)
        speedB = 100
        actuators[2].run_forever(speed_sp=speedB)
    elif (cmd==REMOTE_RED_DOWN_AND_BLUE_DOWN):
        speedA = -100
        actuators[0].run_forever(speed_sp=speedA)
        speedB = -100
        actuators[2].run_forever(speed_sp=speedB)
    elif (cmd==REMOTE_BAECON_MODE_ON):
        actuators[0].stop(stop_action='brake')
        actuators[2].stop(stop_action='brake')
    else:
        print("Pass motors")
        pass
    return speedA,speedB,0,0
   
     
def gripper_control(actuators,cmd):
    speed_lift = 0
    speed_grip = 0
    print("gripper")
    if (cmd==REMOTE_RED_UP):
        speed_lift = 100
        actuators[1].run_to_rel_pos(position_sp=70,speed_sp=speed_lift)
    elif (cmd==REMOTE_RED_DOWN):
        speed_lift = -100
        actuators[1].run_to_rel_pos(position_sp=-50,speed_sp=speed_lift)
    elif (cmd==REMOTE_BLUE_UP):
        #print("counts")
        #print(actuators[3].count_per_m())
        #print(actuators[3].count_per_rot())
        speed_grip = 300
        actuators[3].run_forever(speed_sp=speed_grip)
    elif (cmd==REMOTE_BLUE_DOWN):
        speed_grip = -300
        actuators[3].run_forever(speed_sp=speed_grip)
    elif (cmd==REMOTE_BAECON_MODE_ON):
        actuators[3].stop(stop_action='hold')
        actuators[1].stop(stop_action='hold')
    else:
        print("Pass gripper")
        pass
    return 0,0,speed_lift,speed_grip
    

def emergency(actuators,cmd):
    
    sA = None
    sB = None
    sC = None
    sD = None
    print("emergency")
    if (cmd==REMOTE_BAECON_MODE_ON):
        actuators[0].stop(stop_action='brake')
        actuators[1].stop(stop_action='brake')
        actuators[2].stop(stop_action='brake')
        actuators[3].stop(stop_action='brake')
        sA = 0
        sB = 0
        sC = 0
        sD = 0
    else:
        print("Pass emergency")
        pass
    return sA,sB,sC,sD
    


call_channel = { 0 : motor_control,
                 1 : gripper_control,
                 3 : emergency
               }


def ir_to_control(actuators,channel,cmd):


    #Return speed_sp of motor A,B,C,D - 0 if stopped
    if channel!=-1:
       return call_channel[channel](actuators,cmd)    
    else:
       return None,None,None,None
    
