from Vision.vision_commands import publish_vision_info
from behaviours.box_detection.detect_chili import get_box_distance

def detect_box(params,image,client=None):

    box_idx = params["box_identifier"]
    
    boxes = get_box_distance(image)
    if (boxes!=[]):
       #Get target box details. "class_name" attribute must contain word "box"
       target_box = [i for i in boxes if (i[0]==box_idx)][0]
       print(target_box)
       if client==None:
          return target_box
       else:
          publish_vision_info(client,topic="vision",info=[target_box[0],target_box[1],target_box[2]])  #check order of "info" contents, maybe extend target_box with None for UUID,class_name
          return []
    else:
       target_box = ["no_box",0,0]
       if client!=None:
          publish_vision_info(client,topic="vision",info=target_box)
          return []
       else:
          return target_box
    

