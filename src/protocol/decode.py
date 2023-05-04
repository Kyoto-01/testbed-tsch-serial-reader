FIRMTYPE_SERVER = 'server'
FIRMTYPE_CLIENT = 'client'
FIRMWARE_PROTOCOL_FIELD_COUNT = 9


def decode_protocol_data(data: 'str') -> 'dict':
    data = data.split(',')
    data = [item.strip() for item in data]

    ret = {}

    if len(data) == FIRMWARE_PROTOCOL_FIELD_COUNT:
        firmtype = data[0]

        if firmtype == FIRMTYPE_SERVER:
            ret = decode_server_data(data)
        elif firmtype == FIRMTYPE_CLIENT:
            ret = decode_client_data(data)

    return ret


def decode_server_data(data: 'list') -> 'dict':
    return {
        "firmtype": data[0],
        "addr": data[1],
        "peer": data[2],
        "rssi": data[3],
        "datalen": data[4],
        "tx": data[5],
        "rx": data[6],
        "txpwr": data[7],
        "ch": data[8],
    }


def decode_client_data(data: 'list') -> 'dict':
    return {
        "firmtype": data[0],
        "addr": data[1],
        "peer": data[2],
        "datalen": data[3],
        "tx": data[4],
        "rx": data[5],
        "txpwr": data[6],
        "ch": data[7]
    }
