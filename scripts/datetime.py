from machine import RTC
# This script will get the datetime from the RTC and express it as a string.
#todo: Learn how to use QSTR to save memory on wkdays and mo.

wkdays=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
mo=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def dts_string(tpl):
    dtstr= wkdays[tpl[3]]+"-"
    dtstr += mo[tpl[1]] + "-"
    dtstr += str(tpl[2]) + "-"
    dtstr += str(tpl[0])+" "
    dtstr += str(tpl[4])+":"
    dtstr += str(tpl[5])+":"
    dtstr += str(tpl[6])+"."
    dtstr += str(tpl[7])
    return dtstr


def get_date_time_as_string():
    '''Formats date time as a string: eg:  '''
    return dts_string(get_date_time_as_tuple())

    
 def get_date_time_as_tuple():
     '''Returns the datatime as a 7-tuple'''
     return RTC().datetime()
        