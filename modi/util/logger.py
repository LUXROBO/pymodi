import base64
import json


cmd_dict = {
    0x00: 'Health',
    0x01: 'Echo',
    0x02: 'Module Info',
    0x03: 'Request Property',
    0x04: 'Set Property',
    0x05: 'Assign ID',
    0x06: 'Assign Action',
    0x07: 'Topology Signal',
    0x08: 'Find ID',
    0x09: 'Set State',
    0x0A: 'Warning',
    0x0B: 'Firmware Data',
    0x0C: 'Firmware State',
    0x0D: 'Firmware Command',
    0x10: 'Stream Data',
    0x11: 'Stream State',
    0x12: 'Stream Command',
    0x13: 'Request Monitor',
    0x14: 'Battery',
    0x1C: 'Variable',
    0x1D: 'Sync Signal',
    0x1E: 'Event',
    0x1F: 'Channel Property',
}


def log(msg: str, log_type: str):
    if log_type == 'r':
        with open("communication_log.txt", 'a') as logfile:
            logfile.write(f'recv - {msg}\n')
    elif log_type == 's':
        with open("communication_log.txt", 'a') as logfile:
            logfile.write(f'send - {msg}\n')
    elif log_type == 'i':
        with open("communication_log.txt", 'w') as logfile:
            logfile.write('pyMODI Logging...\n')
    else:
        raise Exception


