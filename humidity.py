import json
import logging
import os
from datetime import date

from sensors import Humidity
from utils import catch_measurement, save_measurement, find, exit_on_time


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    local_storage: str = setup.get('local_storage')

    logging.basicConfig(filename=os.path.join(local_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    humidity_port: int = setup['humidity'].get('humidity_port')
    period: int = setup['humidity'].get('period')
    wait: float = setup['humidity'].get('wait')

    humidity_sensor = Humidity(humidity_port)

    with open(os.path.join(local_storage, 'humidity_' + str(date.today()) + '.txt'), 'w+') as f:
        f.write('Timestamp, Humidity\n')

    while exit_on_time(setup['humidity'].get('exit_time')):
        measurement = catch_measurement(sensor=humidity_sensor, period=period, wait=wait)
        save_measurement(measurement=measurement,
                         path=os.path.join(local_storage, 'humidity_' + str(date.today()) + '.txt'))

    quit()


if __name__ == '__main__':
    main()

