from MotionCtrl import low_level_ctrl as ctrl
from MotionCtrl.ctrl_config import *
import math


def check_if_in_gripper(distance):
    if distance < DISTANCE_LIMIT_MM:
        return True
    else:
        return False


def rad_to_deg(rad):
    return rad*(180/math.pi)

def deg_to_rad(deg):
    return deg*(math.pi/180)


def transform_img_to_robot_level(cam_dist, cam_angle):
    print("Beh: Object received in distance " + str(cam_dist) + " and angle " + str(cam_angle))

    if abs(cam_dist-0.0) < 0.001:
        return 0, cam_angle

    return cam_dist, cam_angle

    cam_angle += 90
    x_cam = math.sin(deg_to_rad(cam_angle)) * cam_dist
    #x_robot = x_cam - CAM_ROBOT_DISTANCE
    if cam_angle > 0:
        x_robot = x_cam - CAM_ROBOT_DISTANCE
    else:
        x_robot = x_cam + CAM_ROBOT_DISTANCE
    y_robot = math.cos(deg_to_rad(cam_angle)) * cam_dist
    robot_dist = math.sqrt(x_robot*x_robot + y_robot*y_robot)
    if (cam_dist <0):
        robot_dist = -robot_dist
    robot_angle = -math.atan2(y_robot,x_robot)
    print("... and translated in distance " + str(robot_dist) + " and angle " + str(rad_to_deg(robot_angle)))
    return robot_dist, rad_to_deg(robot_angle)


def move_to(distance, angle):
    print("Beh: Message received distance " + str(distance) + " angle " + str(angle)) 

    flag = ""
    dist = 0.0
    deg = 0.0

    if abs(distance-0.0)<0.0000001 and abs(angle-0.0)<0.00000001:
       return (0,0, flag)
    if abs(angle) < 10:
        angle = 0
    [d, a] = transform_img_to_robot_level(distance, angle)  #rm return and uncomment

    flag = "moved"

    a -= CAMERA_ANGLE_OFFSET  
    if abs(a-0.0) > 0.000001:
        deg = ctrl.turn_left_deg(PERCENTAGE_TURN*a)
    ctrl.wait_for(1)
    #ctrl.lift_gripper_abs_position()
    #ctrl.lower_gripper_reset_position()
    ctrl.wait_for(0.5)
    if abs(distance-0.0)>0.1:
        dist = ctrl.forward_cm(ctrl.mm_to_cm(PERCENTAGE_MOVE*d))
    ctrl.wait_for(1)
    
    return (dist, deg, flag)


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
    flag = ""
    if distance == 0 and angle == 0:
        return 0,0, flag

    #calibrate for box depth
    distance -= BOX_DEPTH
    if distance < DISTANCE_LIMIT_BOX_MM:
        flag = "release"
        d = release_obj()
        [d,a,f] = move_to(distance, angle)
        dist+=d
        reset_gripper()
    else:    
        [d, a, f] = move_to((distance), angle)
        deg += a
        dist+=d
    print("MC: Travelled for " + str(dist) + " cm and " + str(deg) +  " degrees.")
    return (ctrl.cm_to_mm(dist), deg, flag)


def grasp_brick():
    ctrl.lower_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.close_gripper_abs_position()
    ctrl.wait_for(1)
    ctrl.lower_gripper_reset_position()
    ctrl.wait_for(1)



def move_and_grasp_object(distance, angle):
    flag = ""
    if distance == 0 and angle ==0:
        return 0,0, flag
    ctrl.reset_position()

    if distance < DISTANCE_LIMIT_MM:
        [d, a, f] = move_to(distance, angle)
        print("BEH: I grasped the object! Oh yeah! ")
        flag = "grasped"
        grasp_brick()
    else:
        [d, a, f] = move_to((distance), angle)
        

    print("MC: Travelled for " + str(d)+ " cm and " + str(a)+ " degrees.")
    return (ctrl.cm_to_mm(d),a, flag)

"""
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
"""
