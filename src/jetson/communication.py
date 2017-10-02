from Vision.vision_commands import addVisionDevices
from functools import partial
import paho.mqtt.client as mqtt
import config as config
import json
import ev3control.slave as slave
import time 

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


def on_publish(client,userdata,mid):
    print(str(mid)+" delivered")


def comm_init(topics_to_listen=[], qos_listen=None, topics_to_publish=[] ,qos_pub=None, listening=None, log=1):

   listening = {}
   #Set up client to receive sensor values and send actuator commands
   client = mqtt.Client()
   client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)
   client.on_message = partial(slave.process_message, listening)
   #client.on_publish = on_publish
   #Subscribe to topics we get values from
   for top in range(len(topics_to_listen)):
         client.subscribe(topics_to_listen[top],qos=qos_listen[top])            
   #Subscribe to topics we send values to
   for top in range(len(topics_to_publish)):
         if topics_to_publish[top]=="vision":
            addVisionDevices(client,topics_to_publish[top],qos=qos_pub[top])
   while (listening=={}):
         print("Waiting to connect...")
         for top in range(len(topics_to_publish)):
             if topics_to_publish[top]=="vision":
                addVisionDevices(client,topics_to_publish[top],qos=qos_pub[top])
         client.loop()
         time.sleep(1)

   if log==1:
      client.on_log = on_log

   return client,listening
