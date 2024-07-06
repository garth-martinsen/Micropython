from collections import namedtuple
import time

days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] # day 0 is Mon
DTS_Tuple = namedtuple("DTS_TUPLE",("year","month","day","hour","minutes","seconds","dayOfWeek"))
MyTuple = namedtuple("MyTuple",("x","y","z"))
lst = []
lst.append(MyTuple(3,4,7))
lst.append(MyTuple(5,8,15))
now = list(time.localtime())
#DTS = DTS_Tuple(list(now))
GateState = namedtuple("GateState",("dts","cmd","state","actor","stpTempC","dcmTempC","volts","amps","bat%"))
states=[]
states.append(GateState(now[:-1],1,2,1,25.6,27.8,12.56,1.0045,98))
states
dts=states[0].dts
print("day: ",days[dts[6]])


# see localtime_asStr.py for conversion to string. method: def dts(n)
#end

