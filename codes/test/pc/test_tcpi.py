import threading

from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from tcpi.bus.tcpi_client import I2C as TcpI2C_client
from tcpi.bus.tcpi_server import I2C as TcpI2C_server
from tcpi.protocols.TCPIP1701 import class_finder


with_hardware_device = True

if with_hardware_device:
    ctrl = I2cController()
    _i2c = ctrl.I2C()

else:
    _i2c = None  # using None for testing without actual hardware device.

bus = adapters.I2C(i2c = _i2c)

# server ====================================
tcpi_server = TcpI2C_server(bus, class_finder, i2c_addresses = {1: 0x68 >> 1,
                                                                2: 0xA0 >> 1})
# tcpi_server.run()

t_server = threading.Thread(target = tcpi_server.run)
t_server.start()

# client ====================================
tcpi_client = TcpI2C_client(class_finder)
t_client = threading.Thread(target = tcpi_client.run)
t_client.start()
# ===========================================

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 1]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 2]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))

tcpi_client.write_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, bytes_array = bytes([0, 0, 0, 0]))
print(tcpi_client.read_addressed_bytes(i2c_address = 0x34, sub_address = 0x08, n_bytes = 4))

tcpi_client.stop()
t_client.join()

tcpi_server.stop()
t_server.join()
