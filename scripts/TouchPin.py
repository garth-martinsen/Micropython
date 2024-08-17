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

    def __init__(self, id, sb):
        self._id = id
        self._pin = ADC(Pin(id))
        self._lb= 7000
        self._ub=4000
        self._delta = 0
        self._adc = 0
        self._state = CALIB
        self._cnt =0
        self._smooth_sz=sb
        self._samples =[]
        self._variants = []
        
    
    def read(self):
        time.sleep(1)
        adc = self._pin.read_u16()
        self.handle_sample(adc)
        
    def smooth(self, n, adc):
        '''averages over the last n samples'''
        self._samples.append(adc)
        if len(self._samples) > n:
            self._samples.pop(0)                                       #when list holds 1 more than _smooth_sz, remove the first element to keep the list size at _smooth_sz
        mean = sum(self._samples)/len(self._samples)
        # if less than 2 samples then just assign sd=250; guess!
        sd=   250
        self._variants.append((mean -adc)*(mean-adc))
        if len(self._variants) > n:
            self._variants.pop(0)                                       #when list holds 1 more than _smooth_sz, remove the first element to keep the list size at _smooth_sz
        if len(self._variants) > 2:
            sd = math.sqrt(sum(self._variants)/(len(self._variants) -1))
                
        return math.floor(mean), math.floor(sd)           # return as truncated ints because adc counts are ints.
                
    def handle_sample(self, adc):
        '''Samples are handled in one of  two states: {CALIBRATE, DETECT}. The state transistions from CALIBRATE-> DETECT when count >_smooth_sz'''
        self._adc = adc
      
        if type(adc) != int:
            print("Type: ", type(adc))
            return
        if self._cnt < self._smooth_sz:
            self._state = CALIB
            self.calibrate(adc)
        else:
            self._state = DETECT
            self.detect(adc)
      
 
    def calibrate(self, adc):
        ''' Calibration is complete when sample size > _smooth_sz , and also after _cnt > _smooth_sz,  for samples within bounds (ie: NON-TOUCH samples)  '''
        self._cnt +=1
       
        if self._cnt >2:
            mean, sd = self.smooth(self._smooth_sz, adc)
            self._lb  = math.floor(mean - 3.5* sd)                                             #bounds: samples > abs(mean +- 3.5 sd) , will be branded as TOUCHes
            self._ub = math.floor(mean + 3.5 * sd)
            print("id-cnt-adc-mean-lb-ub: ", self._id, sep, self._cnt, sep, self._adc,sep, mean, sep, self._lb, sep, self._ub)

       
    def detect(self, adc):
        ''' bounds are at mean -x*sd and mean+x*sd, where x is chosen by user from inspection (eg: 1.3).
    If bounds are exceeded, it is a TOUCH. Observation shows that a 65535 or a zero could trigger
        a TOUCH so testing for anything outside of the bounds works well... No false TOUCHES'''
        mean = math.floor(sum(self._samples)/len(self._samples))
        if adc < self._lb or adc > self._ub:
            print("     Touch!:  id-cnt-adc-mean-lb-ub: ", self._id, sep, self._cnt, sep, self._adc, sep, mean, sep, self._lb, sep, self._ub)       #do not pass adc to calibrate(). It is an outlier
        else: 
            self.calibrate(adc)        # not a TOUCH, so use adc to improve estimation of thresh
        
    def createMeas(self, n_samples, low, high):
        '''This is for testing only. it will generate samples between low and high'''
        for i in range(n_samples):
            self.handle_sample( random.randrange(low*1000, high*1000)/10)

    def stats(self):
        ''' statistics are all truncated to ints as adc counts cannot be floats'''
        print("pin: ", self._id)
        print("Count", self._cnt )
        print("Mean: ", math.floor(sum(self._samples) /len(self._samples)))
        print("Std Dev: ", math.floor(math.sqrt(  sum(self._variants)/len(self._variants  ) )))
        print("LowerBound: ", self._lb)
        print("UpperBound: ", self._ub)
              

