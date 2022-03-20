import socket


try:
    from .. import config

except:
    import config



class SocketClient:

    def __init__(self):
        self.socket = None
        self.subscribers = []


    def __del__(self):
        if self.socket:
            self.socket.close()
            self.socket = None


    def set_server_address(self, server_ip, server_port):
        self.server_address = socket.getaddrinfo(server_ip, server_port)[-1][-1]


    def run(self):
        self.connect()


    def stop(self):
        print('\n[Client set to stop.]')
        self.is_stopped = True
        self.close_connection()


    @property
    def stopped(self):
        return self.is_stopped


    def connect(self, server_ip, server_port = config.SERVER_PORT):
        self.set_server_address(server_ip, server_port)

        try:
            print(f'\n[Connecting server: {self.server_address}]')
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


    def close_connection(self):
        if self.socket:
            self.socket.close()
            self.socket = None

            self.on_close()


    def on_close(self):
        print(f'\n[Connection with server {self.server_address} is closed.]')


    def add_subscriber(self, func):
        self.subscribers.append(func)


    def send(self, data):
        # assert self.socket is not None, 'Not connected.'
        self.socket.sendall(data)
