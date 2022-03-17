try:
    from ..protocols.protocol import CONTROL_CODES
    from ..networking.socket_client import SocketClient, socket, time, config

except:
    from protocol import CONTROL_CODES
    from socket_client import SocketClient, socket, time, config



class TCPiClient(SocketClient):

    def connect(self, server_ip = config.SERVER_IP, server_port = config.SERVER_PORT):
        self.set_server_address(server_ip, server_port)
        print(f'\n[Connecting server: {self.server_address}]')

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_address)
            self.on_connect()

        except Exception as e:
            print(f'<{e.__class__.__name__}> : {e}')
            raise e


    def on_connect(self):
        print(f'\n[Connected with server: {self.server_address}]')


    def receive(self):
        self.socket.settimeout(config.CLIENT_RECEIVE_TIME_OUT_SECONDS)

        try:
            data = self.socket.recv(config.BUFFER_SIZE)

            if len(data) == 0:  # If Broker shut down, need this line to close socket
                self.close_connection()
                return

            return data

        except Exception as e:
            if config.IS_MICROPYTHON:
                if str(e) == config.MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE:
                    raise e

            elif isinstance(e, ConnectionResetError):
                raise e



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
