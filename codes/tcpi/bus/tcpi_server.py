import gc


try:
    from .. import config

except:
    import config

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

    if config.IS_MICROPYTHON:
        print('\n[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))



class TCPiServer(SocketServer):
    pass



class I2C(TCPiServer):
    I2C_ADDRESSes = {1: 0x68 >> 1,
                     2: 0xA0 >> 1}


    def __init__(self, bus, class_finder, i2c_addresses = I2C_ADDRESSes, **kwargs):
        super().__init__(**kwargs)

        self._bus = bus
        self._i2c_addresses = i2c_addresses
        self._class_finder = class_finder

        self.actions = {CONTROL_CODES['Write']      : self.write,
                        CONTROL_CODES['ReadRequest']: self.read}

        self.add_subscriber(self._process_data)


    def _load_packet_data(self, cls, data):

        packet = cls()
        remains = packet.load_bytes(data)
        packet.print()

        return packet, remains


    def _process_data(self, data):

        if config.IS_MICROPYTHON:
            led.blink_on_board_led(times = 1, forever = False, on_seconds = 0.003, off_seconds = 0.0)

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

        collect_garbage()


    def _get_i2c_address(self, packet):
        addr = packet.elements['Chip_address'].value
        return self._i2c_addresses[addr] if addr in self.I2C_ADDRESSes else addr


    def write(self, packet):
        self._bus.write_addressed_bytes(i2c_address = self._get_i2c_address(packet),
                                        sub_address = packet.elements['Address'].value,
                                        bytes_array = packet.data)


    def read(self, packet_request):
        # hardware read =================
        result = self._bus.read_addressed_bytes(i2c_address = self._get_i2c_address(packet_request),
                                                sub_address = packet_request.elements['Address'].value,
                                                n_bytes = packet_request.elements['Data_length'].value)
        # send response packet ==========
        cls = self._class_finder[CONTROL_CODES['ReadResponse']]
        packet_response = cls(chip_address = packet_request.elements['Chip_address'].value,
                              sub_address = packet_request.elements['Address'].value,
                              data = result, success = True)
        packet_response.print()
        self.send(packet_response.bytes)

        return result
