from machine import Pin, ADC
import time
import TouchPin


tp = TouchPin.TouchPin(7)
while tp._cnt < 200:
    adc = tp.read()
    if type(adc) != int:
        continue
    tp.handle_sample(adc)
    time.sleep(2)
    print("Stats: ", tp.stats())