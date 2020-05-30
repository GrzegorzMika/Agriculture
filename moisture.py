import logging
import os
from datetime import date

from sensors import Moisture
from utils import catch_measurement, save_measurement, exit_on_time


def moisture(setup):
    log_storage = setup.get('log_storage')
    local_storage = setup.get('local_storage')

    logging.basicConfig(filename=os.path.join(log_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    moisture_port = setup['moisture'].get('moisture_port')
    period = setup['moisture'].get('period')
    wait = setup['moisture'].get('wait')

    moisture_sensor = Moisture(moisture_port)

    with open(os.path.join(local_storage, 'moisture_' + str(date.today()) + '.txt'), 'w+') as f:
        f.write('Timestamp, Moisture\n')

    while exit_on_time(setup['moisture'].get('exit_time')):
        measurement = catch_measurement(sensor=moisture_sensor, period=period, wait=wait)
        save_measurement(measurement=measurement,
                         path=os.path.join(local_storage, 'moisture_' + str(date.today()) + '.txt'))

    quit()
