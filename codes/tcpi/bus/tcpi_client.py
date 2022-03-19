try:
    from ..protocols.protocol import CONTROL_CODES
    from ..networking.socket_client import SocketClient, socket, time, config

except:
    from protocol import CONTROL_CODES
    from socket_client import SocketClient, socket, time, config



class TCPiClient(SocketClient):
    pass



class Bus(TCPiClient):
    DEBUG_MODE = False


    def __init__(self, class_finder):
        super().__init__()

        self._class_finder = class_finder


    @property
    def is_virtual_device(self):
        return False


    # read ============================================

    def _request_to_read(self, chip_address, sub_address, n_bytes):
        cls = self._class_finder[CONTROL_CODES['ReadRequest']]
        self.send(cls(chip_address, sub_address, n_bytes).bytes)


    def _read_bytes(self, bytes_array):
        cls = self._class_finder[CONTROL_CODES['ReadResponse']]
        packet = cls()
        packet.load_bytes(bytes_array)

        return packet.data


    def read_addressed_bytes(self, chip_address, sub_address, n_bytes):
        self._request_to_read(chip_address, sub_address, n_bytes)
        bytes_response = self.receive()

        if bytes_response:
            assert bytes_response != b''
            return self._read_bytes(bytes_response)


    # write ============================================

    def write_addressed_bytes(self, chip_address, sub_address, bytes_array):
        cls = self._class_finder[CONTROL_CODES['Write']]
        packet = cls(chip_address, sub_address, bytes_array, channel = 0, safeload = True)
        self.send(packet.bytes)



class I2C(Bus):

    def read_addressed_bytes(self, i2c_address, sub_address, n_bytes):
        return super().read_addressed_bytes(i2c_address, sub_address, n_bytes)


    def write_addressed_bytes(self, i2c_address, sub_address, bytes_array):
        return super().write_addressed_bytes(i2c_address, sub_address, bytes_array)



class SPI(Bus):

    def read_addressed_bytes(self, sub_address, n_bytes):
        return super().read_addressed_bytes(0, sub_address, n_bytes)


    def write_addressed_bytes(self, sub_address, bytes_array):
        return super().write_addressed_bytes(0, sub_address, bytes_array)


    def exchange(self, bytes_array):
        raise NotImplementedError
