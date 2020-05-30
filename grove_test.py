import logging
import os
import time
from datetime import datetime

from grove.grove_moisture_sensor import GroveMoistureSensor


class Moisture:
    def __init__(self, port):
        """
        Wrapper for Grove Moisture sensor.
        :param port: port to which the sensor is connected
        """
        self.sensor = GroveMoistureSensor(port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        return self.sensor.moisture


def catch_measurement(sensor, period, wait):
    """
    Catch the measurement value of a sensor. It is an average of period consecutive measurements performed one every
    wait seconds.
    :param sensor: sensor to read
    :param period: how many measurements to perform before sending hte value downstream
    :param wait: how long to wait between consecutive measurements
    :return: measurement value averaged in period
    """
    measurement_temporary = []
    for _ in range(period):
        try:
            measurement_temporary.append(sensor.measurement)
        except Exception as e:
            logging.error(e, exc_info=True)
        finally:
            time.sleep(wait)
    measurement = sum(measurement_temporary) / len(measurement_temporary)
    return measurement


def save_measurement(measurement, path):
    """
    Add measurement value to the file specified by path.
    :param measurement: measurement value
    :param path: path to the file to which append the measurement value
    """
    now = datetime.now()
    with open(path, 'a+') as f:
        try:
            f.write('{}, {}\n'.format(now.strftime("%Y-%m-%d %H:%M:%S"), measurement))
        except Exception as e:
            logging.error(e, exc_info=True)


path = "/home/pi/database"

moisture_sensor = Moisture(port=0)

try:
    files = os.listdir(path)
    files = [f for f in files if 'test' in f]
    files = [f.split('.')[0] for f in files]
    files = [int(f.split('_')[1]) for f in files]
    run = max(files) + 1
except:
    run = 1

with open(os.path.join(path, 'test_' + str(run) + '.txt'), 'w+') as f:
    f.write('Timestamp, Moisture\n')

measurement = catch_measurement(sensor=moisture_sensor, period=60, wait=2)
save_measurement(measurement=measurement,
                 path=os.path.join(path, 'test_' + str(run) + '.txt'))
