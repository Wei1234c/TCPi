try:
    from . import protocol

except:
    import protocol



class PacketData:

    def __init__(self):
        self.elements['Total_length'].n_bits = 8 * 4
        self.elements['Data_length'].n_bits = 8 * 4
        self.data = self.data



class PacketReadRequest(protocol.PacketReadRequest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements['Total_length'].n_bits = 8 * 4
        self.elements['Data_length'].n_bits = 8 * 4

        self._elements.append(protocol.Element(name = 'Reserved', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0))
        self.elements = self._elements

        self.elements['Total_length'].value = self.n_bytes



class PacketReadResponse(protocol.PacketReadResponse, PacketData):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._elements.append(protocol.Element(name = 'Reserved', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0))
        self.elements = self._elements

        PacketData.__init__(self)



class PacketWrite(protocol.PacketWrite, PacketData):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PacketData.__init__(self)



class_finder = {PacketWrite.CONTROL_CODE       : PacketWrite,
                PacketReadRequest.CONTROL_CODE : PacketReadRequest,
                PacketReadResponse.CONTROL_CODE: PacketReadResponse}
