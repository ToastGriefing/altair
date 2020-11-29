import struct

LOGIN_SUCCESS = b'\n\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00'
LOGIN_FAILED = b'\n\x00\x00\x00\xff\xff\xff\xff\x02\x00\x00\x00\x00\x00'

def login_packet(payload):
    _packet = b''
    _packet += b'\x00\x00\x00\x00\x03\x00\x00\x00'
    _packet += payload.encode()
    _packet += b'\x00\x00'

    packet = b''
    packet += struct.pack("<i", len(_packet))
    packet += _packet

    return packet

def command_packet(payload):
    _packet = b''
    _packet += b'\x00\x00\x00\x00\x02\x00\x00\x00'
    _packet += payload.encode()
    _packet += b'\x00\x00'

    packet = b''
    packet += struct.pack("<i", len(_packet))
    packet += _packet

    return packet
