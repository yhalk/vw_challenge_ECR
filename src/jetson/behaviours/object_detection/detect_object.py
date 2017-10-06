from Vision.vision_commands import publish_vision_info,analyse_image

def detect_object(params,image,predictor,client=None):

    object_class = params #params["class"]  params==class now
    print(object_class)
    info = analyse_image(predictor,image)   
    required_ = [i for i in info if (i[0]==object_class)]  #Add checks for UUID
    print(required_)
    if required_!=[]:
          required_obj = required_[0]
          print("Should move for " + str(required_obj[1])+" and turn "+str(required_obj[2])+" for object "+required_obj[0])
          info = ["object_"+required_obj[0],required_obj[1],required_obj[2]]
          if client!=None:
             publish_vision_info(client,topic="vision",info=info)
             return []
          else:
             return info
    else:
       required_obj = ["bg",0,0]
       if client!=None:
          publish_vision_info(client,topic="vision",info=required_obj)
          return []
       else:
          return required_obj
    

