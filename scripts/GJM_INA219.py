'''Learn how to get I2C to work with an esp32. Different esp32s will have different SCL and SDA pins. lib machine — functions related to the hardware'''
import machine   #will be redundant when I finish classes below
from machine import Pin,  SoftI2C as I2C, mem16 
from micropython import const
import struct
from collections import namedtuple

#Pins for SCL and SDA need PULLUP resistors so they are held high. TheINA219 has 10k Ω resistors embedded in the chip to provide this.
SCL=Pin(22)
SDA=Pin(21)

#Registers
CONFIG_REG = const(0x00)
SHUNTVOLTAGE_REG=const(0X01)
BUSVOLTAGE_REG= const(0x02)
POWER_REG=const(0x03)
CURRENT_REG=const(0x04)
CALIBRATION_REG=const(0x05)
Registers = ["CONFIG_REG", "SHUNTVOLTAGE_REG", "BUSVOLTAGE_REG", "POWER_REG", "CURRENT_REG", "CALIBRATION_REG"]

#VALUES
#Write to Config Reg: 1C5Fh  (7263d)
#Write to Calib Reg:  1053h  (4179d) 
CONFIG=const(0X1C5F)  #ref: https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fdocs.google.com%2Fdocument%2Fd%2F1Atsp6_A-tUvi6SXvg_-Uzt1hx__wah7jDZP4JKNTYWE%2Fedit%3Fpli%3D1&followup=https%3A%2F%2Fdocs.google.com%2Fdocument%2Fd%2F1Atsp6_A-tUvi6SXvg_-Uzt1hx__wah7jDZP4JKNTYWE%2Fedit%3Fpli%3D1&ifkv=Ab5oB3oq5Bgnwf1qJcxNNeOgFHPSLiDy9vRqD_yi6QCu31KGk7dRbORck7Hqx-tiUp-YrcQWcNmMBQ&ltmpl=docs&osid=1&passive=1209600&service=wise&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S305462666%3A1724988400343476&ddm=0#heading=h.v1vijerveij4
CALIB = const(0X1053)
fmt = '@h'  #unsigned Short will handle 2 bytes
CURRENT_LSB = const(98e-6)
POWER_LSB =CURRENT_LSB*20
MEASUREMENTS = namedtuple("MEASUREMENTS",("shunt_volts","bus_volts","supply_volts","power_watts","current_amps"))
def show_attributes(self ):
    print("Format statement for packing bytes", fmt)
    print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
    print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
    print("SoftI2C interface: ",self.i2c)
    print("I2C Device address: ",self.address)
 
    
class GJM_INA219 :
    def __init__(self, SCL, SDA):
        self.i2c= self._create_i2c(SCL,SDA)
        self.addr = int(self._get_device_address())
        
    def _get_device_address(self):
        ''' A scan for devices returns a List of integers. Assume only one for now and adjust later if needed.'''
        return hex(self.i2c.scan()[0])
 
    def _create_i2c(self, scl, sda):
        return I2C(scl,sda)
    
    def set_register( self, reg, val):
        '''saving the CAL value to the CALIBRATION_REG for device
        self.addr. i2c.writeto_mem(0x40, 2, b'\x10') # write 1 byte to memory
        of peripheral self.addr  starting at address 2 in the peripheral'''
        self.i2c.writeto_mem(self.addr, reg, struct.pack(fmt,val))
        
    def read_register(self, reg):
        '''Read two bytes from registry memory previously saved to REGISTRY reg by config, calib, or sensors'''
        val = struct.unpack(fmt,self.i2c.readfrom_mem(self.addr, reg, 2))
        return  val[0]
         
    
    def clear_reg(self, reg):
        val = b'\x0000'
        self.i2c.writeto_mem(self.addr, reg, val)

    def show_registers_addresses(self):
        for i in range(len(Registers)):
            print(Registers[i], ": ",  hex(i))
    
    def show_measurements(self):
        '''Shunt Voltage (V) = Shunt Voltage Register Value * 10 µV, '''
        shunt = self.read_register(SHUNTVOLTAGE_REG) *10e-6
        volt_bus = self.read_register(BUSVOLTAGE_REG) * 4e-3
        power =self.read_register(POWER_REG) * POWER_LSB
        current= self.read_register(CURRENT_REG) * CURRENT_LSB
        volt_supply = shunt + volt_bus
        meas = MEASUREMENTS(shunt, volt_bus, volt_supply,  power, current)
        return meas
        
    def show_attributes(self ):
        print("Format statement for packing bytes", fmt)
        print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
        print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
        print("SoftI2C interface: ",self.i2c)
        print("I2C Device address: ",hex(self.addr))
 
    def get_shunt_voltage(self):
        return self.read_register(SHUNTVOLTAGE_REG) *10e-6
    
    def get_bus_voltage(self):
        return self.read_register(BUSVOLTAGE_REG)*4e-3
    
    def get_current_amps(self):
        return self.read_register(CURRENT_REG) * CURRENT_LSB
        
    def get_power_watts(self):
        return self.read_register(POWER_REG) * POWER_LSB
    
     



