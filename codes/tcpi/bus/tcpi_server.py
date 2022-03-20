import gc


try:
    from .. import config
    from ..protocols.protocol import CONTROL_CODES
    from ..networking.socket_server import SocketServer

except:
    import config
    from protocol import CONTROL_CODES
    from socket_server import SocketServer
    import led



def collect_garbage():
    gc.collect()
    print('\n[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))



class TCPiServer(SocketServer):
    pass



class Bus(TCPiServer):

    def __init__(self, bus, class_finder, **kwargs):
        super().__init__(**kwargs)

        self._bus = bus
        self._class_finder = class_finder
        self.actions = {CONTROL_CODES['Write']      : self.write,
                        CONTROL_CODES['ReadRequest']: self.read}

        self.add_subscriber(self._process_data)


    def write(self, packet):
        raise NotImplementedError


    def read(self, packet_request):
        raise NotImplementedError


    @staticmethod
    def _load_packet_data(cls_packet, data):

        packet = cls_packet()
        remains = packet.load_bytes(data)
        packet.print()

        return packet, remains


    def _process_data(self, data):

        while len(data) > 0:
            control_code = data[0]
            cls = self._class_finder.get(control_code)

            if cls:
                packet, data = self._load_packet_data(cls, data)
                action = self.actions[control_code]
                action(packet)

            else:
                print('Unknown data: ', data)
                break

        if config.IS_MICROPYTHON:
            led.blink_on_board_led(times = 1, forever = False,
                                   on_seconds = config.LED_ON_ms / 1e3, off_seconds = config.LED_OFF_ms / 1e3)
            collect_garbage()



class I2C(Bus):
    I2C_ADDRESS = 0x68 >> 1
    I2C_ADDRESS_EEPROM = 0xA0 >> 1

    I2C_ADDRESSes = {1                 : (I2C_ADDRESS, 2),  # (i2c_addresses, n_sub_address_bytes)
                     2                 : (I2C_ADDRESS_EEPROM, 2),
                     I2C_ADDRESS       : (I2C_ADDRESS, 2),
                     I2C_ADDRESS_EEPROM: (I2C_ADDRESS_EEPROM, 2)}


    def __init__(self, bus, class_finder, i2c_addresses = I2C_ADDRESSes, **kwargs):
        super().__init__(bus, class_finder, **kwargs)

        self._i2c_addresses = i2c_addresses


    def _get_i2c_address(self, packet):
        addr = packet.elements['Chip_address'].value
        return self._i2c_addresses[addr] if addr in self.I2C_ADDRESSes else (addr, 1)


    def write(self, packet):
        i2c_address, n_sub_address_bytes = self._get_i2c_address(packet)
        self._bus.write_addressed_bytes(i2c_address = i2c_address,
                                        sub_address = packet.elements['Address'].value,
                                        bytes_array = packet.data,
                                        n_sub_address_bytes = n_sub_address_bytes)


    def read(self, packet_request):
        # hardware read =================
        i2c_address, n_sub_address_bytes = self._get_i2c_address(packet_request)
        result = self._bus.read_addressed_bytes(i2c_address = i2c_address,
                                                sub_address = packet_request.elements['Address'].value,
                                                n_bytes = packet_request.elements['Data_length'].value,
                                                n_sub_address_bytes = n_sub_address_bytes)
        # send response packet ==========
        cls = self._class_finder[CONTROL_CODES['ReadResponse']]
        packet_response = cls(chip_address = packet_request.elements['Chip_address'].value,
                              sub_address = packet_request.elements['Address'].value,
                              data = result if result is not None else b'', success = result is not None)
        packet_response.print()
        self.send(packet_response.bytes)

        return result
