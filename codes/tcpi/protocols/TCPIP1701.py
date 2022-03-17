try:
    from . import protocol

except:
    import protocol



class PacketReadRequest(protocol.PacketReadRequest):
    pass



class PacketReadResponse(protocol.PacketReadResponse):
    pass



class PacketWrite(protocol.PacketWrite):
    pass



class_finder = {PacketWrite.CONTROL_CODE       : PacketWrite,
                PacketReadRequest.CONTROL_CODE : PacketReadRequest,
                PacketReadResponse.CONTROL_CODE: PacketReadResponse}
