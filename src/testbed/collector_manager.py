from threading import Thread, Lock
from datetime import datetime
from uuid import uuid4

from collector.serial_collector import SerialCollector
from database.db_connection import InfluxDBConnection
from protocol.decode import decode_protocol_data
from utils import sys_info


class TestbedCollectorManager:

    def __init__(
        self,
        collectorList: 'list[SerialCollector]',
        database: 'InfluxDBConnection',
        testbedName=f'testbed-{str(uuid4())}'
    ):
        self._collectorList = collectorList
        self._database = database
        self._testbedName = testbedName
        self._finished = False
        self._mutex = Lock()

    @staticmethod
    def get_testbed_devices_collectors(baudrate: 'int'):
        devices = sys_info.get_sys_serial_devices()
        devices = devices[1::2]
        devices = SerialCollector.get_collectors_from_ports(devices, baudrate)

        return devices

    @property
    def testbedName(self):
        return self._testbedName

    def start(self):
        for collector in self._collectorList:
            Thread(
                target=self._manage_collector,
                args=(collector,)
            ).start()

    def _persist_collected_data(self, data: 'dict'):
        if self._database:
            data = list(data.items())

            measurement = data[0][1]
            tags = dict(data[1:3])
            fields = dict(data[3:])

            self._database.insert(
                bucket=self._testbedName,
                measurement=measurement,
                tags=tags,
                fields=fields
            )

    def _show_collected_data(self, data: 'dict', port: 'str'):
        print(f'[ ({datetime.now()}) {port} ]')

        for k, v in data.items():
            print(f'{k}: {v}')

        print()

    def _manage_collector(self, collector: 'SerialCollector'):
        while not self._finished:
            data = collector.collect()

            if data:
                data = decode_protocol_data(data)

                if data:
                    with self._mutex:
                        self._persist_collected_data(data)
                        self._show_collected_data(data, collector.port)

    def close(self):
        self._finished = True
