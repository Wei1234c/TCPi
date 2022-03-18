from math import ceil


try:
    from utilities import register

except:
    import register

CONTROL_CODES = {'Write'       : 0x09,
                 'ReadRequest' : 0x0A,
                 'ReadResponse': 0x0B}



class Element(register.Element):

    @property
    def n_bytes(self):
        return ceil(self.n_bits // 8)


    @property
    def bytes(self):
        return self.value.to_bytes(self.n_bytes, 'big')



class Packet(register.Register):

    def __init__(self, name):
        super().__init__(name = name)

        self._total_length_slice = None


    @property
    def n_bytes(self):
        return sum([e.n_bytes for e in self._elements])


    @property
    def bytes(self):
        return b''.join([e.bytes for e in self._elements])


    @property
    def total_length_slice(self):

        if self._total_length_slice is None:
            idx_start = 0

            for e in self._elements:
                if e.name != 'Total_length':
                    idx_start += e.n_bytes
                else:
                    break

            idx_stop = idx_start + self.elements['Total_length'].n_bytes
            self._total_length_slice = (idx_start, idx_stop)

        return self._total_length_slice


    def _get_total_length(self, data_bytes):
        idx_start, idx_stop = self.total_length_slice
        return int.from_bytes(data_bytes[idx_start:idx_stop], 'big')


    def _get_my_data_chunk(self, data_bytes):
        length = self._get_total_length(data_bytes)
        my_chunk = data_bytes[:length]
        remains = data_bytes[length:]

        return my_chunk, remains


    def load_bytes(self, data_bytes):
        data, remains = self._get_my_data_chunk(data_bytes)

        for e in self._elements:
            e.value = int.from_bytes(data[:e.n_bytes], 'big')
            data = data[e.n_bytes:]

        self.data = data

        return remains


    def print(self, as_hex = False):
        len_name_field = max([len(e.name) for e in self._elements] + [0])
        print(f'\n{"<< " + self.name + " >>":<{len_name_field + 7}s}')

        for e in self._elements:
            print(
                f'{"[ " + e.name + " ]":<{len_name_field + 5}s}:  {(hex(e.value), bin(e.value)) if as_hex else e.value}')

        return len_name_field



class PacketData(Packet):

    def __init__(self, name):
        super().__init__(name = name)


    @property
    def data(self):
        return self._data


    @property
    def n_bytes(self):
        # MicroPython doesn't support super().property.
        return sum([e.n_bytes for e in self._elements]) + len(self.data)


    @data.setter
    def data(self, data):
        self._data = data
        self.elements['Data_length'].value = len(data)
        self.elements['Total_length'].value = self.n_bytes


    @property
    def bytes(self):
        # MicroPython doesn't support super().property.
        return b''.join([e.bytes for e in self._elements]) + self.data


    def print(self, as_hex = False):
        len_name_field = super().print(as_hex)
        print(f'{"[ Data ]":<{len_name_field + 5}s}:  {[b for b in self.data]}')
        print(f'{"[ Data in Hex ]":<{len_name_field + 5}s}:  {[hex(b) for b in self.data]}')



class PacketReadRequest(Packet):
    CONTROL_CODE = CONTROL_CODES['ReadRequest']


    def __init__(self, chip_address = 1, sub_address = None, n_bytes = None):
        Packet.__init__(self, name = 'ReadRequest')

        self.elements = (Element(name = 'Control', idx_lowest_bit = 0, n_bits = 8 * 1, value = self.CONTROL_CODE),
                         Element(name = 'Total_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0),
                         Element(name = 'Chip_address', idx_lowest_bit = 0, n_bits = 8 * 1, value = chip_address),
                         Element(name = 'Data_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = n_bytes),
                         Element(name = 'Address', idx_lowest_bit = 0, n_bits = 8 * 2, value = sub_address))

        self.elements['Total_length'].value = self.n_bytes



class PacketReadResponse(PacketData):
    CONTROL_CODE = CONTROL_CODES['ReadResponse']


    def __init__(self, chip_address = 1, sub_address = None, data = b'', success = True):
        super().__init__(name = 'ReadResponse')

        self.elements = (Element(name = 'Control', idx_lowest_bit = 0, n_bits = 8 * 1, value = self.CONTROL_CODE),
                         Element(name = 'Total_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0),
                         Element(name = 'Chip_address', idx_lowest_bit = 0, n_bits = 8 * 1, value = chip_address),
                         Element(name = 'Data_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0),
                         Element(name = 'Address', idx_lowest_bit = 0, n_bits = 8 * 2, value = sub_address),
                         Element(name = 'Success', idx_lowest_bit = 0, n_bits = 8 * 1, value = 0 if success else 1))
        self.data = data



class PacketWrite(PacketData):
    CONTROL_CODE = CONTROL_CODES['Write']


    def __init__(self, chip_address = 1, sub_address = None, data = b'', channel = 0, safeload = True):
        super().__init__(name = 'Write')

        self.elements = (Element(name = 'Control', idx_lowest_bit = 0, n_bits = 8 * 1, value = self.CONTROL_CODE),
                         Element(name = 'Safeload', idx_lowest_bit = 0, n_bits = 8 * 1, value = bool(safeload)),
                         Element(name = 'Channel_number', idx_lowest_bit = 0, n_bits = 8 * 1, value = channel),
                         Element(name = 'Total_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0),
                         Element(name = 'Chip_address', idx_lowest_bit = 0, n_bits = 8 * 1, value = chip_address),
                         Element(name = 'Data_length', idx_lowest_bit = 0, n_bits = 8 * 2, value = 0),
                         Element(name = 'Address', idx_lowest_bit = 0, n_bits = 8 * 2, value = sub_address))
        self.data = data



class_finder = {PacketWrite.CONTROL_CODE       : PacketWrite,
                PacketReadRequest.CONTROL_CODE : PacketReadRequest,
                PacketReadResponse.CONTROL_CODE: PacketReadResponse}
