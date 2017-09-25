import ev3control.master as master
import frcnn
import cv2

class VisualFeedback():

    def __init__(self):
        self._distance = None
        self._angle = None


    def get_distance(self):
        return self._distance

    def set_distance(self,value):
        self._distance = value

    distance = property(get_distance,set_distance,'distance')

    
    def get_angle(self):
        return self._angle

    def set_angle(self,value):
        self._angle = value

    angle = property(get_angle,set_angle,'angle')



def addVisionDevices(client,topic,qos=2):
    
    master.publish_cmd(client, topic, AddDeviceMessage('Vision', "VisualFeedback()"),delay=1,qos=qos)

def get_bbox(key_tuple):

    return key_tuple[1]

def get_distance(key_tuple):

    return key_tuple[2]

def get_angle(key_tuple):

    return key_tuple[3]



def analyse_image(predictor,img):

    ret_val = predictor.detect_known_objects(img)
    bbox = get_bbox(ret_val[0])  # Get first detected object,  change later???
    distance = get_distance(ret_val[0])
    angle = get_angle(ret_val[0])

    info = (bbox,distance,angle)

    return info
 

def publish_vision_info(client,topic,info):
#Use same device name as in vision_commands.py

    master.publish_cmd(client,topic, SetAttrMessage('Vision','distance',str(info[1])),qos=0) #do we care about quality of service here??? probably not,want speed
    master.publish_cmd(client,topic, SetAttrMessage('Vision','angle',str(info[2])),qos=0)

def save_image(img_name,img,info):

    bbox = info[0]
    (real_x1, real_y1, real_x2, real_y2) = bbox
    cv2.rectangle(img,(real_x1, real_y1), (real_x2, real_y2), (0,0,255),5)
    cv2.imwrite(img_name,img)


def see_and_tell(predictor,client,topic,img, img_name="./test_see_tell.jpg"):

    info = analyse_image(predictor,img)
    publish_vision_info(client,topic,info)
    save_image(img_name,img,info)
