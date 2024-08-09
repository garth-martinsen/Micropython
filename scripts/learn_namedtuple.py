from collections import namedtuple
import time
from machine import RTC

#learn to create, load, get values as tuple and create using *.make

days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] # day 0 is Mon
#DTS_Tuple = namedtuple("DTS_TUPLE",("year","month","day","wkd","hour","minutes","seconds","dayOfWeek"))
# MyTuple = namedtuple("MyTuple",("x","y","z"))
# lst = []
# lst.append(MyTuple(3,4,7))
# lst.append(MyTuple(5,8,15))
# #now = list(time.localtime())
# rtc=RTC()
# now = rtc.datetime()
# print(no
# DTS = DTS_Tuple(list(now))
# GateState = namedtuple("GateState",("dts","cmd","state","actor","stpTempC","dcmTempC","volts","amps","bat%"))
# states=[]
# states.append(GateState(now[:-1],1,2,1,25.6,27.8,12.56,1.0045,98))
# states
# dts=states[0].dts
# print("day: ",dts[int(days[5]]))
# see localtime_asStr.py for conversion to string. method: def dts(n)
#end

rtc=RTC()
now = rtc.datetime()
print("Fields for now: ", now)
GateState = namedtuple("GateState",("year","month","day","wkdy", "hour","minutes","seconds","fract","cmd","state","actor","stpTempC","dcmTempC","volts","amps","bat%"))
gte = 1,2,1,25.6,27.8,12.56,1.0045,98
state= now + gte
print("Type of state: ", type(state))
print("state with dts:", state)
print("GateState namedtuple: ",GateState)
# instantiating a gate_state using state
gs =GateState(2024, 7, 6, 5, 12, 8, 46, 473989, 1, 2, 1, 25.6, 27.8, 12.56, 1.0045, 98)


print("namedtuple of gs: ", gs)




