from time import sleep
from machine import Pin, PWM
import math

DUTY_MAX = 2**16 - 1

duty_u16 = 0
delta_d = 656  # ~100 steps between 0 and 2**16 -1



p = PWM(Pin(5), 1000, duty_u16=duty_u16)
print(p)

while True:
    p.duty_u16(duty_u16)

    #sleep(1 / 1000)
    sleep(1)
    duty_u16 += delta_d
    print("DutyCycle %: ", duty_u16*100/DUTY_MAX)
    if duty_u16 >= DUTY_MAX:
        duty_u16 = DUTY_MAX
        delta_d = -delta_d
    elif duty_u16 <= 0:
        duty_u16 = 0
        delta_d = -delta_d