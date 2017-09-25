import os
import glob
import warnings
import re
import atexit


class NoSuchSensorError(Exception):

    def __init__(self, port, name=None):
        self.port = port
        self.name = name

    def __str__(self):
        return "No such sensor port=%d name=%s" % (self.port, self.name)

class Ev3StringType(object):

    @staticmethod
    def post_read(value):
        return value

    @staticmethod
    def pre_write(value):
        return value

class Ev3IntType(object):

    @staticmethod
    def post_read(value):
        return int(value)

    @staticmethod
    def pre_write(value):
        return str(value)


class create_ev3_property(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, cls):
        for name, args in self.kwargs.items():
            def ev3_property(name, read_only=False, write_only=False, flush_on_write=False, property_type=Ev3StringType):
                def fget(self):
                    if not write_only:
                        return property_type.post_read(self.read_value(name))
                    else:
                        return None

                def fset(self, value):
                    self.write_value(
                        name, property_type.pre_write(value), flush_on_write)
                return property(fget, None if read_only else fset)

            setattr(cls, name, ev3_property(name, **args))

        return cls


@create_ev3_property(
    bin_data={'read_only': True},
    bin_data_format={'read_only': True},
    decimals={'read_only': True},
    #mode={ 'read_only': False},
    fw_version={'read_only': True},
    modes={'read_only': True},
    name={'read_only': True},
    port_name={'read_only': True},
    uevent={'read_only': True},
    units={'read_only': True},
    value0={'read_only': True, 'property_type': Ev3IntType},
    value1={'read_only': True, 'property_type': Ev3IntType},
    value2={'read_only': True, 'property_type': Ev3IntType},
    value3={'read_only': True, 'property_type': Ev3IntType},
    value4={'read_only': True, 'property_type': Ev3IntType},
    value5={'read_only': True, 'property_type': Ev3IntType},
    value6={'read_only': True, 'property_type': Ev3IntType},
    value7={'read_only': True, 'property_type': Ev3IntType}
)


class LegoSensor():

    def __init__(self,port=-1,name=None):
        self.sys_path = ""

        sensor_existing = False
        if name != None and port == -1:
            for p in glob.glob('/sys/class/lego-sensor/sensor*/uevent'):
                with open(p) as f:
                    port_name = None
                    for value in f:
                        if (value.strip().lower().startswith('LEGO_ADDRESS=in'.lower())):
                            port_name = value.strip()[-1]
                            if sensor_existing:
                                break
                        if (value.strip().lower() == ('LEGO_DRIVER_NAME=' + name).lower()):
                            self.sys_path = os.path.dirname(p)
                            sensor_existing = True
                            if port_name is not None:
                                break
                    print(port_name)
                if sensor_existing:
                    self.port = int(port_name)
                    break
        """
        #FOR JETSON IR_control.py ONLY!
        if (not sensor_existing):
            raise NoSuchSensorError(port, name)
        """
        self._mode = self.read_value('mode')

    def read_value(self, name):
            attr_file = os.path.join(self.sys_path, name)
            if os.path.isfile(attr_file):
                with open(attr_file) as f:
                  value = f.read().strip()
                  return value
            else:
               return None

    def write_value(self, name, value, flush = False):
            attr_file = os.path.join(self.sys_path, name)
            if os.path.isfile(attr_file):
               with open(attr_file, 'w') as f:
                  f.write(str(value))
                  if flush:
                    f.flush()
            else:
               return

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if (self._mode != value):
            self._mode = value
            self.write_value('mode', value)

    def mode_force_flush(self, value):
        self._mode = value
        self.write_value('mode', value)



class InfraredSensor(LegoSensor):

    def __init__(self, port=-1):
        LegoSensor.__init__(self, port, name='lego-ev3-ir')
        self._channel = -1
        self._cmd = -1

    class REMOTE:

        """Button values for the `remote` property."""
        NONE = 0
        RED_UP = 1
        RED_DOWN = 2
        BLUE_UP = 3
        BLUE_DOWN = 4
        RED_UP_AND_BLUE_UP = 5
        RED_UP_AND_BLUE_DOWN = 6
        RED_DOWN_AND_BLUE_UP = 7
        RED_DOWN_AND_BLUE_DOWN = 8
        BAECON_MODE_ON = 9
        RED_UP_AND_RED_DOWN = 10
        BLUE_UP_AND_BLUE_DOWN = 11

     
    @property
    def remote(self):
        """IR remote control mode. A tuple of recieved value for each of the 4
        channels.
        """
        self.mode = 'IR-REMOTE'
        return self.value0, self.value1, self.value2, self.value3

    @property
    def prox(self):
        """Proximity mode. Distance in percent (100% is about 70cm)."""
        self.mode = 'IR-PROX'
        return self.value0

    
    def get_channel(self):
        return self._channel

    def set_channel(self,value):
        self._channel = value
   
    channel = property(get_channel,set_channel,'channel')

    def get_cmd(self):
        return self._cmd
    
    def set_cmd(self,value):
        self._cmd = value
      
    cmd = property(get_cmd,set_cmd,'cmd')



def get_IR_cmd(ir):

    ir_input = list(ir.remote)
    channel = [i for i, e in enumerate(ir_input) if e != 0]
    tup = (-2,-2)
    if channel==[]:
       tup = (0,-1)
    else:
       ir_command = ir_input[channel[0]]
       tup = (channel[0],ir_command)
    
    ir.set_channel(tup[0])
    ir.set_cmd(tup[1])
