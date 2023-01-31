from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


TOKEN = 'xieC8nuRsu6nzlmtgek39_-qETB_ur0wGx0rwgGGM5lvkQjxq1uvDVucB4lfUOsBQT7ULdDnNvDZ9nKPpioyEw=='
ORG = 'ifpb'
BUCKET = 'testbed'


def create_client(dbAddr='localhost'):
    return InfluxDBClient(
        url=f'http://{dbAddr}:8086',
        token=TOKEN,
        org=ORG
    )


class UDPServerDBController:

    '''
        Client to manipulate a InfluxDB database
    '''

    MEASUREMENT = 'udpServer'

    def __init__(self, dbAddr='localhost'):
        self.client = create_client(dbAddr)
        self.__writeApi = self.client.write_api(write_options=SYNCHRONOUS)
        self.__deleteApi = self.client.delete_api()

    def insert(self, data):
        data = {
            'measurement': self.__class__.MEASUREMENT,
            'tags': {
                'addr': data['addr'],
            },
            'fields': {
                'txCount': int(data['txCount']),
                'rxCount': int(data['rxCount']),
                'txPower': int(data['txPower']),
                'channel': int(data['channel']),
                'rssi': int(data['rssi']),
            },
            'time': datetime.utcnow(),
        }

        self.__writeApi.write(BUCKET, ORG, data)

    def remove(self, start, end=None):
        if not end:
            end = datetime.utcnow()

        self.__deleteApi.delete(
            start,
            end,
            f'_measurement="{self.__class__.MEASUREMENT}"',
            bucket=BUCKET,
            org=ORG
        )

    def removeAll(self):
        self.remove('1970-01-01T00:00:00Z')
