import time

import adapters
import config
import machine
import peripherals
from TCPIP1701 import class_finder
from tcpi_server import I2C as TcpI2C
from wifi import wait_for_wifi


# pin_reset ======================
pin_reset = machine.Pin(config.RESET_PIN_ID, machine.Pin.OUT)
pin_reset.value(1)



def reset_adau():
    for v in (1, 0, 1):
        pin_reset.value(v)
        time.sleep(1 / 1e3)



# hardware bus ======================

wait_for_wifi()

with_hardware_device = True

if with_hardware_device:
    _i2c = peripherals.I2C.get_uPy_i2c(scl_pin_id = config.I2C_SCL_PIN_ID,
                                       sda_pin_id = config.I2C_SDA_PIN_ID)
else:
    _i2c = None  # using None for testing without actual hardware device.

bus = adapters.I2C(_i2c)
reset_adau()

# =================================

I2C_ADDRESS = 0x68 >> 1
I2C_ADDRESS_EEPROM = 0xA0 >> 1
I2C_ADDRESSes = {1                 : (I2C_ADDRESS, 2),  # (i2c_addresses, n_sub_address_bytes)
                 2                 : (I2C_ADDRESS_EEPROM, 2),
                 I2C_ADDRESS       : (I2C_ADDRESS, 2),
                 I2C_ADDRESS_EEPROM: (I2C_ADDRESS_EEPROM, 2)}



def process_data(data):
    if data == config.CMD_RESET:
        reset_adau()
        machine.reset()



tcpi_server = TcpI2C(bus, class_finder, i2c_addresses = I2C_ADDRESSes)
tcpi_server.DEBUG_MODE = True

tcpi_server.add_subscriber(process_data)

tcpi_server.run()

# tcpi_server.stop()
