FIRMTYPE_SERVER = 'server'
FIRMTYPE_CLIENT = 'client'


def decode_protocol_data(data: 'str') -> 'dict':
    data = data.split(',')
    data = [item.strip() for item in data]

    ret = {}

    if data:
        firmtype = data[0]

        if firmtype == FIRMTYPE_SERVER:
            ret = decode_server_data(data)
        elif firmtype == FIRMTYPE_CLIENT:
            ret = decode_client_data(data)

    return ret


def decode_server_data(data: 'list') -> 'dict':
    return {
        "firmtype": data[0],
        "addrsend": data[1],
        "addrrecv": data[2],
        "tx": data[3],
        "rx": data[4],
        "txpwr": data[5],
        "ch": data[6],
        "rssi": data[7]
    }


def decode_client_data(data: 'list') -> 'dict':
    return {
        "firmtype": data[0],
        "addrsend": data[1],
        "addrrecv": data[2],
        "tx": data[3],
        "rx": data[4],
        "txpwr": data[5],
        "ch": data[6]
    }
