#!/usr/bin/env python3

'''
@file       at86rf215-ping-pong.py
@author     Pere Tuset-Peiro  (peretuset@openmote.com) modified by felipefbs and Kyoto-01
@version    v0.1
@date       February, 2019
@brief

@copyright  Copyright 2019, OpenMote Technologies, S.L.
            This file is licensed under the GNU General Public License v2.
'''

import argparse
import signal
from serial.serialutil import SerialException
from json.decoder import JSONDecodeError

from collector.serial_collector import SerialCollector
from database.db_connection import InfluxDBConnection
from testbed.collector_manager import TestbedCollectorManager


CONFIG_FILE = '../config.ini'

config = {
    'testbed_name': None,
    'serial_ports': None,
    'serial_baudrate': None,
    'data_persist': True
}

finished = False


def signal_handler(sig, frame):
    global finished
    finished = True


def setup_from_cmdline():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-t", "--testbed", type=str)
    parser.add_argument("-p", "--ports", type=str)
    parser.add_argument("-b", "--baudrate", type=int, default=115200)
    parser.add_argument("-n", "--nopersist", action='store_true')

    args = parser.parse_args()

    if args.ports:
        config['serial_ports'] = args.ports.split(',')
        config['serial_ports'] = [p.strip() for p in config['serial_ports']]

    config['testbed_name'] = args.testbed
    config['serial_baudrate'] = args.baudrate
    config['data_persist'] = not args.nopersist


def show_banner(
    testbedName: 'str',
    collectors: 'list[SerialCollector]'
):
    print('-' * 70)

    print(f'Running Testbed TSCH Serial Reader: {testbedName}')

    print(
        f'Collecting data from port(s):',
        ', '.join([c.port for c in collectors if not c.is_closed()])
    )

    print('Baudrate:', config['serial_baudrate'])

    print(f"Data persist: {config['data_persist']}")

    print('-' * 70, '\n')


def config_collectors():
    collectors = []

    try:
        if config['serial_ports']:
            collectors = SerialCollector.get_collectors_from_ports(
                ports=config['serial_ports'],
                baudrate=config['serial_baudrate']
            )
        else:
            collectors = TestbedCollectorManager.get_testbed_devices_collectors(
                baudrate=config['serial_baudrate']
            )
    except SerialException as se:
        print(se.strerror)
        raise

    return collectors


def config_database():
    database = None

    if config['data_persist']:
        try:
            with open(CONFIG_FILE):
                pass
            database = InfluxDBConnection(configFile=CONFIG_FILE)

        except FileNotFoundError as fe:
            print(f"Configuration file \"{CONFIG_FILE}\" not found")
            raise

        except JSONDecodeError as je:
            print(f"Syntax error in configuration file \"{CONFIG_FILE}\"")
            raise

        except KeyError as ke:
            print(
                f"Configuration file \"{CONFIG_FILE}\" misconfigured: ",
                f"Missing \"{ke.args[0]}\" key"
            )
            raise

        except Exception as e:
            print(e)
            raise

    return database


def main():
    setup_from_cmdline()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        collectors = config_collectors()
        database = config_database()
    except:
        return
    else:
        collectorManager = TestbedCollectorManager(
            collectorList=collectors,
            database=database,
            testbedName=config['testbed_name']
        )

        show_banner(
            testbedName=collectorManager.testbedName,
            collectors=collectors
        )

        collectorManager.start()

        while not finished:
            pass
        else:
            collectorManager.close()
            if database:
                database.close()


if __name__ == '__main__':
    main()
