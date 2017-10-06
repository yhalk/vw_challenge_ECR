from Sensors.sensors_simple import IR_teensy

def avoid_obstacle():
    '''
       Avoiding the obstacle that is detected in front of the gripper.
       The behaviour for this is to box the obstacle:
        -turn right for 90 degrees
        -move forward for 20 cm
        -turn left for 90 degrees
        -move forward for 20 cm
        -turn left for 90 degrees
        -move forward for 20 cm
        -turn right for 90 degrees
    '''
    return [(20, 90), (20,-90), (20, -90), (0,90)
