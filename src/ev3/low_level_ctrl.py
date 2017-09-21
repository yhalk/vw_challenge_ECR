import os

def stop_actuator(actuators,stop_action):

    for actuator in actuators:
        actuator.stop(stop_action=stop_action)

#moving motors A,D
def turn_N_steps(actuator1,actuator2,N,speed_sp=360,time_sp=360):
#Turn robot 1 step, i.e. 18 degrees
    for in in xrange(N):
        actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp)
        actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    stop_actuator(actuators=[actuator1,actuator2],stop_action='brake')

def forward_N_steps(actuator1,actuator2,N,speed_sp,time_sp):
    
    for i in xrange(N):
        actuator1.run_timed(time_sp=time_sp,speed_sp=speed_sp)
        actuator2.run_timed(time_sp=time_sp,speed_sp=speed_sp)
    stop_actuator(actuators=[actuator1,actuator2],stop_action='brake')
    

def backward_N_steps(actuator1,actuator2,N,speed_sp,time_sp):

    for i in xrange(N):
        actuator1.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
        actuator2.run_timed(time_sp=time_sp,speed_sp=-speed_sp)
    stop_actuator(actuators=[actuator1,actuator2],stop_action='brake')
    

#manipulation motors C,D
def open_gripper_position(actuator,position,speed_sp,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=position,speed_sp=speed_sp)

    print(actuator.position)
     

def close_gripper_position(actuator,position,speed_sp,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'inverse'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'
    
    print(actuator.position)

    
def lift_gripper_position(actuator,position,speed_sp,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'normal'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=position,speed_sp=speed_sp)

    print(actuator.position)

    
def lower_gripper_position(actuator,position,speed_sp,time_sp=None):

    print(actuator.position)

    actuator.polarity = 'inverse'
    actuator.stop_action = 'hold'
    actuator.run_to_abs_pos(position_sp=position,speed_sp=speed_sp)
    actuator.polarity = 'normal'

    print(actuator.position)


#manipulation motors C,D
def open_gripper_time(actuator,speed_sp,time_sp=None):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)
     

def close_gripper_time(actuator,speed_sp,time_sp=None):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)

    
def lift_gripper_time(actuator,speed_sp,time_sp=None):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)

    
def lower_gripper_time(actuator,speed_sp,time_sp=None):

    actuator.run_timed(time_sp=time_sp,speed_sp=speed_sp)
