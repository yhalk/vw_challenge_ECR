from ev3dev_online import LegoSensor

class InfraredSensor(LegoSensor):

    def __init__(self, port=-1):
        LegoSensor.__init__(self, port, name='lego-ev3-ir')

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


