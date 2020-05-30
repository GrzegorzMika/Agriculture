from abc import ABCMeta, abstractmethod

from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.seeed_dht import DHT


class Sensor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def measurement(self):
        ...


class Moisture(Sensor):
    def __init__(self, port):
        """
        Wrapper for Grove Moisture sensor.
        :param port: port to which the sensor is connected
        """
        super().__init__()
        self.sensor = GroveMoistureSensor(port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        return self.sensor.moisture


class Temperature(Sensor):
    def __init__(self, port):
        """
        Wrapper for Grove Temperature sensor.
        :param port: port to which the sensor is connected
        """
        super().__init__()
        self.sensor = DHT("11", port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        _, temperature = self.sensor.read()
        return temperature


class Humidity(Sensor):
    def __init__(self, port):
        """
        Wrapper for Grove Humidity sensor.
        :param port: port to which the sensor is connected
        """
        super().__init__()
        self.sensor = DHT("11", port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        humidity, _ = self.sensor.read()
        return humidity


class Light(Sensor):
    def __init__(self, port):
        """
        Wrapper for Grove Light sensor.
        :param port: port to which the sensor is connected
        """
        super().__init__()
        self.sensor = GroveLightSensor(port)

    @property
    def measurement(self):
        """
        Get value of the measurement
        """
        return self.sensor.light
