import sys
import os
import machine
import time
import struct

print(sys.implementation)

print("Micro Python Version: ", sys.version)

rtc = machine.RTC()
