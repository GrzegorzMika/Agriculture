import json
import logging
import os
from datetime import date

from sensors import Temperature
from utils import catch_measurement, save_measurement, find, exit_on_time


def main():
    with open(find('setup', '/')) as f:
        setup = json.load(f)

    local_storage: str = setup.get('local_storage')

    logging.basicConfig(filename=os.path.join(local_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    temperature_port: int = setup['temperature'].get('temperature_port')
    period: int = setup['temperature'].get('period')
    wait: float = setup['temperature'].get('wait')

    temperature_sensor = Temperature(temperature_port)

    with open(os.path.join(local_storage, 'temperature_' + str(date.today()) + '.txt'), 'w+') as f:
        f.write('Timestamp, Temperature\n')

    while exit_on_time(setup['temperature'].get('exit_time')):
        measurement = catch_measurement(sensor=temperature_sensor, period=period, wait=wait)
        save_measurement(measurement=measurement,
                         path=os.path.join(local_storage, 'temperature_' + str(date.today()) + '.txt'))

    quit()


if __name__ == '__main__':
    main()
