from grove.grove_moisture_sensor import GroveMoistureSensor


class Moisture:
    def __init__(self, port):
        self.sensor = GroveMoistureSensor(port)

    @property
    def measurement(self):
        return self.sensor.moisture
