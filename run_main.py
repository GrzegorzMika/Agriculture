import json
import logging
import os

from cleaner import cleaner
from humidity import humidity
from light import light
from moisture import moisture
from synchronize_gcp import synchronize_gcp
from temperature import temperature
from utils import find


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    logging.basicConfig(filename=os.path.join(setup.get('log_storage'), 'log.log'), level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    logger.info('Start collecting data...')
    temperature(setup)
    humidity(setup)
    moisture(setup)
    light(setup)
    logger.info('Collection completed')

    logger.info('Start synchronization...')
    synchronize_gcp(setup)
    logger.info('Synchronization completed')

    logger.info('Start cleanup...')
    cleaner(setup)
    logger.info('Cleanup completed')

    logger.info("That's all for today")


if __name__ == '__main__':
    main()
