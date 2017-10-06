import sys, serial
from serial.tools import list_ports

class IR_teensy(object):
	def __init__(self):
		self.ports = list(list_ports.comports()) # get all the connected serial devices
		print(len(self.ports))
		self.debug()
		#/dev/bus/usb/001/019
		#self.serial_port = serial.Serial('/dev/'+self.ports[0].name) # connect to the first
		self.serial_port = serial.Serial('/dev/bus/usb/001/020')

	def debug(self):
		'''
		   Use if cannot connect to the port
		   This function will print all found serial devices and prints the name and index of the port 
		'''
		print("finding ports")
		for i, item in enumerate(self.ports):
			print(i + ' : ' + item.name)

	def read(self):
		'''
		   Reads the current value from the teensy
		   Returns: 
		       Distance in cm
		'''

		measurement = self.serial_port.readline() # read the measurement
		
		measurement = measurement.decode('utf-8').split('\r') # change it to utf and split it on funny characters

		return measurement[0] # only return the actual measurment


if __name__ == '__main__':
	ir_sensor = IR_teensy()

	while True:
		
		print(ir_sensor.read())
