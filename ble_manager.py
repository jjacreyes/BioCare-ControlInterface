import asyncio
from bleak import BleakClient, BleakScanner

# Service and Characteristic UUIDs -- Should match ESP32 defined UUIDs
SERVICE_UUID = "b36ffaec-2ef4-4f92-8240-05877b9d71e6"
TX_UUID = "36e89808-bb82-471d-9791-a2dc10994675" # UUID for Python Module to Transmit (write) -> Named RX_UUID on .cpp
RX_UUID = "c6b9e79d-8f5c-4cc0-9628-04cdd5a05bd8" # UUID for Python Module to Recieve (notify) -> Named TX_UUID on .cpp

# Data Storage for plot v. time
times = []
forceA_values = []
start_time = None

class BLEManager:
    """BLE Manager class to search for advertising devices.
    Return True if device found and connected.
    Return False if device is not founds
    """

    def __init__(self):
        self.client = None

    async def connect(self):
        devices = await BleakScanner.discover()
        esp32 = None

        for d in devices:
            if d.name and "BioCare_ProstheticESP32" in d.name:
                esp32 = d
                break

        if not esp32:
            print("Device Not Found....")
            return False
        
        self.client = BleakClient(esp32.address)
        await self.client.connect()
        print("========= Device Connected =========== ")
        print(f"Device Found: {esp32.name} ({esp32.address})")
        return True
    

async def start_notifications(self, callback):
    """Starts notification tracing"""
    await self.client.start_notify(RX_UUID, callback)


async def send_gesture(self, position_list):
    """ Uploads gestures via 4 - byte BLE package"""

    position_data = bytes(position_list)
    await self.client.write_gatt_char(TX_UUID, position_data)