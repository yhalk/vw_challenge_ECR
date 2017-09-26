from Vision.vision_commands import publish_vision_info
from behaviours.box_detection import get_box_distance

def detect_box(params,image,client):

    box_idx = params["box_identifier"]
    
    boxes = get_box_distance(image)

    if (boxes!=[]):
       #Get target box details
       target_box = [i for i in boxes if (i[0]==box_idx)]
       dst = target_box[2]
       publish_vision_info(client,topic="Vision",info=target_box)  #check order of "info" contents, maybe extend target_box with None for UUID,class_name
       return 1
    else:
       print("No box found")
       return 0
        
    

