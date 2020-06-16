

def get_type_from_uuid(uuid: int) -> str:
    """Returns type based on uuid

    :param uuid: UUID of the required type
    :type uuid: int
    :return: Corresponding type
    :rtype: str
    """
    if uuid is None:
        return 'Network'

    hexadecimal = hex(uuid).lstrip("0x")
    type_indicator = str(hexadecimal)[:4]
    module_type = {
        # Input modules
        '2000': 'Env',
        '2010': 'Gyro',
        '2020': 'Mic',
        '2030': 'Button',
        '2040': 'Dial',
        '2050': 'Ultrasonic',
        '2060': 'Infrared',

        # Output modules
        '4000': 'Display',
        '4010': 'Motor',
        '4020': 'Led',
        '4030': 'Speaker',
    }.get(type_indicator)
    return module_type
