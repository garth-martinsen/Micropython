from machine import Pin, ADC
import time
import TouchPin
''' This script reads the pin_to_test  up to the tp._cnt indicated. The user chooses at which cnts to touch the pin, starting after _cnt=25.
The plotter should be enabled to show the touches. Any adc count which falls outside of bounds (lb,ub) is a TOUCH.'''

pin_to_test = 7
times_to_read = 200
tp = TouchPin.TouchPin(pin_to_test)
while tp._cnt < times_to_read :
    adc = tp.read()
    if type(adc) != int:
        continue
    tp.handle_sample(adc)
    time.sleep(2)
    print("Stats: ", tp.stats())