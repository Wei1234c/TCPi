import socket

import select


try:
    from .. import config

except:
    import config



class SocketServer:
    DEBUG_MODE = False


    def __init__(self, bind_ip = config.BIND_IP, bind_port = config.BIND_PORT):
        super().__init__()

        self.bind_address = (bind_ip, bind_port)

        self.socket_being_read = None
        self.socket = None
        self.is_stopped = True
        self.subscribers = []
        self.clients = {}

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
        self.disconnect_clients()
        self.socket.close()
        self.socket = None


    def disconnect_clients(self):
        for k in self.clients.keys():
            self.clients[k].close()
            self.clients[k] = None


    def listen(self):
        print('\n[Server waiting for connection.]')
        self.is_stopped = False

        while True:
            if self.is_stopped:
                break

            # generate list of sockets
            sockets = list(self.clients.values())
            sockets.append(self.socket)

            # select
            list_to_read, _, _ = select.select(sockets, [], [], config.SERVER_POLLING_REQUEST_TIMEOUT_SECONDS)

            # process tasks
            for self.socket_being_read in list_to_read:
                # new connection
                if self.socket_being_read is self.socket:
                    try:
                        self.on_accept()
                        # connections list has changed
                        # need to escape for loop to re-generate the new list of sockets
                        break

                    except OSError as e:
                        print(f'<{e.__class__.__name__}> : {e}')
                        break
                else:
                    # try to receive data
                    try:
                        data = self.socket_being_read.recv(config.BUFFER_SIZE)
                        if len(data) == 0:
                            self.on_close()
                            # connections list has changed
                            # need to escape for loop to re-generate the new list of sockets
                            break

                        self.on_receive(data)

                    except Exception as e:
                        print(f'<{e.__class__.__name__}> : {e}')

                        if config.IS_MICROPYTHON:
                            if str(e) == config.MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE:
                                self.on_close()
                                break
                        elif isinstance(e, ConnectionResetError):
                            self.on_close()
                            break


    def on_accept(self):
        the_socket, client_address = self.socket.accept()
        print(f'\n[Connection from client {client_address} established.]')

        self.clients[client_address] = the_socket


    def on_receive(self, data):

        if self.DEBUG_MODE:
            print(f'\n[Server receiving: {len(data)} bytes of data.]')
            print([b for b in data])

        if data:
            for func in self.subscribers:
                func(data)


    def on_close(self):
        for k, s in self.clients.items():
            if s is self.socket_being_read:
                print(f'\n[Connection with client {k} is closed.]')
                s.close()
                self.clients[k] = None
                del self.clients[k]
                break


    def add_subscriber(self, func):
        self.subscribers.append(func)


    def send(self, data):
        self.socket_being_read.sendall(data)
