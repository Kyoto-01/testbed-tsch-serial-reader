FIRMTYPE_SERVER = 'server'
FIRMTYPE_CLIENT = 'client'

SERVER_PROTOCOL_FIELD_COUNT = 9
CLIENT_PROTOCOL_FIELD_COUNT = 8


def decode_protocol_data(data: 'str') -> 'dict':
    data = data.split(',')
    data = [item.strip() for item in data]

    fieldCount = len(data)

    ret = {}

    if fieldCount > 0:
        firmtype = data[0]

        if (
            firmtype == FIRMTYPE_SERVER and 
            fieldCount == SERVER_PROTOCOL_FIELD_COUNT
        ):
            ret = decode_server_data(data)
        elif (
            firmtype == FIRMTYPE_CLIENT and 
            fieldCount == CLIENT_PROTOCOL_FIELD_COUNT
        ):
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
