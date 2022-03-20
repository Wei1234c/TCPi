import threading
import time

from tcpi.networking.socket_server import SocketServer
from tcpi.protocols.TCPIP1701 import class_finder, PacketReadResponse



def show_packet(data):
    control_code = data[0]
    cls = class_finder.get(control_code)

    if cls:
        packet = cls()
        packet.load_bytes(data)
        packet.print()

        if packet.elements['Control'].value == 10:
            response = PacketReadResponse(chip_address = 1, sub_address = 0, data = bytes([0, 0x80, 0]))
            response.print()
            print([b for b in response.bytes])
            server.send(response.bytes)
            # server.send( bytes([11, 0, 8, 0, 0, 128, 0, 0]))



server = SocketServer()
server.add_subscriber(show_packet)

# server.run()
t_server = threading.Thread(target = server.run)
t_server.start()
time.sleep(1)

server.stop()
t_server.join()
