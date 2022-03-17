import adapters
import peripherals
from TCPIP1701 import class_finder
from tcpi_server import I2C as TcpI2C


with_hardware_device = True

if with_hardware_device:
    _i2c = peripherals.I2C.get_uPy_i2c(scl_pin_id = 5, sda_pin_id = 4)

else:
    _i2c = None  # using None for testing without actual hardware device.

bus = adapters.I2C(_i2c)

# =================================
tcpi_server = TcpI2C(bus, class_finder)
tcpi_server.run()

tcpi_server.stop()
