from MotionCtrl import low_level_ctrl as ctrl
from MotionCtrl.ctrl_config import *
import math

def move_and_grab():
    lower_gripper_position(60)
    forward_position(600)
    lower_gripper_position(30)
    close_gripper_full(5*100)
    lift_gripper_position(100)
    forward_position(300)
    open_gripper_full(3*100)
    backward_position(300)

def move_to_and_grab():
    forward_position(300)
    lower_gripper_position(30)
    close_gripper_full(5*100)
    lift_gripper_position(100)
    #forward_1_step_position(actuator1,actuator2, 300)
    #time.sleep(2)
    backward_position(300)
    turn_right_deg(90)
    open_gripper_full(3*100)

def move_to_and_grab_box():
    dist = 0
    angle = 0
    ctrl.open_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.lower_gripper_abs_position()
    ctrl.wait_for(1)
    dist += ctrl.forward_cm(10)
    ctrl.wait_for(1)
    ctrl.close_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.lift_gripper_abs_position()
    ctrl.wait_for(1)
    dist += ctrl.backward_cm(10)
    ctrl.wait_for(1)
    angle += ctrl.turn_right_deg(90)
    ctrl.wait_for(1)
    ctrl.open_gripper_abs_position()
    ctrl.wait_for(1)
    return (dist, angle)

def check_if_in_gripper(distance):
    if distance < DISTANCE_LIMIT_CM:
        return True
    else:
        return False


def rad_to_deg(rad):
    return rad*(180/math.pi)

def deg_to_rad(deg):
    return deg*(math.pi/180)


def transform_img_to_robot_level(cam_dist, cam_angle):
    print("Beh: Object received in distance " + str(cam_dist) + " and angle " + str(cam_angle))
    cam_angle += 90
    x_cam = math.sin(deg_to_rad(cam_angle)) * cam_dist
    x_robot = x_cam - CAM_ROBOT_DISTANCE
    y_robot = math.cos(deg_to_rad(cam_angle)) * cam_dist
    robot_dist = math.sqrt(x_robot*x_robot + y_robot*y_robot)
    robot_angle = math.atan2(y_robot,x_robot)
    print(".. and translated in distance " + str(robot_dist) + " and angle " + str(rad_to_deg(robot_angle)))
    return robot_dist, rad_to_deg(robot_angle)


def move_to(distance, angle):
    
    if abs(distance-0.0)<0.0000001 and abs(angle-0.0)<0.00000001:
       return (0,0)

    return transform_img_to_robot_level(distance, angle)  #rm return and uncomment
    """
    angle -= CAMERA_ANGLE_OFFSET  
    deg = ctrl.turn_left_deg(angle)
    ctrl.wait_for(1)
    #ctrl.lift_gripper_abs_position()
    ctrl.lower_gripper_reset_position()
    ctrl.wait_for(0.5)
    dist = ctrl.forward_cm(ctrl.mm_to_cm(distance))
    ctrl.wait_for(1)
    """
    return (dist, deg)


def release_obj():
    ctrl.open_gripper_abs_position()
    ctrl.wait_for(0.5)
    dist = ctrl.backward_cm(20)
    ctrl.wait_for(0.5)
    ctrl.lower_gripper_reset_position()
    return dist
    
def reset_gripper():
    ctrl.open_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.lower_gripper_reset_position() 


def move_to_box_and_release(distance, angle):
    dist = 0
    deg = 0

    #calibrate for box depth
    distance -= BOX_DEPTH
    print("distance "+distance)
    [d, a] = move_to(distance, angle)
    deg += a
    print("deg "+deg)
    dist+=d
    print("dist "+dist)
    d = release_obj()
    dist+=d
    print("dist "+dist)
    reset_gripper()
    print("MC: Travelled for " + str(dist) + " cm and " + str(deg) +  " degrees.")
    return (dist, deg)
"""
    deg = ctrl.turn_right_deg(angle)
    ctrl.wait_for(1)
    ctrl.lift_gripper_abs_position()
    ctrl.wait_for(0.5)
    dist = ctrl.forward_cm(ctrl.mm_to_cm(distance))
    ctrl.wait_for(1)
    ctrl.open_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.backward_cm(20)
    ctrl.wait_for(1)
    ctrl.lower_gripper_reset_position()
"""

def grasp_brick():
    ctrl.lower_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.close_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.lift_gripper_abs_position()
    ctrl.wait_for(1)



def move_and_grasp_object(distance, angle):
    [d, a] = move_to(distance, angle)
    grasp_brick()
    print("MC: Travelled for " + str(dist)+ " cm and " + str(deg)+ " degrees.")
    return (d,a)


def move_towards_object( distance, angle):
    print("Beh: Moving towards object "+ str(distance) + " " + str(angle))
    offset = 10
    percentage = 1.0
    deg = ctrl.turn_right_deg(angle)
    dist = 0
    ctrl.wait_for(2)
    if check_if_in_gripper(ctrl.mm_to_cm(distance)):
        print("MC: In gripper distance")
        #forward_cm(actuator1, actuator2, mm_to_cm(distance)+offset)
        [d,a] = move_to_and_grab_box()
        dist += d
        deg += a
    else:
        print("MC: move towards object "+ str(percentage*ctrl.mm_to_cm(distance)))
        dist = ctrl.forward_cm(percentage*ctrl.mm_to_cm(distance))
        [d,a] = move_to_and_grab_box()
        dist += d
        deg +=a
        ctrl.lower_gripper_reset_position()        
    return (dist, deg)

