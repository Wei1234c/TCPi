import threading

from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from tcpi.bus.tcpi_server import I2C as TcpI2C
from tcpi.protocols.TCPIP1701 import class_finder


with_hardware_device = True

if with_hardware_device:
    ctrl = I2cController()
    _i2c = ctrl.I2C()

else:
    _i2c = None  # using None for testing without actual hardware device.

bus = adapters.I2C(i2c = _i2c)
tcpi_server = TcpI2C(bus, class_finder, i2c_addresses = {1: 0x68 >> 1, 2: 0xA0 >> 1})
print(tcpi_server.ip_address)
# tcpi_server.run()


t_server = threading.Thread(target = tcpi_server.run)
t_server.start()

tcpi_server.stop()
t_server.join()
