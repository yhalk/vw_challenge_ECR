# ev3dev
import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
from sensors import publish_sensor_data, sensors, items_to_publish
import ev3dev.core as ev3core

def get_IR_cmd(ir_remote):

    ir_input = list(ir_remote)
    channel = [i for i, e in enumerate(ir_input) if e != 0]
    if channel==[]:
       return (-1,-1)
    else:
       ir_command = ir_input[channel[0]]
       return (channel[0],ir_command)

    return (-2,-2)

# Endless loop that keeps sending all properties
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)

#Set IR sensor to remote control mode
ir = sensors[0]
ir.mode = "IR-REMOTE"

counter = 0
while(1):
    tup = get_IR_cmd(ir.remote)
    print(tup)
    #publish_sensor_data(client=client)
    #receive_actuator_properties(client=client)
    counter += 1
    if counter % 10:
        print('still running... {}'.format(counter))
client.disconnect()

