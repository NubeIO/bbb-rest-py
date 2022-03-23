def command_to_bool(x) -> bool:
    if x == 'true':
        return True
    elif x == 'false':
        return False
    elif x == 1:
        return True
    elif x == 0:
        return False
    elif x == '1':
        return True
    elif x == '0':
        return False
    elif x == 'on':
        return True
    elif x == 'off':
        return False


def is_float(x) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False


def analog_in(x) -> str:
    x = x.upper()
    return {
        'UI1': 'P9_39',
        'UI2': 'P9_40',
        'UI3': 'P9_37',
        'UI4': 'P9_38',
        'UI5': 'P9_33',
        'UI6': 'P9_36',
        'UI7': 'P9_35',
    }.get(x, -1)


def analog_out(x) -> str:
    x = x.upper()
    return {
        'UO1': 'P8_13',
        'UO2': 'P9_14',
        'UO3': 'P9_21',
        'UO4': 'P9_42',
        'UO5': 'P8_19',
        'UO6': 'P9_16',
        'UO7': 'P9_22',
    }.get(x, -1)


def digital_out(x) -> str:
    x = x.upper()
    return {
        'DO1': 'P8_7',
        'DO2': 'P8_8',
        'DO3': 'P8_9',
        'DO4': 'P8_10',
        'DO5': 'P8_12',
        'R1': 'P9_29',
        'R2': 'P9_12',
        'LC': 'P9_41', # lora connect reset
    }.get(x, -1)


def digital_in(x) -> str:
    x = x.upper()
    return {
        'DI1': 'P9_30',
        'DI2': 'P9_15',
        'DI3': 'P9_31',
        'DI4': 'P9_28',
        'DI5': 'P9_23',
        'DI6': 'P9_25',
        'DI7': 'P9_27',
    }.get(x, -1)
