import threading
import time

from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from tcpi.bus.tcpi_client import I2C as TcpI2C_client
from tcpi.bus.tcpi_server import I2C as TcpI2C_server
from tcpi.protocols.TCPIP1701 import class_finder


with_hardware_device = False

if with_hardware_device:
    ctrl = I2cController()
    _i2c = ctrl.I2C()

else:
    _i2c = None  # using None for testing without actual hardware device.

bus = adapters.I2C(i2c = _i2c)

# server ====================================

I2C_ADDRESS = 0x68 >> 1
I2C_ADDRESS_EEPROM = 0xA0 >> 1
I2C_ADDRESSes = {1                 : (I2C_ADDRESS, 2),  # (i2c_addresses, n_sub_address_bytes)
                 2                 : (I2C_ADDRESS_EEPROM, 2),
                 I2C_ADDRESS       : (I2C_ADDRESS, 2),
                 I2C_ADDRESS_EEPROM: (I2C_ADDRESS_EEPROM, 2)}

tcpi_server = TcpI2C_server(bus, class_finder, i2c_addresses = I2C_ADDRESSes)
print(tcpi_server.ip_address)
t_server = threading.Thread(target = tcpi_server.run)
t_server.start()
time.sleep(1)

# client ====================================
tcpi_client = TcpI2C_client(class_finder)
tcpi_client.connect(*tcpi_server.ip_address)
time.sleep(1)
# ===========================================

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 1]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))


print('====================== re-connecting ==========================')
tcpi_client = TcpI2C_client(class_finder)
tcpi_client.connect(*tcpi_server.ip_address)
time.sleep(1)
print('====================== re-connected ==========================')

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 2]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 0]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))

tcpi_client.stop()
tcpi_server.stop()
t_server.join()
