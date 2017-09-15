# ev3dev
import paho.mqtt.client as mqtt
import config
import ev3dev.ev3 as ev3
from sensors import publish_sensor_data, sensors, items_to_publish
#import time
import ev3dev.core as ev3core
from event_loop import EventLoop


# Endless loop that keeps sending all properties
client = mqtt.Client()
client.connect(config.BROKER_IP, config.BROKER_PORT, keepalive=60)

#Set IR sensor to remote control mode
sensors[0].mode = "IR-REMOTE"
sensors[1].mode = "IR-REMOTE"



ir = sensors[1]

"""
rc_motors = ev3core.RemoteControl(sensors[0],0)
rc_fingers = ev3core.RemoteControl(sensors[1],0)
rc_master = ev3core.RemoteControl(sensors[0],1)
rc_ctrl = [rc_motors,rc_fingers,rc_master]
rc_fingers.on_red_up = print("comms")
for rc in rc_ctrl:
    items_to_publish[rc] = []
    for member, dtype in rc.__class__.__dict__.items():
        if isinstance(dtype, property):
            items_to_publish[rc].append(member)
"""


buttons = [
    (ir.REMOTE.RED_UP, ir.REMOTE.RED_DOWN),
    (ir.REMOTE.BLUE_UP, ir.REMOTE.BLUE_DOWN),
]

def ir_changed(event):
    for channel in range(2):
        state = event.evaluation[channel]
        if state == ir.REMOTE.BAECON_MODE_ON:
            print("beacon")
#            loop.stop()
        for button in range(2):
            n = channel * 2 + button
            if state == buttons[button][0]:
                print("button0")
            elif state == buttons[button][1]:
                print("button1")
            else:
                print("button2")
    

loop = EventLoop()
loop.register_value_change(getter=lambda: ir.remote, 
                           startvalue=ir.remote,
                           target=ir_changed)
loop.start()


"""
counter = 0

while(1):
    # TODO: Implement receiving stop signal
    # TODO: Implement self restarting timer instead of while loop
    publish_sensor_data(client=client)
    print(sensors[0].num_values)
    counter += 1
    if counter % 10:
        print('still running... {}'.format(counter))
client.disconnect()

"""
