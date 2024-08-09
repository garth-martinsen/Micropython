import micropython
import gc


print("MEM: ")
print(micropython.mem_info())
print("QSTR: ")
print( micropython.qstr_info())

wkdys = micropython.const(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
mos = micropython.const(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
# todo gate= micropython.const(Gate = namedtuple("Gate",("dts","cmd","state","actor","stpTempC","dcmTempC","volts","amps","bat%"))) needs work
print("QSTR: ", micropython.qstr_info())

# Memory functions
gc.enable()
allocated = gc.mem_alloc()
free = gc.mem_free()
collect = gc.collect()
gc.disable()

print("Allocated: ",allocated)
print("Free: ",free)
total = allocated + free
print("Total Heap bytes: ",total)
print("Heap used% : ", allocated/free *100)
print("collected: ", collect)
print("Globals: ", globals())