class DataCollector():

     def __init__(self):
         self._motA = None
         self._motB = None
         self._motC = None
         self._motD = None
         self._time = None



     def get_data(self):
         return self._motA,self._motB,self._motC,self._motD,self._time

     def set_data(self,a,b,grip,lift,time):
         self._motA = a
         self._motB = b
         self._motC = grip
         self._motD = lift
         self._time = time

     data = property(get_data,set_data,'data')
