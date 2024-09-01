'''Learn how to get I2C to work with an esp32. Different esp32s will have different SCL and SDA pins. module machine — functions are related to the hardware'''
import machine   
from machine import Pin,  SoftI2C as I2C, mem16 
from micropython import const
import struct
from collections import namedtuple

#Pins for SCL and SDA need PULLUP resistors so they are held high for i2c to work. TheINA219 has two 10k Ω resistors embedded in the chip to provide this.
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
CONFIG=0X1C5F  
CALIB = 0X1053
fmt = '<h'  #unsigned Short will handle 2 bytes (16 bit word, little endian)

MEASUREMENTS = namedtuple("MEASUREMENTS",("shunt_volts","bus_volts","supply_volts","power_watts","current_amps"))
__BUS_RANGE = [16, 32]  # two choices for FSR of Bus; When BUS_FSR=0, the FSR is 16V
BUS_FSR=0
BUS_LSB=4e-3  #4mV
SHUNT_LSB= 9.8e-6  # 9.80 µV = 98e-6 A* 0.1Ω
CURRENT_LSB = const(98e-6)  #amps/bit
POWER_LSB =CURRENT_LSB*20 # 1.96 mW/bit

def show_attributes(self ):
    print("Format statement for packing bytes", fmt)
    print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
    print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
    print("I2C Device address: ",self.address)
    print("Addresses of Registers: ", self.show_registers_addresses())
 
    
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
        '''saving the  value, val  to the register, reg for device at self.addr
        self.addr. i2c.writeto_mem(0x40, 2, b'\x10') # write 1 byte to memory
        of peripheral self.addr  starting at address 2 in the peripheral'''
        self.i2c.writeto_mem(self.addr, reg, struct.pack(fmt,val))
        
    def read_register(self, reg):
        '''Read two bytes from registry memory previously written to  reg by config, calib, or sensors'''
        val = struct.unpack(fmt, self.i2c.readfrom_mem(self.addr, reg, 2))
        return  val[0]
         

    def show_registers_addresses(self):
        '''Cycles thru the 6 registers and displays where they start in memory. Each registry stores a short (2 bytes). '''
        for i in range(len(Registers)):
            print(Registers[i], ": ",  hex(i))
    
    def show_measurements(self):
        '''Shunt Voltage (V) = Shunt Voltage Register Value * 10 µV, '''
        shunt = abs(self.read_register(SHUNTVOLTAGE_REG) )*SHUNT_LSB
        volt_bus = self.read_register(BUSVOLTAGE_REG) * BUS_LSB
        power =abs(self.read_register(POWER_REG)) * POWER_LSB
        current= self.read_register(CURRENT_REG) * CURRENT_LSB
        volt_supply = abs(shunt)+ abs(volt_bus)
        meas = MEASUREMENTS(shunt, volt_bus, volt_supply,  power, current)
        return meas
        
    def show_attributes(self ):
        print("Format statement for packing bytes", fmt)
        print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
        print("Values of pins for SCL: ", SCL.value(), " SDA: ",  SDA.value())
        print("SoftI2C interface: ",self.i2c)
        print("I2C Device address: ", hex(self.addr))
        print("Register Addresses: ", self.show_registers_addresses())
    
    def show_configuration(self):
        print("INA219 Configuration: ")
        print("Configuration Register and Value: ", hex(CONFIG_REG), "--", self.read_register(CONFIG_REG))
        print("Calibration Register and Value: ", hex(CALIBRATION_REG), "--", self.read_register(CALIBRATION_REG))
        print("Full Scale Range of Bus ADC:  ", __BUS_RANGE [BUS_FSR])
        print("Current_LSB: ", CURRENT_LSB)
        print("Shunt_LSB: ", SHUNT_LSB)
        print("Power_LSB: ", POWER_LSB)
    
    def get_shunt_voltage(self):
        '''When ina is ready, read the register for shunt voltage: 0x01'''
        return self.read_register(SHUNTVOLTAGE_REG) *10e-6
    
    def get_bus_voltage(self):
        return self.read_register(BUSVOLTAGE_REG)*4e-3
    
    def get_current_amps(self):
        return self.read_register(CURRENT_REG) * CURRENT_LSB
        
    def get_power_watts(self):
        return self.read_register(POWER_REG) * POWER_LSB
    
    def reset(self):
        '''Bit 15 is Reset Bit. Setting this bit to '1' generates a system reset that is the same as power-on reset. This resets all registers to default values; this bit self-clears.'''
        self.set_register(CONFIG_REG, CONFIG | 1<<15)
                
    def esp32_type(self):
        print(" esp32 Unique_id : ",  machine.unique_id() )
        
    def theBug(self):
        '''Store 0x1C5F in Config_reg , read it back out and unpack it to see if the value is correctly stored.'''
        #TODO: Fix bug that saves 0x1C5F to CONFIG Register and later returns 0x1C1F, short by 0x40 , why ?
        print("First show that packing and unpacking a value does not cause the error.")
        input1 = 0x1C5F
        bts=struct.pack(fmt, input1)
        output1= struct.unpack(fmt, bts)[0]
        print("inputValue, packedValue, unpackedValue: ",input1,", " ,bts,", " ,output1)
        print(" input1 == output1: ", input1== output1)
        print("-------------------------------")
        print("Now show what happens when value is stored in CONFIG_Reg, read from CONFIG_REG and unpacked...")
        input2= 0x1C5F
        self.set_register(CONFIG_REG, input2)
        output2 = self.read_register(CONFIG_REG)
        bts2 =  self.i2c.readfrom_mem(self.addr, CONFIG_REG, 2)
        print(" Config_Register: inputValue, packed value returned,   unpackedValue: ",input2, ", " , bts2, ", ", output2)
        print(" input2== output2: ", input2== output2)
        print("Difference between input and output: ", hex(input2-output2))
        
        '''Example: For a value of VSHUNT = –320 mV:
1. Take the absolute value (include accuracy to 0.01 mV) → 320.00
2. Translate this number to a whole decimal number → 32000
3. Convert it to binary → 111 1101 0000 0000
4. Complement the binary result : 000 0010 1111 1111
5. Add 1 to the Complement to create the Two’s Complement formatted result → 000 0011 0000 0000
6. Extend the sign and create the 16-bit word: 1000 0011 0000 0000 = 8300h (Remember to extend the sign to all sign-bits, as necessary based on the PGA setting.)
formula: v =32000; 
'''