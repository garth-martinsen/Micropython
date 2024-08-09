import random

class smoother:
    def __init__( self, sz ):
        self._cap = sz + 5     # The number of measurements in meas will never exceed _cap
        self._sz = sz             # _sz is the number of measurements to be averaged, counting from last to first;
        self._meas = []           # _meas is Ordered List of measurements of length, lng, can get avg when  sz <= lng <= _cap
        self._thresh=-99
    
    def add_meas(self, m):
        self._meas.append(m)
        self.enforce_cap()
    
    def enforce_cap(self):
        lng = len(self._meas)
        if lng > self._cap:
            self._meas = self._meas[lng - self._cap:]
            print("Over Capacity limited to...: " ,self. _cap)
        if lng < self._sz:
            print("Need more samples...")
            
    def holds(self):
        return len(self._meas)
            
    def avg(self):
        ''' This method will return the  average the last _sz measurements'''
        lng=len(self._meas)
        if self._sz > lng:
            print("Not enough samples yet...")
            return -99
        return sum(self._meas[lng-self._sz:lng])/self._sz

    def std(self):
        avg = self.avg()
        sd = []
        for i in range(self._sz):
            sd.append((self._meas[i]-avg)**2)
        return sum(sd)/self._sz
    
    def thresh(self):
        self._thresh = self.avg() - 3 * self.std()
        return self._thresh
        
    def createMeas(self, n_samples, low, high):
        for i in range(n_samples):
            self.add_meas( random.randrange(low*10, high*10)/10)

 #usage: create smoother, sm,  with sz to be averaged; feed measurements in until lgn > sz; request avg
sm = smoother(10)
sm.createMeas(21,3,6)  # for simulation, sample size must be > sz
print("measurements: " , sm._meas)
print("Avg: ",sm.avg())
print("std: ", sm.std())
print("threshold: ", sm.thresh())  # subtract 3 * sd from mean to get threshold. if sample < thresh,  indicates a touch


#TODO: plug this into a test with real touch readings in lieu of createMeas and use the thresh to determine if a touch has occurred on a pin.