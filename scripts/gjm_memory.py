import gc
import micropython
import esp32
import esp

print("==============================")
print("Not useful, esp32.idf_heap_info",esp32.idf_heap_info(esp32.HEAP_DATA))
print("==============================")

print("micropython mem_info: ", micropython.mem_info())
print()
print("The max new split value in :func: micropython.mem_info() output corresponds to the largest free block of ESP-IDF heap that could be automatically added on demand to the MicroPython heap.")
print("==============================")

print("Heap from: gc.mem_free: ",gc.mem_free())
print()
print("The result of :func: gc.mem_free() is the total of the current free + max new split values printed by :func: micropython.mem_info().")
print("==========Flash====================")
print("Flash_Size: ",esp.flash_size())
print("Flash User Start: ",esp.flash_user_start())

print("Writing to and reading from Flash is not working correctly...")
buf = 'bHello, this is garth'
print("buf to write: ", buf)
print("Write ",esp.flash_write(2097153, buf))
buf = bytearray(21)
print("Reading from first 20 bytes of User Flash:  ",esp.flash_read(2097153, buf))