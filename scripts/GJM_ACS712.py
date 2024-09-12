'''This Module implements the ACS712 Hall Effect Current sensor. The sensed current is limited to ±20 Amps and is
ratiometric with the hall voltage at sensitivity of ~100mV/Amp. Two control gpio pins: Bus Voltage  and Hall Voltage'''
from machine import Pin, ADC, RTC
import GJM_DateTime 

wkdays=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
mo=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


class GJM_ACS712:
    def __init__(self, bus_gpio, hall_gpio, vcc ):
        self._rtc = RTC()
        self._vcc = vcc
        self._badc = ADC(Pin(bus_gpio))       # adc on bus voltage pin 
        self._badc.init()
        self._hadc = ADC(Pin(hall_gpio))      # adc on hall voltage pin 
        self._hadc.init()
        self._sensitivity = 10  #1/100mV/Amp =1/0.1
        self._mid= 32768
       
        # Initialize to zero; Set later from sensor readings and computations.
        self._bvolts = 0.0
        self._hvolts = 0.0
        self._current_amps = 0.0
        self._power_watts = 0.0
        
        
    def header(self):
         # header for print out of state:
         header =  f"                       datetime                                        Bus Volts   Hall Volts   Current Amps  Power Watts"  
         print(header )
        
    def read_sensors(self):
        self._badc.init()
        self._hadc.init()
        self._hvolts = self._hadc.read_u16()*61e-6          # counts * LSB
        self._bvolts = self._badc.read_u16()* 244e-6      # counts * LSB
        self.compute_current()
        self.compute_power()
  
    def datetimestr(self):
        dts=self._rtc.datetime()
        return f"{wkdays[dts[3]]} {mo[dts[1]-1]} {dts[2]}, {dts[0]} T:{dts[4]}:{dts[5]}:{dts[6]}.{dts[7]} PDT"
    
    def compute_current(self):
        '''Given : - 20A <current< 20A and 100mV/Amp , sensor fsc is -2V < hall_volts < 2V. FSR = 4 Volts, so hall_LSB= 4/(pow(2,16-1)=61e-6V/lsb'''
        self._current_amps = (self._vcc/2 + self._hvolts) * self._sensitivity  # multiplying by 10 is same as dividing by 0.1
    
        
    def compute_power(self):
        self._power_watts = self._bvolts * self._current_amps
    
                        
    def show_measurements(self):
        self.header()
        print( self.datetimestr(), ",  ",self._bvolts,",  ", self._hvolts, ",  ", self._current_amps, ",  ", self._power_watts )
    

    
        
        