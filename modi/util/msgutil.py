import json
from base64 import b64encode, b64decode
from typing import Tuple


def parse_message(command: int, source: int, destination: int,
                  byte_data: Tuple = (None, None, None, None,
                                      None, None, None, None)):
    message = dict()
    message['c'] = command
    message['s'] = source
    message['d'] = destination
    message['b'] = __encode_bytes(byte_data)
    message['l'] = len(byte_data)
    return json.dumps(message, separators=(",", ":"))


def __encode_bytes(byte_data: Tuple):
    idx = 0
    data = bytearray(len(byte_data))
    while idx < len(byte_data):
        if not byte_data[idx]:
            idx += 1
        elif byte_data[idx] > 256:
            data[idx] = byte_data[idx] % 256
            data[idx + 1] = byte_data[idx] >> 8
            idx += 2
        elif byte_data[idx] < 256:
            data[idx] = byte_data[idx]
            idx += 1
    return b64encode(bytes(data)).decode('utf8')


def decode_message(message: str):
    message = json.loads(message)
    command = message['c']
    source = message['s']
    destination = message['d']
    data = message['b']
    length = message['l']
    return command, source, destination, data, length


def unpack_data(data: str, structure: Tuple = (1, 1, 1, 1, 1, 1, 1, 1)):
    data = bytearray(b64decode(data.encode('utf8')))
    idx = 0
    result = []
    for size in structure:
        result.append(int.from_bytes(data[idx:idx+size],
                                     byteorder='little'))
        idx += size
    return result
