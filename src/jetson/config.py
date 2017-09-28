# NOTE: This config should be the same as the config on the ev3!

BROKER_IP = "10.180.225.154"  # This is the IP address of your Jetson, connected to EV3 (check with ifconfig)
BROKER_PORT = 1883


topics_to_listen = ["actuators","IR","odometry"]
qos_listen = [1,1,1]
topics_to_publish = ["vision"]
qos_pub = [2]

#Have behaviours taking a dictionary of param names:values and decompose them internally
behaviour_json = "behaviour.py"
params_json = "behaviour_param.py"
