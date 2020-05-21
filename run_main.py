import json

from humidity import humidity
from light import light
from moisture import moisture
from temperature import temperature
from utils import find


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    temperature(setup)
    humidity(setup)
    moisture(setup)
    light(setup)


if __name__ == '__main__':
    main()