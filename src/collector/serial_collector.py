from serial import Serial


class SerialCollector:

    def __init__(
        self,
        port: 'str',
        baudrate: 'int',
        timeout=1
    ):
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._serial = Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout
        )

    @staticmethod
    def get_collectors_from_ports(
        ports: 'list[str]',
        baudrate: 'int'
    ) -> 'list[SerialCollector]':
        collectors = []

        for port in ports:
            collector = SerialCollector(
                port=port,
                baudrate=baudrate
            )
            if not collector.is_closed():
                collectors.append(collector)

        return collectors

    @property
    def port(self):
        return self._port

    def is_closed(self) -> 'bool':
        return self._serial.closed

    def collect(self):
        if not self.is_closed():
            message = self._serial.readline()

            if message:
                try:
                    message = message.decode()
                except Exception as e:
                    message = None

            return message
