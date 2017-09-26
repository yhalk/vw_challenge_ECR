from MotionCtrl.ctrl_config import *
import time
from MotionCtrl import actuators_simple as acts
actuators = acts.actuators

print(actuators[0].position_p)
print(actuators[0].position_i)
print(actuators[0].position_d)
def stop_actuator(stop_action):

    for actuator in actuators:
        actuator.stop(stop_action=stop_action)

#moving motors A,D
## ROTATION
###############################################
def turn_18deg_step(actuator1=actuators[0],actuator2=actuators[2],speed_sp=SPEED_TURN,time_sp=TIME_TURN):
     #Turn robot 1 step, i.e. 18 degrees
     actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')
     actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp,stop_action='brake')


def turn_deg_position(position,actuator1=actuators[0], actuator2=actuators[2], speed_sp=SPEED_TURN,time_sp=TIME_TURN):
    #4.2 degrees with position 25
    actuator1.run_to_rel_pos(position_sp=position, speed_sp=speed_sp,stop_action='hold')
    actuator2.run_to_rel_pos(position_sp=-position, speed_sp=speed_sp,stop_action='hold')


def turn_right_deg( degrees, actuator1=actuators[0], actuator2=actuators[2]):
    if LOG_ON==1:
        print("MC: Rotate R for "+str(degrees) + " new position " + str((degrees)*TURN_RIGHT_TICKS_PER_DEG))
        print("MC: position before "+ str(actuator1.position) + " " + str(actuator2.position))
    turn_deg_position((degrees*TURN_RIGHT_TICKS_PER_DEG))
    time.sleep(1)
    if LOG_ON==1:
        print("... and position after "+ str(actuator1.position) + " " + str(actuator2.position))
    

def turn_left_deg( degrees, actuator1=actuators[0], actuator2=actuators[2]):
    if LOG_ON==1:
        print("MC: Rotate L for "+str(degrees) + " new position " + str((degrees)*TURN_RIGHT_TICKS_PER_DEG))
        print("MC: position before "+ str(actuator1.position) + " " + str(actuator2.position))
    turn_deg_position( -(degrees*TURN_LEFT_TICKS_PER_DEG))
    time.sleep(1)
    if LOG_ON==1:
        print("... and position after "+ str(actuator1.position) + " " + str(actuator2.position))


## TRANSLATION
#############################################


def forward_1_step_time(actuator1=actuators[0],actuator2=actuators[2],speed_sp=SPEED_FWD,time_sp=TIME_FWD):
    actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')
    actuator2.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')


def backward_1_step_time(actuator1=actuators[0],actuator2=actuators[2],speed_sp=SPEED_BWD,time_sp=TIME_BWD):
    actuator1.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    

def forward_position(position, actuator1=actuators[0],actuator2=actuators[2],speed_sp=SPEED_FWD,time_sp=TIME_FWD):
    # 1 step is 10cm with position=360
    print(actuator1)

    actuator1.polarity = 'normal'
    actuator2.polarity = 'normal'
    actuator1.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='hold')
    actuator2.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='hold')



def backward_position(position, actuator1=actuators[0],actuator2=actuators[2],speed_sp=SPEED_BWD,time_sp=TIME_BWD):
    # 1 step is 3cm with position=100
    actuator1.polarity = 'inversed'
    actuator2.polarity = 'inversed'
    actuator1.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='hold')
    actuator2.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='hold')




def forward_cm(cm, actuator1=actuators[0], actuator2=actuators[2]):
    if LOG_ON==1:
        print("MC: Move for "+str(cm) + " new position " + str(cm*FORWARD_TICKS_PER_CM))
        print("MC: position before "+ str(actuator1.position) + " " + str(actuator2.position))
    forward_position(cm*FORWARD_TICKS_PER_CM)
    time.sleep(cm*0.15)
    if LOG_ON==1:
        print("MC: position after "+ str(actuator1.position) + " " + str(actuator2.position))
  
 
def backward_cm(cm, actuator1=actuators[0], actuator2=actuators[2]):
    if LOG_ON==1:
        print("MC: Move for "+str(cm) + " new position " + str(cm*BACKWARD_TICKS_PER_CM))
        print("MC: position before "+ str(actuator1.position) + " " + str(actuator2.position))
    backward_position(cm*BACKWARD_TICKS_PER_CM)
    time.sleep(cm*0.15)
    if LOG_ON==1:
        print("MC: position after "+ str(actuator1.position) + " " + str(actuator2.position))


def forward_position_pid(position, actuator1 = actuators[0], actuator2=actuators[2], speed_sp=SPEED_FWD):
    actuator1.position_p = 1
    actuator1.position_i = 0
    actuator1.position_d = 0
    actuator2.position_p = 1
    actuator2.position_i = 0    
    actuator2.position_d = 0
    forward_position(position)    

#manipulation motors C,D
# GRIPPER
################################################
# OPEN - CLOSE
################################################

def open_gripper_abs_position(position,actuator=actuators[3],speed_sp=SPEED_GRIP_OPEN,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before opening " + str(actuator.position))

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=GRIP_OPEN_POS,speed_sp=speed_sp, stop_action='hold')
    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after" + str(actuator.position))
     

def close_gripper_abs_position(position,actuator=actuators[3],speed_sp=SPEED_GRIP_CLOSE,time_sp=None):
    if LOG_ON==1:
        print("MC: Gripper position before closing " + str(actuator.position))

#    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=GRIP_CLOSE_POS,speed_sp=speed_sp, stop_action='hold')
#    actuator.polarity = 'normal'
    
    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after " + str(actuator.position))





def open_gripper_position(position,actuator=actuators[3],speed_sp=SPEED_GRIP_OPEN,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before opening " + str(actuator.position))

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after" + str(actuator.position))
     

def close_gripper_position(position,actuator=actuators[3], speed_sp=SPEED_GRIP_CLOSE,time_sp=None):
    if LOG_ON==1:
        print("MC: Gripper position before closing " + str(actuator.position))

    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'
    
    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after " + str(actuator.position))


def open_gripper_full(position,actuator=actuators[3]):
    #for i in range(7):
    #print(i)
    open_gripper_position(actuator, position)
    #    time.sleep(0.2)

def close_gripper_full(position,actuator=actuators[3]):
    #for i in range(7):
    #print(i)
    close_gripper_position(actuator, position)


def open_gripper_time(actuator=actuators[3],speed_sp=SPEED_GRIP_OPEN,time_sp=TIME_GRIP_OPEN):
    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)
     

def close_gripper_time(actuator=actuators[3],speed_sp=SPEED_GRIP_CLOSE,time_sp=TIME_GRIP_CLOSE):
    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)


# UP - DOWN
###############################################    
def lift_gripper_position(position,actuator=actuators[1],speed_sp=SPEED_GRIP_UP,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before lifting " + str(actuator.position))

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    time.sleep(1)

    if LOG_ON==1:
        print("... and gripper position after lifting " + str(actuator.position))

    
def lower_gripper_position(position,actuator=actuators[1],speed_sp=SPEED_GRIP_DOWN,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before lowering " + str(actuator.position))

    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'

    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after lowering " + str(actuator.position))
  
def lift_gripper_abs_position(position,actuator=actuators[1],speed_sp=SPEED_GRIP_UP,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before lifting " + str(actuator.position))

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=GRIP_UPPER_POS,speed_sp=speed_sp)
    time.sleep(1)

    if LOG_ON==1:
        print("... and gripper position after lifting " + str(actuator.position))

    
def lower_gripper_abs_position(position,actuator=actuators[1],speed_sp=SPEED_GRIP_DOWN,time_sp=None):

    if LOG_ON==1:
        print("MC: Gripper position before lowering " + str(actuator.position))

#    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=GRIP_LOWER_POS,speed_sp=speed_sp)
#    actuator.polarity = 'normal'

    time.sleep(1)
    if LOG_ON==1:
        print("... and gripper position after lowering " + str(actuator.position))
  
    
def lift_gripper_time(actuator=actuators[1],speed_sp=SPEED_GRIP_UP,time_sp=TIME_GRIP_UP):
    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='hold')

    
def lower_gripper_time(actuator=actuators[1],speed_sp=SPEED_GRIP_DOWN,time_sp=TIME_GRIP_UP):
    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='hold')




# BEHAVIORS - TODO: go to a different file
#############################################
def move_and_grab(actuator1=actuators[0], actuator2=actuators[2], actuator3=actuators[3], actuator4=actuators[1]):
    lower_gripper_position(60)
    time.sleep(2)
    forward_position(600)
    time.sleep(2)
    lower_gripper_position(30)
    time.sleep(2)
    close_gripper_full(5*100)
    time.sleep(2)
    lift_gripper_position(100)
    time.sleep(2)
    forward_position(300)
    time.sleep(2)
    open_gripper_full(3*100)
    time.sleep(2)
    backward_position(300)
    time.sleep(2)

def move_to_and_grab(actuator1=actuators[0], actuator2=actuators[2], actuator3=actuators[3], actuator4=actuators[1]):
    time.sleep(2)
    forward_position(300)
    time.sleep(2)
    lower_gripper_position(30)
    time.sleep(2)
    close_gripper_full(5*100)
    time.sleep(2)
    lift_gripper_position(100)
    time.sleep(2)
    #forward_1_step_position(actuator1,actuator2, 300)
    #time.sleep(2)
    backward_position(300)
    time.sleep(2)
    turn_right_deg(90)
    time.sleep(2)
    open_gripper_full(3*100)
    time.sleep(2)


def check_if_in_gripper(distance):
    if distance < DISTANCE_LIMIT_CM:
        return True
    else:
        return False

def move_towards_object( distance, angle, actuator1=actuators[0], actuator2=actuators[2], actuator3=actuators[3], actuator4=actuators[1]):
    offset = 10
    percentage = 1.0
    turn_right_deg(angle)
    time.sleep(2)
    if check_if_in_gripper(mm_to_cm(distance)):
        print("MC: In gripper distance")
        #forward_cm(actuator1, actuator2, mm_to_cm(distance)+offset)
        move_to_and_grab()
    else:
        print("MC: move towards object "+ str(percentage*mm_to_cm(distance)))
        forward_cm(percentage*mm_to_cm(distance))
        move_to_and_grab()
        lower_gripper_position(80)
        open_gripper_full(100)
        

def mm_to_cm(mm):
    return (mm/10)
