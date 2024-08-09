#Network basics
import network

sta_if = network.WLAN(network.STA_IF)
print("sta_if active: ", sta_if.active())
sta_if.active(True)
print("IPAddress: ",sta_if.ifconfig())
sta_if.connect('Ziply1824', '1408945739')
#print("connected: ", sta_if.isconnected())

#ap_if = network.WLAN(network.AP_IF)
#print("ap_if active: ", ap_if.active())

#

