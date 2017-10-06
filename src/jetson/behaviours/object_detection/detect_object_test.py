from Vision.vision_commands import publish_vision_info
from behaviours.box_detection.detect_chili import get_box_distance

import sys
sys.path.insert(0, '/home/nvidia/vision/')

import temp

def detect_object(params,image,client):

    box_idx = params["box_identifier"]
    
    boxes = single_predition(): 
    if (boxes!=[]):
       #Get target box details. "class_name" attribute must contain word "box"
       target_box = ["box", boxes[0][1], boxes[0][2]]
       publish_vision_info(client,topic="vision",info=target_box)  #check order of "info" contents, maybe extend target_box with None for UUID,class_name
    else:
       target_box = ["no_box",0,0]
       publish_vision_info(client,topic="vision",info=target_box)
        
    

