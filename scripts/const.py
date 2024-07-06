import micropython


print("MEM: ")
print(micropython.mem_info())
print("QSTR: ")
print( micropython.qstr_info())

wkdys = micropython.const(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
mos = micropython.const(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
# todo gate= micropython.const(Gate = namedtuple("Gate",("dts","cmd","state","actor","stpTempC","dcmTempC","volts","amps","bat%"))) needs work
print("QSTR: ", micropython.qstr_info())