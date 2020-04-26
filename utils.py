import logging
import os
import time
from datetime import datetime
from typing import Union, List


def find(name: str, path: str) -> str:
    """
    Find a file specified by name starting from path.
    :param name: name of the file to be found
    :param path: starting location
    :return: path to the file starting from path
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def catch_measurement(sensor, period: int, wait: Union[int, float]) -> float:
    """
    Catch the measurement value of a sensor. It is an average of period consecutive measurements performed one every
    wait seconds.
    :param sensor: sensor to read
    :param period: how many measurements to perform before sending hte value downstream
    :param wait: how long to wait between consecutive measurements
    :return: measurement value averaged in period
    """
    measurement_temporary: List[float] = []
    for _ in range(period):
        try:
            measurement_temporary.append(sensor.measurement)
        except Exception as e:
            logging.error(e)
        finally:
            time.sleep(wait)
    measurement: float = sum(measurement_temporary) / len(measurement_temporary)
    return measurement


def save_measurement(measurement: float, path: str) -> None:
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
            logging.error(e)


def exit_on_time(exit_time: dict) -> bool:
    """
    Verify if the time condition specified by exit_time is met.
    :param exit_time: reference time
    :return: boolean indicating if before reference time (true) or after (false)
    """
    now = datetime.now()
    leave_time = now.replace(**exit_time)
    return now < leave_time
