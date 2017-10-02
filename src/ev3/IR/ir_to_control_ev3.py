import ev3control.master as master
import IR.IR_control as remoteControl
import ev3dev.ev3 as ev3
from ev3control.messages import *
import csv
import os
import MotionCtrl.low_level_ctrl as ctrl
import MotionCtrl.simple_behaviors as behavior
from IR.IR_control import get_IR_cmd
from Sensors.sensors import publishable_names_dict


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

def motor_control(cmd): 
    speedA = 0
    speedB = 0
    print("motor_ctrl")
    if (cmd==REMOTE_RED_UP):
        #ctrl.move_towards_object(310, 15) 
        #ctrl.turn_left_deg(90)
        #behavior.move_to_and_grab_2()
        behavior.move_to_box_and_release(310, 15)
    elif (cmd==REMOTE_BLUE_UP):
        #ctrl.move_and_grab(actuators[0], actuators[2], actuators[3], actuators[1])
        ctrl.forward_cm(10)#position_pid(10, 0, 0, 0)
        print("IR: Move forward command")
    elif (cmd==REMOTE_BLUE_DOWN):
        ctrl.backward_cm(10)
        print("IR: Move backward command")
    elif (cmd==REMOTE_RED_DOWN):
        #ctrl.turn_deg_position(actuators[0], actuators[2], 15)
        ctrl.turn_right_deg(10)
        print("IR: Turn!")
    elif (cmd==REMOTE_RED_UP_AND_BLUE_UP):
        ctrl.forward_position(100)
    elif (cmd==REMOTE_RED_DOWN_AND_BLUE_DOWN):
        ctrl.backward_position(100)
    elif (cmd==REMOTE_BAECON_MODE_ON):
        ctrl.stop_actuator(stop_action='brake')
    else:
        print("Pass motors")
        pass
    return speedA,speedB,0,0
   
     
def gripper_control(cmd):
    speed_lift = 0
    speed_grip = 0
    print("gripper")
    if (cmd==REMOTE_RED_UP):
        ctrl.lift_gripper_abs_position()
    elif (cmd==REMOTE_RED_DOWN):
        ctrl.lower_gripper_abs_position()
    elif (cmd==REMOTE_BLUE_UP):
        #ctrl.open_gripper_full(actuators[3], position=100)
        ctrl.open_gripper_abs_position()
    elif (cmd==REMOTE_BLUE_DOWN):
        #ctrl.close_gripper_full(position=70)
        ctrl.close_gripper_abs_position()
    elif (cmd==REMOTE_BAECON_MODE_ON):
        ctrl.stop_actuator(stop_action='brake')
    else:
        print("Pass gripper")
        pass
    return 0,0,speed_lift,speed_grip
    
def calibration(cmd):
    print("Calibrating!")
    if (cmd==REMOTE_RED_UP):
        ctrl.get_actuators_values() 
    elif (cmd==REMOTE_BLUE_UP):
        ctrl.open_gripper_position(70)
    elif (cmd==REMOTE_BLUE_DOWN):
        ctrl.close_gripper_position(70)
    else:
        print("Pass calibration")
        pass
    return 0,0,0,0
    

def emergency(cmd):
    
    sA = None
    sB = None
    sC = None
    sD = None
    print("emergency")
    if (cmd==REMOTE_BAECON_MODE_ON):
        ctrl.stop_actuator(stop_action='brake')
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
                 2 : calibration,
                 3 : emergency
               }


def ir_to_control(channel,cmd):
    #Return speed_sp of motor A,B,C,D - 0 if stopped
    if channel!=-1:
       return call_channel[channel](cmd)    
    else:
       return None,None,None,None
   


def IR_controller():

   (channel,cmd,valid) = get_IR_cmd(publishable_names_dict["IR_control"])
   _,_,_,_ = ir_to_control(int(channel),int(cmd))
   if int(channel)==3:
      return 1
   return 0
 
