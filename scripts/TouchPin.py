from machine import Pin, ADC
from micropython import const
import random
import math
import time

#TODO: Create an app that instantiates each of the active TouchPins.
# Run it from actual measurements, with time to calibrate, and count true and false Touches.
# Active TouchPins: [ 2,3,6,7,8,9,10,11,12,13,14]  count=11
CALIB = const(0)
DETECT = const(1)
states= [ CALIB, DETECT ]
sep = const(", ")

class TouchPin:
    ''' A TouchPin is sensitive to touch by human. A touch causes the adc count to change radically.
    Two states are used: CALIBRATE , DETECT. During CALIBRATE, all samples are used to establish bounds ( lb, ub).
    During DETECT state, any adc outside of bounds (lb,ub) is a TOUCH, any adc which is in bounds  goes to calibrate() to improve bounds.
    State transitions from  CALIBRATE -> DETECT  when sample count is greater than 25. '''

    def __init__(self, id):
        self._id = id
        self._pin = ADC(Pin(id))
        self._lb= 7000
        self._ub=4000
        self._delta = 0
        self._adc = 0
        self._state = CALIB
        self._cnt =0
        self._sum_samples =2000
        self._sum_variants = 0
        
    
    def read(self):
        time.sleep(1)
        adc = self._pin.read_u16()
        self.handle_sample(adc)
        
        
    def handle_sample(self, adc):
        '''Samples are handled in one of  two states: {CALIBRATE, DETECT}. The state transistions from CALIBRATE-> DETECT when count >25.'''
        self._adc = adc
      
        if type(adc) != int:
            print("Type: ", type(adc))
            return
        if self._cnt < 25:
            self._state = CALIB
            self.calibrate(adc)
        else:
            self._state = DETECT
            self.detect(adc)
        
    def calibrate(self, adc):
        ''' Calibration is done until sample size > 25, and also for NON-TOUCH, bounded measurements, after sample size > 25'''
        self._cnt +=1
        if self._cnt >2:
            mean= self._sum_samples / self._cnt
            sd = math.sqrt(self._sum_variants/(self._cnt -1))
            self._lb  = mean - 0.9* sd
            self._ub = mean + 0.9 * sd
            self._sum_samples += adc
            self._sum_variants += (mean-adc)**2
         
            print("id-cnt-adc-mean-lb-ub: ", self._id, sep, self._cnt, sep, self._adc,sep, mean, sep, self._lb, sep, self._ub)

       
    def detect(self, adc):
        ''' bounds are at mean -2*sd and mean+2*sd. If bounds are exceeded,  it is a TOUCH. Observation shows that a 65535 or a zero could trigger
a TOUCH so testing for anything outside of the bounds works well... No false TOUCHES'''
        mean = self._sum_samples/self._cnt
        if adc < self._lb or adc > self._ub:
            print("     Touch!:  id-cnt-adc-mean-lb-ub: ", self._id, sep, self._cnt, sep, self._adc, sep, mean, sep, self._lb, sep, self._ub)       #do not pass adc to calibrate(). It is an outlier
        else: 
            self.calibrate(adc)        # not a TOUCH, so use adc to improve estimation of thresh
 
              
      
           
            
    def createMeas(self, n_samples, low, high):
        '''This is for testing only. it will generate samples between low and high'''
        for i in range(n_samples):
            self.handle_sample( random.randrange(low*1000, high*1000)/10)

    def stats(self):
        print("id: ", self._id)
        print("Count", self._cnt )
        print("Mean: ", self._sum_samples /self._cnt)
        print("Std Dev: ", math.sqrt(self._sum_variants/(self._cnt-1)))
        print("LowerBound: ", self._lb)
        print("UpperBound: ", self._ub)
              

