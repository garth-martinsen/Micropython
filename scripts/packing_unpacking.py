from struct import *

from collections import namedtuple
from machine import RTC
from micropython import const

# import /Users/garth/Programming/MicroPython/scripts/datetime
import os
import sys

#demonstrates how to pack the Gate tuple into bytes for transmission via BLE and
#also how to unpack it on both sides of the Client Server .
#Note that two tuples can be joined using the + operator wg=now+gs. Then could
#load the Gate named tuple using wg[0:16]
# Both packing , sizing and unpacking require the fmt string which is defined. See Format Characters at: https://docs.python.org/3/library/struct.html
# Best fmt: use: 'H6Bi3B4fB' because when packed is is only 33 bytes.


fmt= const('H6BI3B4fB')  # 1 u_short, 6 ushort, 1 u_int, 3 u_char, 4 float, 1u_short

print("Endian: ", sys.byteorder)

now = RTC().datetime()
print("now: ", now)
gs=(1,1,2,25.6,25.9,12.6,1.0003,95)  #tuple representing the gate state namedtuple "Gate" below.
wg=now+gs    # joins the two tuples into one.
print("dts + gate: ", wg)

Gate = namedtuple("Gate", ("year","month", "day", "wkd", "hour", "min",
                  "second", "fract", "cmd","actor","state","temp_stp",
                  "temp_dcm","volts","amps","bat_lvl"))
gate = Gate(now[0],now[1],now[2],now[3],now[4],now[5],now[6],now[7],1,1,2,25.6,25.9,12.6,1.0003,95)

print("gate namedtuple: ", gate)


#this packs the values as bytearray IAW format fmt ('H6BI3B4fB')
packed = pack(fmt, gate.year,gate.month,gate.day,gate.wkd,
                     gate.hour,gate.min, gate.second, gate.fract, gate.cmd,
                     gate.actor, gate.state, gate.temp_stp, gate.temp_dcm,
                     gate.volts, gate.amps, gate.bat_lvl)
print("packed bytes: ", packed)


sz = calcsize(fmt)  # Note that length in bytes depends on the fmt string used to pack

print("Size of packed bytes: ", sz)

#this upacks the  bytearray into a tuple IAW format  fmt ('H6BI3B4fB'). 
t= unpack(fmt, packed)
print("unpacked: ", t)

