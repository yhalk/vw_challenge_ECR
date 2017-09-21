import ev3control.master as master
import IR_control as remoteControl
import ev3dev.ev3 as ev3
from ev3control.messages import *
import csv
import os
import low_level_ctrl as ctrl

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
        speedA  = -360
        time_sp = 360
        N = 1
        ctrl.turn_N_steps(actuators[0],actuators[2],N=N,speed_sp=speedA,time_sp=time_sp)     
    elif (cmd==REMOTE_RED_DOWN):
        speedA  = 360
        time_sp = 360
        N = 1
        ctrl.turn_N_steps(actuators[0],actuators[2],N=N,speed_sp=speedA,time_sp=time_sp)
    elif (cmd==REMOTE_BLUE_UP):
        speedA  = -360
        time_sp = 360
        N = 1
        ctrl.turn_N_steps(actuators[2],actuators[0],N=N,speed_sp=speedA,time_sp=time_sp)     
    elif (cmd==REMOTE_BLUE_DOWN):
        speedA  = 360
        time_sp = 360
        N = 1
        ctrl.turn_N_steps(actuators[2],actuators[0],N=N,speed_sp=speedA,time_sp=time_sp)
    elif (cmd==REMOTE_RED_UP_AND_BLUE_UP):
        speed_sp = 360
        time_sp  = 360
        N = 1
        ctrl.forward_N_steps(actuators[2],actuators[0],N=N,speed_sp=speed_sp,time_sp=time_sp)
    elif (cmd==REMOTE_RED_DOWN_AND_BLUE_DOWN):
        speed_sp = 360
        time_sp  = 360
        N = 1
        ctrl.backward_N_steps(actuators[2],actuators[0],N=N,speed_sp=speed_sp,time_sp=time_sp)
    elif (cmd==REMOTE_BAECON_MODE_ON):
        ctrl.stop_actuator(actuators=[actuators[0],actuators[2]],stop_action='brake')
    else:
        print("Pass motors")
        pass
    return speedA,speedB,0,0
   
     
def gripper_control(actuators,cmd):
    speed_lift = 0
    speed_grip = 0
    print("gripper")
    if (cmd==REMOTE_RED_UP):
        speed_lift = 250
        position_sp = 70
        ctrl.lift_gripper(actuator=actuators[1],position_sp=position_sp,speed_sp=speed_lift)
    elif (cmd==REMOTE_RED_DOWN):
        speed_lift = 250
        position_sp = 70
        ctrl.lower_gripper(actuator=actuators[1],position_sp=position_sp,speed_sp=speed_lift)
    elif (cmd==REMOTE_BLUE_UP):
        position_sp = 90
        speed_sp = 200
        ctrl.open_gripper(actuators[3],position=position_sp,speed_sp=speed_sp)
    elif (cmd==REMOTE_BLUE_DOWN):
        position_sp = 90
        speed_sp = 200
        ctrl.close_gripper(actuators[3],position=position_sp,speed_sp=speed_sp)
    elif (cmd==REMOTE_BAECON_MODE_ON):
        ctrl.stop_actuator(actuators=[actuators[3],actuators[1]],stop_action='brake')
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
        ctrl.stop_actuator(actuators=actuators,stop_action='brake')
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
    
