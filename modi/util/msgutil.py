import json
import struct
from base64 import b64encode, b64decode
from typing import Tuple


def parse_message(command: int, source: int, destination: int,
                  byte_data: Tuple =
                  (None, None, None, None, None, None, None, None)):
    message = dict()
    message['c'] = command
    message['s'] = source
    message['d'] = destination
    message['b'] = __encode_bytes(byte_data)
    message['l'] = len(byte_data)
    return json.dumps(message, separators=(",", ":"))


def __extract_length(begin: int, src: Tuple) -> int:
    length = 1
    for i in range(begin + 1, len(src)):
        if not src[i]:
            length += 1
        else:
            break
    return length


def __encode_bytes(byte_data: Tuple):
    idx = 0
    data = bytearray(len(byte_data))
    while idx < len(byte_data):
        if not byte_data[idx]:
            idx += 1
        elif byte_data[idx] > 256:
            length = __extract_length(idx, byte_data)
            data[idx: idx + length] = int.to_bytes(
                byte_data[idx], byteorder='little', length=length, signed=True
            )
            idx += length
        elif byte_data[idx] < 0:
            data[idx: idx + 4] = int.to_bytes(
                int(byte_data[idx]), byteorder='little', length=4, signed=True
            )
            idx += 4
        elif byte_data[idx] < 256:
            data[idx] = int(byte_data[idx])
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
        result.append(int.from_bytes(data[idx:idx + size], byteorder='little'))
        idx += size
    return result


def parse_data(values, data_type: str) -> Tuple:
    data = []
    if data_type == 'int':
        for value in values:
            if value >= 0:
                data += int.to_bytes(int(value), byteorder='little', length=2)
            else:
                data += int.to_bytes(
                    int(value), byteorder='little', length=4, signed=True
                )
    elif data_type == 'float':
        for value in values:
            data += struct.pack("f", float(value))
    elif data_type == 'string':
        data = map(ord, str(values))
    elif data_type == 'raw':
        data = values
    elif data_type == 'display_var':
        data = struct.pack("f", float(values[0])) + bytearray(
            [values[1], 0x00, values[2], 0x00])
    return tuple(data)


def decode_data(data: str) -> float:
    return round(struct.unpack("f", bytes(unpack_data(data)[:4]))[0], 2)
