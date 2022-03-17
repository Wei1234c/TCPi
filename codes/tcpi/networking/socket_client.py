import socket
import time


try:
    from .. import config

except:
    import config



class SocketClient:

    def __init__(self):
        self.socket = None
        self.set_server_address()
        self.subscribers = []


    def __del__(self):
        if self.socket:
            self.socket.close()
            self.socket = None


    def set_server_address(self, server_ip = config.SERVER_IP, server_port = config.SERVER_PORT):
        self.server_address = socket.getaddrinfo(server_ip, server_port)[-1][-1]


    def run(self):
        self.connect()


    def stop(self):
        print('\n[Client set to stop.]')
        self.is_stopped = True
        self.socket.close()


    @property
    def stopped(self):
        return self.is_stopped


    def connect(self):
        print(f'\n[Connecting server: {self.server_address}]')
        self.is_stopped = False

        while True:
            if self.stopped:
                break

            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(self.server_address)
                self.on_connect()

            except Exception as e:
                print(e)
                time.sleep(config.CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS)


    def on_connect(self):
        print(f'\n[Connected with server: {self.server_address}]')
        self.socket.settimeout(config.CLIENT_RECEIVE_TIME_OUT_SECONDS)

        while True:
            if self.stopped:
                break
            try:
                data = self.socket.recv(config.BUFFER_SIZE)

                if len(data) == 0:  # If Broker shut down, need this line to close socket
                    self.close_connection()
                    break

                self.on_receive(data)

            except Exception as e:
                if config.IS_MICROPYTHON:
                    if str(e) == config.MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE:
                        raise e

                elif isinstance(e, ConnectionResetError):
                    raise e

                # Receiving process timeout.
                self.process_messages()


    def on_receive(self, data):
        print(f'\n[Client receiving: {len(data)} bytes of data.]')
        print([b for b in data])

        if data:
            for func in self.subscribers:
                func(data)


    def process_messages(self):
        pass


    def close_connection(self):
        if self.socket:
            self.socket.close()

        self.on_close()


    def on_close(self):
        print(f'\n[Connection with server {self.server_address} is closed.]')


    def add_subscriber(self, func):
        self.subscribers.append(func)


    def send(self, data):
        self.socket.sendall(data)
