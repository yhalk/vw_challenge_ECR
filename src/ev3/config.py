BROKER_IP = "10.180.225.154"  # This is the IP address of your Jetson, connected to EV3 (check with ifconfig)
BROKER_PORT = 1883

#Has to be in same order in actuators_simple.py, sensors.py
LARGE_MOTOR_A = "outA"
LARGE_MOTOR_B = "outB"
LARGE_MOTOR_D = "outD"
MEDIUM_MOTOR  = "outC"

topics_to_listen = ["vision"]
qos_listen = [0]
topics_to_publish = ["odometry"]
qos_pub = [0]

