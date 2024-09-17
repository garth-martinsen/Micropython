#Network basics ref: https://docs.micropython.org/en/latest/esp32/quickref.html
# TODO:Find out why this is not working 9/12/2024

import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('Ziply1824', '1408945739') # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ipconfig('addr4')  # get the interface's IPv4 addresses

# Use Esp32 as an access point (or  an HTTP server)
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.config(ssid='ESP-AP') # set the SSID of the access point
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)         # activate the interface

'''
sta_if = network.WLAN(network.STA_IF)
print("sta_if active: ", sta_if.active())
sta_if.active(True)
print("IPAddress: ",sta_if.ifconfig())
sta_if.connect('Ziply1824', '1408945739')
print("connected: ", sta_if.isconnected())

#ap_if = network.WLAN(network.AP_IF)
#print("ap_if active: ", ap_if.active())

'''
