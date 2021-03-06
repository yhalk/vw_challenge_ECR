import master
import time

class DummyDev:

    def __init__(self):
        self._channel = -1
        self._cmd = -1
        self._name = "test_obj"
        self._port = -1
        
    def print_hi(self,test=""):
        print("Hello object: "+test)
        
    def get_chn(self):
        return self._channel

    def set_chn(self,value):
        self._channel = value

    channel = property(get_chn,set_chn,'channel')

    def get_cmd(self):
        return self._cmd

    def set_cmd(self,value):
        self._cmd = value

    cmd = property(get_cmd,set_cmd,'cmd')
    
    def get_port(self):
        return self._port

    def set_port(self,value):
        self._port = value

    port = property(get_port,set_port,'port')
    
    
        
if __name__ == '__main__':
    from messages import *
    m = master.start_master('localhost')
    dum = DummyDev()
    dum.set_cmd(10)
    p = 2
    master.publish_cmd(m, AddDeviceMessage("test_obj", "DummyDev()"))

    """
    print("Going to sleep...")
    time.sleep(4)
    print("Wake up")

  
    master.publish_cmd(m, SetAttrMessage("test_obj", "cmd",repr(getattr(dum, "cmd"))))
    """
    print("Going to sleep...")
    time.sleep(4)
    print("Wake up")
    
    master.publish_cmd(m, ShowAttrMessage("test_obj", "port"))
    """
    print("Going to sleep...")
    time.sleep(4)
    print("Wake up")
    
    master.publish_cmd(m, RunMethodMessage("test_obj", "print_hi", {'test':'1'}))
    """
