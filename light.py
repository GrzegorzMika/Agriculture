import json
import logging
import os
from datetime import date

from sensors import Light
from utils import catch_measurement, save_measurement, find, exit_on_time


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    local_storage: str = setup.get('local_storage')

    logging.basicConfig(filename=os.path.join(local_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    light_port: int = setup['light'].get('light_port')
    period: int = setup['light'].get('period')
    wait: float = setup['light'].get('wait')

    light_sensor = Light(light_port)

    filename = os.path.join(local_storage, 'light_' + str(date.today()) + '.txt')

    if not os.path.exists(filename):
        with open(filename, 'w+') as f:
            f.write('Timestamp, Light\n')

    while exit_on_time(setup['light'].get('exit_time')):
        measurement = catch_measurement(sensor=light_sensor, period=period, wait=wait)
        save_measurement(measurement=measurement,
                         path=filename)

    quit()


if __name__ == '__main__':
    main()

