from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.seeed_dht import DHT


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


class Temperature:
    def __init__(self, port):
        """
        Wrapper for Grove Temperature sensor.
        :param port: port to which the sensor is connected
        """
        self.sensor = DHT("11", port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        _, temperature = self.sensor.read()
        return temperature


class Humidity:
    def __init__(self, port):
        """
        Wrapper for Grove Humidity sensor.
        :param port: port to which the sensor is connected
        """
        self.sensor = DHT("11", port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        humidity, _ = self.sensor.read()
        return humidity


class Light:
    def __init__(self, port):
        """
        Wrapper for Grove Light sensor.
        :param port: port to which the sensor is connected
        """
        self.sensor = GroveLightSensor(port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        return self.sensor.light
