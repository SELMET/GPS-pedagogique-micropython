import board
import busio
import adafruit_gps
import digitalio

class Gps(adafruit_gps.GPS):

    _KEYS = ('datetime', 'latitude', 'longitude', 'altitude', 'speed', 'fix_quality', 'satellites', 'horizontal_dilution')
    _DIS_PIN = digitalio.DigitalInOut(board.D10)

    @property
    def header(self):
        return ';'.join(self._fields)

    def set_logging(self, field_name, enable):
        """
        Enables or disables the logging output for the given field
        """
        if field_name == '*' or field_name == 'all':  # wildcard : enable or disable ALL fields
            if enable:
                self._fields = list()
                self._fields.extend(Gps._KEYS[0:len(Gps._KEYS)])
            else:
                self._fields = list()
            return None  # all fields were added or deleted, stop here

        # One-by-one enabling or disabling field
        if not enable and field_name in self._fields:
            self._fields.remove(field_name)
        elif enable and field_name not in self._fields:
            if field_name not in Gps._KEYS:
                raise RuntimeError('field named {} is unknown to the GPS module'.format(field_name))
            else:
                self._fields.append(field_name)

    def __init__(self, debug=False):
        uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=3000)
        super(Gps, self).__init__(uart, debug=debug)
        self._fields = list()
        self._fields.extend(Gps._KEYS[0:3])
        Gps._DIS_PIN.direction = digitalio.Direction.OUTPUT
        Gps._DIS_PIN.value = False

    def update(self):
        try:
            return super(Gps, self).update()
        except UnicodeError:
            return False

	def disable(self):
		Gps._DIS_PIN.value = True

	def enable(self):
		Gps._DIS_PIN.value = False

    def timestamp_to_datetime(self):
        """
        Format a struct_time into human-readable datetime
        YYYY-MM-DD hh:mm:ss
        """
        time = self.timestamp_utc
        return '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec)
        
    def knots_to_kmh(self):
        """
        Converts provided GPS speed (in knots) to standard km/h
        """
        try:
            return self.speed_knots / 1852
        except TypeError:
            return 0

    def __str__(self):
        content = list()
        for key in self._fields:
            if key == 'datetime':
                content.append(self.timestamp_to_datetime())
            elif key == 'latitude':
                content.append(self.latitude)
            elif key == 'longitude':
                content.append(self.longitude)
            elif key == 'altitude':
                content.append(self.altitude_m)
            elif key == 'speed':
                content.append(self.knots_to_kmh())
            elif key == 'fix_quality':
                content.append(self.fix_quality)
            elif key == 'satellites':
                content.append(self.satellites)
            elif key == 'horizontal_dilution':
                content.append(self.horizontal_dilution)
            else:
                raise RuntimeError('something went wrong fetching unknown field {}'.format(key))

        for i in range(0,  len(content)):
            content[i] = str(content[i])
        return ';'.join(content)