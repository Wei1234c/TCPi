import threading
import time

from tcpi.networking.socket_client import SocketClient
from tcpi.networking.socket_server import SocketServer
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

client = SocketClient()
t_client = threading.Thread(target = client.run)

t_server.start()
time.sleep(1)
t_client.start()
time.sleep(2)

packet = PacketReadRequest(chip_address = 1, sub_address = 8, n_bytes = 4)
client.send(packet.bytes)

server.stop()
client.stop()

t_server.join()
t_client.join()
