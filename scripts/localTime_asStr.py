import time
import pyb

days= ["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
mo=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

epoc = time.gmtime(0)[0]
now = time.localtime()
print(now)

def dts(n):
   dtstr = days[n[6]+1] + "-"
   dtstr += str(n[0])
   dtstr += "-" +mo[n[1]-1]
   dtstr += "-" +str(n[2])
   dtstr += " T:" +str(n[3])
   dtstr += ":" +str(n[4])
   dtstr += ":" +str(n[5])
  
    # testing
   return dtstr