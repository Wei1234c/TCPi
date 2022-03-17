from tcpi.protocols.TCPIP1701 import *


p = PacketWrite(chip_address = 0x34, sub_address = 0x08, data = bytes([0, 0x80, 0, 0]))
ba = p.bytes
p.load_bytes(ba)
p.print()

assert ba == p.bytes

p = PacketReadRequest(chip_address = 0x34, sub_address = 0x08, n_bytes = 4)
p.print()

response = PacketReadResponse(chip_address = 0x34, sub_address = 0x08, data = bytes([0, 0x80, 0]), success = True)
response.print()

