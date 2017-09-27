from Vision.vision_commands import publish_vision_info
from behaviours.box_detection.detect_chili import get_box_distance

def detect_box(params,image,client):

    box_idx = params["box_identifier"]
    
    boxes = get_box_distance(image)
    
    if (boxes!=[]):
       #Get target box details. "class_name" attribute must contain word "box"
       target_box = [i for i in boxes if (i[0]==box_idx)][0]
       print(target_box)
       publish_vision_info(client,topic="vision",info=target_box)  #check order of "info" contents, maybe extend target_box with None for UUID,class_name
       return 1
    else:
       print("No box found")
       return 0
        
    

