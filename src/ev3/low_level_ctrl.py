from ctrl_config import *

def stop_actuator(actuators,stop_action):

    for actuator in actuators:
        actuator.stop(stop_action=stop_action)

#moving motors A,D

def turn_18deg_step(actuator1,actuator2,speed_sp=SPEED_TURN,time_sp=TIME_TURN):
#Turn robot 1 step, i.e. 18 degrees

     actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')
     actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp,stop_action='brake')


def forward_1_step_time(actuator1,actuator2,speed_sp=SPEED_FWD,time_sp=TIME_FWD):
    

    actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')
    actuator2.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='brake')
    


def backward_1_step_time(actuator1,actuator2,speed_sp=SPEED_BWD,time_sp=TIME_BWD):

    actuator1.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    

def forward_1_step_position(actuator1,actuator2,position,speed_sp=SPEED_FWD,time_sp=TIME_FWD):
# 1 step is 3cm with position=100
    actuator1.polarity = 'normal'
    actuator2.polarity = 'normal'
    actuator1.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='brake')
    actuator2.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='brake')



def backward_1_step_position(actuator1,actuator2,position,speed_sp=SPEED_BWD,time_sp=TIME_BWD):
# 1 step is 3cm with position=100

    actuator1.polarity = 'inversed'
    actuator2.polarity = 'inversed'
    actuator1.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='brake')
    actuator2.run_to_rel_pos(position_sp=position,speed_sp=speed_sp,stop_action='brake')
    

#manipulation motors C,D
def open_gripper_position(actuator,position,speed_sp=SPEED_GRIP_OPEN,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)

    print(actuator.position)
     

def close_gripper_position(actuator,position,speed_sp=SPEED_GRIP_CLOSE,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'
    
    print(actuator.position)

    
def lift_gripper_position(actuator,position,speed_sp=SPEED_GRIP_UP,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)

    print(actuator.position)

    
def lower_gripper_position(actuator,position,speed_sp=SPEED_GRIP_DOWN,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'inversed'
    actuator.stop_action = 'hold'
    actuator.run_to_rel_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'

    print(actuator.position)


#manipulation motors C,D
def open_gripper_time(actuator,speed_sp=SPEED_GRIP_OPEN,time_sp=TIME_GRIP_OPEN):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)
     

def close_gripper_time(actuator,speed_sp=SPEED_GRIP_CLOSE,time_sp=TIME_GRIP_CLOSE):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)

    
def lift_gripper_time(actuator,speed_sp=SPEED_GRIP_UP,time_sp=TIME_GRIP_UP):

    
    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='hold')

    
def lower_gripper_time(actuator,speed_sp=SPEED_GRIP_DOWN,time_sp=TIME_GRIP_UP):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp,stop_action='hold')
