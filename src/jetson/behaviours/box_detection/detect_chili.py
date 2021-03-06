import cv2
import numpy as np
import chili_tag_detector as ctd
import sys
import time

from behaviours.box_detection.utils import calculate_angle_and_distance
#from utils import calculate_angle_and_distance
#1227^2 + 136^2 = sqrt(1524025) = 1309.83 1234.51
#900^2 +136^2 =  sqrt(828496) = 910.21 1004.99
#600^2 + 136^2 = sqrt(378496) = 615.22 623.26
def get_box_distance(frame):
    '''
        This function does the detection of chili tags. It expects the image as an argument and gives back all the tags that are detected.
        
        Arguments:
        frame - the image coming from the camera that is used to detect the chili tags from
        
        Returns:
        list in list with marker_id (cluster number), distance in mm and angle
    '''
#    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

#    ret, frame = cap.read()

    markers = ctd.detect(frame)

    height, width, channels = frame.shape
    marker_distances = []
    for marker in markers:
        marker_id = "box_" + str(marker[0])
        print(marker_id)
        marker_coor = marker[1]
        x2 = marker_coor[0][0]
        y1 = marker_coor[0][1]
        x1 = marker_coor[2][0]
        y2 = marker_coor[2][1]

        angle, distance = calculate_angle_and_distance(width,x1,x2,y1,y2)
        print("Angle " + str(angle) + " dist  " + str(distance)) 
        marker_distances.append([marker_id, distance, angle])

    return marker_distances

if __name__ == '__main__':
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert !  video/x-raw, format=(string)BGR ! appsink")

    ret, frame = cap.read()
    print(get_box_distance(frame))
