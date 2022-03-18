try:
    from . import TCPIPADAU146x

except:
    import TCPIPADAU146x



class PacketReadRequest(TCPIPADAU146x.PacketReadRequest):
    pass



class PacketReadResponse(TCPIPADAU146x.PacketReadResponse):
    pass



class PacketWrite(TCPIPADAU146x.PacketWrite):
    pass



class_finder = {PacketWrite.CONTROL_CODE       : PacketWrite,
                PacketReadRequest.CONTROL_CODE : PacketReadRequest,
                PacketReadResponse.CONTROL_CODE: PacketReadResponse}
