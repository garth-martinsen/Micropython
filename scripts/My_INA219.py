'''Testing of the INA219 Current Sensor. 3.2 Amps'''
#TODO: See if there is a library in µpython for INA219 device. untangle the circuitpython and µpython stuff. replaced adafruit import with: from machine import SoftI2C as SI2C


#TODO: untangle all of the adafruit import and logging import   File "/lib/Adafruit_GPIO/__init__.py", line 1, in <module> ImportError: no module named '__future__' 
import logging
from machine import SoftI2C as SI2C
from machine import Pin
import errno
from INA219 import INA219

def show_parameters(ina):
    print("Measuring voltage, current, and power with: ...")
    print("Peripheral type: ", ina.__qualname__)
    print("ina219._shunt_ohms: ", ina._shunt_ohms)
    print("ina219._max_expected_amps: ", ina._max_expected_amps)
    print("INA219 Periferal address decimal: ", ina.address)
    print("Registers: Config_REG:  /x{0},  Shunt_Reg /x0{1},  Voltage_REG  /x0{2},  Power_REG  /x0{3},  Current_REG  /x0{4},  Calibration_REG  /x0{5}".format(
        ina.__REG_CONFIG, ina.__REG_SHUNTVOLTAGE, ina.__REG_BUSVOLTAGE, ina.__REG_POWER,
        ina.__REG_CURRENT, ina.__REG_CALIBRATION))
    print("Possible Bus Ranges: ", ina.__BUS_RANGE)
    print("Using FSR voltage range: ",ina.__BUS_RANGE [0] )
   
   #print("compute current LSB: " ina._configure(ina.address, ,,)
   # print("ina219.shunt_voltage: ", ina.shunt_voltage())
   #print("ina219._voltage_range : ", ina._voltage_range )
   #print("ina219._gain: ", ina._gain)

''' configure(self, voltage_range=RANGE_32V, gain=GAIN_AUTO,
                  bus_adc=ADC_12BIT, shunt_adc=ADC_12BIT):
                  '''
    
    
SCL=Pin(21)
SDA=Pin(22)
# i2c=I2C(0x40, *, SCL,SDA)
i2c=SI2C(  SCL,SDA, freq=400000 )
#i2c.start()
# __init__( shunt_ohms, max_expected_amps=None, busnum=None, address=__ADDRESS,   log_level=logging.DEBUG):
ina219 =  INA219(0.1, 3.2)
          
          
ina219._i2c=i2c
show_parameters(ina219)

#print(help(i2c))
print(" scan i2c devices...: ", i2c.scan())
#TODO: Find out why the esp32 cannot see the INA219 as device 0x40. ENODEV means it cannot see the device. https://stackoverflow.com/questions/64269494/micropython-oserror-errno-19-enodev
#TODO: Find out if I need to initialize i2c with the id (0x40). No it defaults to 0x40 = 64d
print("Trying to read 10 bytes from INA219:", ina219._i2c.readfrom(0x40, 10, True))
conf =b'1C5F'
print("Writing  to Config Register:  ", conf)

ina219._i2c.writeto_mem(0x40,0x00,conf)

configreg = INA219._configuration_register(0x40,0x00)
print("Config Register try to  read 2 bytes: ", i2c.readfrom_mem(0x40, 0x00, 2))


print("Writing to the Calibration register: 1053h")
calib=b'1053'
# INA219._calibrate(calib)  # needs 3 args.
#calibrationReg = INA219._calibration_register ()  #needs 2 args
#print("Reading config from Configuration Register:", configreg)
#print("Reading from Calibration Register: ", calibrationReg)
#print("Read  Bus Voltage Register: ", INA219._read_voltage_register()) # requires 1 arg
#print("Reading Shunt Voltage Register: ", INA219._shunt_voltage_register()) #requires 1 arg
#print("Reading Current Register: ", INA219. current()) #requires 1 arg
#print("Reading Power : ", INA219.power(ina_219)) #requires 1 arg


    

