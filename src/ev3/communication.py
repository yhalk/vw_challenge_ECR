from functools import partial
import paho.mqtt.client as mqtt
import config as config
import json
from Sensors.sensors import publishable_names_dict, items_to_publish, addSensorDevices
import ev3control.master as master
import ev3control.slave as slave
from ev3control.messages import *
from MotionCtrl.actuators_simple import addActuatorDevices
from Sensors.odometry_ev3 import addOdometryDevices

def get_behaviours_and_params(behaviour_json, params_json):

    #Get {behaviour name: behavior function name} dictionary
    with open(behaviour_json) as beh:
         behaviours = json.load(beh)

    #Get {behaviour name: {param name:value} } dictionary. Order of params should be same as passing order
    with open(params_json) as params:
         params = json.load(params)

    return behaviours,params

         
def on_log(client, userdata, level, buf):
   print("Jetson log: ",buf)

def comm_init(topics_to_listen=[], qos_listen=None, topics_to_publish=[] ,qos_pub=None, listening=None, log=1):

   listening = {}
   #Set up client to receive sensor values and send actuator commands
   client = mqtt.Client()
   client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
   client.on_message = partial(slave.process_message, listening)
   #Subscribe to topics we get values from
   for top in range(len(topics_to_listen)):
      client.subscribe(topics_to_listen[top],qos=qos_listen[top])            
   #Subscribe to topics we send values to
   for top in range(len(topics_to_publish)):
      if topics_to_publish[top]=="IR":
         addSensorDevices(client,topics_to_publish[top],qos=qos_pub[top])
      elif topics_to_publish[top]=="actuators":
         addActuatorDevices(client,topics_to_publish[top],qos=qos_pub[top])
      elif topics_to_publish[top]=="odometry":
         addOdometryDevices(client,topics_to_publish[top],qos=qos_pub[top])

   if log==1:
      client.on_log = on_log
 
   return client,listening


def  publish_all(client,config_topics_to_publish):

     for topic in config_topics_to_publish:
         if topic=="IR":
            sensor = "IR_control"
            for property_name in items_to_publish[sensor]:
                prop = getattr(publishable_names_dict["IR_control"],property_name)
                master.publish_cmd(client,topic,SetAttrMessage(sensor, property_name, str(prop)))
         elif topic=="actuators":
             for pub, property_names in items_to_publish.items():
                 for property_name in property_names:
                     val = getattr(publishable_names_dict[pub],property_name)
                     master.publish_cmd(client,topic,SetAttrMessage(pub, property_name, repr(val)))
