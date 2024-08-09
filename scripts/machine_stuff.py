import machine

print("Machine freq HZ: ", machine.freq())
rtc = machine.RTC()
print("DateTime from RTC: ", rtc.datetime())