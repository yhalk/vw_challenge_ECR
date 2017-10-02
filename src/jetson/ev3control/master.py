"""Master Client implementation."""
import time
import paho.mqtt.client as mqtt

from .messages import *


def start_master(host):
    """Start MQTT client with setup that makes it a master."""
    client = mqtt.Client()
    client.connect(host, 1883, keepalive=60)
    return client


def publish_cmd(client, topic, message, delay=.2, qos=0):
    """Convenience wrapper around MQTT's publish method.

    :message: should be one of the types defined in messages.py
    """
    sts,mid = client.publish(topic=topic, payload=repr(message),qos=qos)
    # If we chain multiple publish commands, we need delays between them
    time.sleep(delay)
    return mid

if __name__ == '__main__':
    from messages import *
    host = "localhost"
    m = start_master(host)
    publish_cmd(m, ShowAttrMessage("test", "max_speed"))
