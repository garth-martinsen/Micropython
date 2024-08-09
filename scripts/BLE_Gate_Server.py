'''BLE_Gate_Server.py is an adaptation of BLE.py from Freenove tutorial at : /Users/garth/Programming/MicroPython/tutorials/Freenove_ESP32_S3_WROOM_Board-main-1/Python/Python_Codes/02.1_BLE.
GJM added Characteristics, Descriptors, etc to allow "Notify" for the iphone client (Central) . Checklist of changes:
_X_ : rename class BLESimplePeripheral  to class BLEGateServer... in lines: 41 and  88 in demo, needed to substitute proper class
__ : add LocalTimeService as an included Service to access datetime as local datetime
__ : add 9 characteristics with descriptors: datetime, cmd, actor, state, stpTemp, dcmTemp, volts, amps, bat_lvl
__ : test to ensure that all values are sent and received on cellphone correctly every 1000 ms, once connection is established.
__ : make the advertising more clear so that the peripheral is easily identified by a human
'''
import bluetooth
# import random   '''assume this is not needed...'''
import struct
import time
from ble_gate_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# UUIDs for Service, _UART_UUID and  Characteristics: _UART_TX and _UART_RX

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# Characteristics
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
# Instantiate the _UART service and its Characteristics
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)
#===================================
# UUIDs for Service, _TIME_UUID and  Characteristics: _XXX and _YYY

_TIME_UUID = bluetooth.UUID("xxx")
# Characteristics

_UART_TX = (
    bluetooth.UUID("yyy"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
# Instantiate the service and its Characteristics
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLEGateServer:
    def __init__(self, ble, name="ESP3223"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()   
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            print("\nThe BLE connection is successful.")
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback


def demo():
    ble = bluetooth.BLE()
    p = BLEGateServer(ble)

    def on_rx(rx_data):
        print("\nRX:", rx_data)

    p.on_write(on_rx)
    
    print("Please use LightBlue to connect to ESP3223.")

    while True:
        if p.is_connected():
            # Short burst of queued notifications.
            tx_data = input("Enter anything: ")
            print("Send: ", tx_data)
            p.send(tx_data)


if __name__ == "__main__":
    demo()
