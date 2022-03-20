import socket


try:
    from .. import config

except:
    import config



class SocketServer:

    def __init__(self, bind_ip = config.BIND_IP, bind_port = config.BIND_PORT):

        # self.bind_address = socket.getaddrinfo(bind_ip, bind_port)[-1][-1]
        self.bind_address = (bind_ip, bind_port)

        self.socket = None
        self.channel = None
        self.client_address = None
        self.is_stopped = True
        self.subscribers = []

        self.init()


    def __del__(self):
        self._close_sockets()


    def init(self):
        self._close_sockets()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.bind_address)
        self.socket.listen(config.MAX_CONCURRENT_CONNECTIONS)


    def _close_sockets(self):
        if self.channel:
            self.channel.close()
            self.channel = None

        if self.socket:
            self.socket.close()
            self.socket = None


    @property
    def ip_address(self):
        return socket.gethostbyname(socket.gethostname()), self.bind_address[1]


    def run(self):
        self.init()
        self.listen()


    def stop(self):
        print('\n[Server set to stop ]')
        self.is_stopped = True
        self.disconnect_client()
        self.socket.close()
        self.socket = None


    @property
    def stopped(self):
        return self.is_stopped


    def listen(self):
        print('\n[Server waiting for connection.]')
        self.is_stopped = False

        while True:
            if self.stopped:
                break

            try:
                self.channel, self.client_address = self.socket.accept()
                self.on_accept()

            except Exception as e:
                print(e)


    def on_accept(self):
        print(f'\n[Connection from client {self.client_address} established.]')

        while True:
            if self.stopped:
                break

            try:
                data = self.channel.recv(config.BUFFER_SIZE)

                if len(data) == 0:
                    self.disconnect_client()
                    break

                self.on_receive(data)

            except OSError as e:
                print(f'<{e.__class__.__name__}> : {e}')
                self.disconnect_client()
                break

            except Exception as e:
                print(f'<{e.__class__.__name__}> : {e}')


    def on_receive(self, data):
        print(f'\n[Server receiving: {len(data)} bytes of data.]')
        print([b for b in data])

        if data:
            for func in self.subscribers:
                func(data)


    def disconnect_client(self):
        if self.channel:
            self.channel.close()
            self.channel = None
            self.on_client_disconnected()


    def on_client_disconnected(self):
        print(f'\n[Connection with client {self.client_address} is closed.]')


    def add_subscriber(self, func):
        self.subscribers.append(func)


    def send(self, data):
        self.channel.sendall(data)
