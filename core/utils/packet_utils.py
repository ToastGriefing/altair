import struct

LOGIN_SUCCESS = b'\n\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00'
LOGIN_FAILED = b'\n\x00\x00\x00\xff\xff\xff\xff\x02\x00\x00\x00\x00\x00'
NULL_BYTE = b'\x00'

def login_packet(payload):
    _packet = NULL_BYTE * 4 + b'\x03' + NULL_BYTE * 3 + payload.encode() + NULL_BYTE * 2
    packet = struct.pack("<i", len(_packet)) + _packet
    return packet

def command_packet(payload):
    _packet = NULL_BYTE * 4 + b'\x02' + NULL_BYTE * 3 + payload.encode() + NULL_BYTE * 2
    packet = struct.pack("<i", len(_packet)) + _packet
    return packet
