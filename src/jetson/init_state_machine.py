#! /usr/bin/python
from behaviours.object_detection.detect_object import detect_object
from Vision.vision_commands import publish_vision_info,analyse_image
from behaviours.box_detection.detect_chili import get_box_distance
from behaviours.box_detection.detect_box import detect_box
import time 
from Vision.vision_commands import grab_camera_image
import subprocess
import os

state = "explore"


def write_ssh_file_command():
    cmd = "sshpass -p maker ssh robot@10.42.0.214 touch /home/robot/DLRC/vw_challenge_ECR/src/ev3/vision/vision_flag"
    return cmd


def move_to_explore(client,dst,angle,listening):    #DST, ANGLE VALUES FOR EXPLORATION ???
    print(dst,angle)
    publish_vision_info(client,topic="vision",info=["explore",dst,angle])
    while (getattr(listening['Odometer'],'moved')!="1"):
              print("explore read and sleep")
              time.sleep(1)
    print("explore sleep")
    time.sleep(10)


def look_for_object(params,camera,predictor):
    # read from vision for new object results
    # if seen return 1 [new dist, angle]
    # else message for turning around and moving forward
    """
      return class,dst,angle but NO PUBLISH
    """
    print("look object")
    image = grab_camera_image(camera)
    object_class,dst,angle = detect_object(params,image,predictor)
    print(object_class,dst,angle)
    if object_class=="bg":
       return 0,dst,angle,object_class

    return 1,dst,angle,object_class


def go_to_object(object_class,dst,angle,client,listening):
    # message to move towards object
    # read feedback
    # if it is not grasped, return 0
    # if grasped return 1
    """  
       PUBLISH class,dst,angle
       WAIT until robot has moved the percentage of the dst 
       CHECK if robot close enough to grasp      

    """
    print("go object")
    publish_vision_info(client,topic="vision",info=[object_class,dst,angle])
    while (getattr(listening['Odometer'],'moved')!="1"):
              print("go to object read and sleep")
              time.sleep(1)
    
    grasp = getattr(listening['Odometer'],'grasp')  #MAKE SURE TO WAIT UNITL UPDATED
    
    return grasp


def look_for_box(params,camera):
    # read from vision for new object results
    # if seen return 1 [new dist, angle]
    # else message for turning around and moving forward
    """
       return "box_IDX",dst,angle
       NO PUBLISH

    """
    print("look box")
    image = grab_camera_image(camera)
    box_spot,dst,angle = detect_box(params,image)    ##WHICH BOX DO WE GO TO?? - ADD CLUSTERING
    if box_spot=="no_box":
       return 0,dst,angle,box_spot
 
    return 1,dst,angle,box_spot


def go_to_box(box,dst,angle,client,listening):
    # message to move towards box
    # read feedback
    # if it is not release, return 0
    # if released return 1
    """  
       PUBLISH class,dst,angle
       WAIT until robot has moved the percentage of the dst 
       CHECK if robot close enough to grasp      

    """
    print("go box")
    publish_vision_info(client,topic="vision",info=[box,dst,angle])
    while (getattr(listening['Odometer'],'moved')!="1"):
              print("go to box read and sleep")
              time.sleep(1)
     
    grasp = getattr(listening['Odometer'],'grasp')   # MAKE SURE YOU WAIT UNTIL IT S UPDATED
 
    return grasp


def run_state_machine(obj,box_id,camera,predictor,client,listening,dst=0.0,angle=0.0,DST_EXPLORE=0.0,ANGLE_EXPLORE=0.0):
    global state
    #time.sleep(10)
    if state == "explore":
        object_seen,dst,angle,object_class = look_for_object(obj,camera,predictor)  
        if object_seen:
            cmd = write_ssh_file_command()
            os.system(cmd)
            state = "explore"
        #else: 
            #move_to_explore(client,dst=DST_EXPLORE,angle=ANGLE_EXPLORE,listening=listening)
    elif state == "locate_obj":
        object_grasped = go_to_object(obj,dst,angle,client,listening)  
        if object_grasped=="grasped":
            state = "locate_box"
        else:
            state = "explore"
    elif state == "locate_box":
        box_seen,dst,angle,box_ident = look_for_box(box_id,camera)
        if box_seen:
            state = "go_to_box"
        else:
            move_to_explore(client,dst=DST_EXPLORE,angle=ANGLE_EXPLORE,listening=listening)
    elif state == "go_to_box":
        object_released = go_to_box(box_ident,dst,angle,client,listening)
        if object_released=="release":
            state = "explore"
        else:
            state = "locate_box"
    print("state machine")
    print(dst,angle)
    return dst,angle 
