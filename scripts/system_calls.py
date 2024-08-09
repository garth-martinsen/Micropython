import sys
import machine
import os
import time
import struct
import platform
from collections import namedtuple

print("System Implementation: ",sys.implementation)

print("Micro Python Version: ", sys.version)

print("Board info: ", machine.unique_id())
# USBDevice supported? No
# print("USB Device: ", machine.USBDevice())  


print("SOAC Freq HZ: ",machine.freq())
	
print("OS Uname: ", os.uname())
print("dir list: ", os.ilistdir())
print("Current Working Dir: ", os.getcwd())
print("files in dir: ", os.listdir())
# fields in os.statvfs(<path>)
fsbs1="fs_block_size"
frgsz2="frag_size"
fbloks3 = "size_of_fs"
fbfre4 = "free_blks"
fb_avail5 = "unpriviv_blks_avail"
f_files6="#inodes"
free_inodes7="free_inodes"
fi_avail8 =" #free_inodes_4_unpriv_users"
f_flag9="mount_flags"
f_namemax="max_filename_length"
arg_list = [ fsbs1,frgsz2,fbloks3,fbfre4,fb_avail5, f_files6,free_inodes7,fi_avail8, f_flag9, f_namemax]
print(arg_list)
print("stat vfs: ", os.statvfs(os.getcwd()))

Stat_fs = namedtuple("Stat_fs",(arg_list))

statfs= Stat_fs(4096, 4096, 1536, 1532, 1532, 0, 0, 0, 0, 255)

print("example os.statvfs(<path>: ", statfs)
print("Parameters related to inodes: f_files, f_ffree, f_avail and the f_flags parameter may return 0 as they can be unavailable in a port-specific implementation.")

print("platform: ", platform.platform())
print("Compiler: ", platform.python_compiler())
print("libc that MicroPython is linked to & version: ",platform.libc_ver())

print("implement_mpy: ",sys.implementation._mpy)