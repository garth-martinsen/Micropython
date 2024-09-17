'''Max4080 Current Sensor: 0-20 Amp . ADC output is a voltage measurement across the Rshunt = 0.1Ω. ADC resolution is: _?__ So Current=Vshunt/Rshunt.'''
import machine

class GJM_MAX4080:
    def __init__(self, pin,atten,conversion,vref):
         self._pin=machine.Pin(pin)
         self._adc=machine.ADC(self._pin)
         self._adc.atten(atten)
         self._conversion=conversion   #until I investigate resolution
         self._vref = vref

    def read_shunt(self):
        count = self._adc.read_u16();
        zeroed = pow(2,15)
        return  count
        
'''Usage: 
  max = GJM_MAX4080(15,3,1 )
  print(max.read_u16())
   '''
                     