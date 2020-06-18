import json
import logging
import os
from datetime import date

from sensors import Moisture
from utils import catch_measurement, save_measurement, find, exit_on_time


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    local_storage: str = setup.get('local_storage')

    logging.basicConfig(filename=os.path.join(local_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    moisture_port: int = setup['moisture'].get('moisture_port')
    period: int = setup['moisture'].get('period')
    wait: float = setup['moisture'].get('wait')

    moisture_sensor = Moisture(moisture_port)

    filename = os.path.join(local_storage, 'moisture_' + str(date.today()) + '.txt')

    if not os.path.exists(filename):
        with open(filename, 'w+') as f:
            f.write('Timestamp, Moisture\n')

    while exit_on_time(setup['moisture'].get('exit_time')):
        measurement = catch_measurement(sensor=moisture_sensor, period=period, wait=wait)
        save_measurement(measurement=measurement,
                         path=filename)

    quit()


if __name__ == '__main__':
    main()
