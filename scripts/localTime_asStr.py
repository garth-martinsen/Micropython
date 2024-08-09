import time
import machine


days= ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
mo=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

epoc = time.gmtime(0)[0]
print("Epoc: ",epoc)
#now = time.localtime()
now = machine.RTC().datetime()
print("RTC datetime:  ",now)

def dts(n):
   dtstr = days[n[3] ] + "-"     #wkday
   dtstr += str(n[0])			 #year
   dtstr += "-" +mo[n[1]-1]		 #month
   dtstr += "-" +str(n[2])       #day
   dtstr += " " +str(n[4])       #hour
   dtstr += ":" +str(n[5])       #min
   dtstr += ":" +str(n[6])       #sec
   dtstr += "." +str(n[7])       #fraction of second
    # testing
   return dtstr

print("DST String: ", dts(now))
print("Milliseconds: ", time.ticks_ms())