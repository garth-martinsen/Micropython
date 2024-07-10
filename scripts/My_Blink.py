#from time import sleep_ms
import time 
from machine import Pin

led=Pin(2,Pin.OUT) #create LED object from pin2,Set Pin2 to output
try:
    while True:
        led.value(1)        #Set led turn on
        print("LED: ", led.value())
        time.sleep_ms(1000)
        print("LED: ", led.value())
        led.value(0)        #Set led turn off
        print("MS: ",time.ticks_ms())
        print("LED: ", led.value())
        time.
        sleep_ms(1000)      #Hold for 1 second
        print("MS: ",time.ticks_ms())
        print("LED: ", led.value())

except:
    pass





