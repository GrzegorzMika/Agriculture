import logging
import os
import time
from datetime import datetime
from typing import Union, List


def find(name: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def catch_measurement(sensor, period: int, wait: Union[int, float]) -> float:
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
    now = datetime.now()
    with open(path, 'a+') as f:
        try:
            f.write('{}, {}\n'.format(now.strftime("%Y-%m-%d %H:%M:%S"), measurement))
        except Exception as e:
            logging.error(e)


def exit_on_time(exit_time: dict) -> bool:
    now = datetime.now()
    leave_time = now.replace(**exit_time)
    return now < leave_time
