import threading
import time

from tcpi.networking.socket_client import SocketClient
# from tcpi.networking.socket_server import SocketServer
from tcpi.networking.socket_server_concurrent import SocketServer
from tcpi.protocols.TCPIP1701 import class_finder, PacketReadResponse, PacketReadRequest


server = SocketServer()



def show_packet(data):
    control_code = data[0]
    cls = class_finder.get(control_code)

    if cls:
        packet = cls()
        payload = packet.load_bytes(data)
        print('data: ', [b for b in data])
        print('payload: ', payload)
        packet.print()

        if packet.elements['Control'].value == 10:
            response = PacketReadResponse(chip_address = 1, sub_address = 0, data = bytes([0, 0x80, 0]))
            response.print()
            print([b for b in response.bytes])
            server.send(response.bytes)
            # server.send( bytes([11, 0, 8, 0, 0, 128, 0, 0]))



# server  ==================================
server.add_subscriber(show_packet)
t_server = threading.Thread(target = server.run)
t_server.start()
# server.run()
time.sleep(1)

# client ===================================
client = SocketClient()
client.connect()
time.sleep(1)

packet = PacketReadRequest(chip_address = 1, sub_address = 8, n_bytes = 4)
client.send(packet.bytes)

client.stop()
server.stop()

t_server.join()
