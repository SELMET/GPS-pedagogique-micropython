import busio
import digitalio
import board
import adafruit_gps


class Gps(adafruit_gps.GPS):

    _KEYS = ('datetime', 'latitude', 'longitude', 'altitude', 'speed', 'fix_quality', 'satellites', 'horizontal_dilution')
	_PORT = None
	try:
		_PORT = board.D10
	except NameError:
		_PORT = 10
		pass
	
    _DIS_PIN = digitalio.DigitalInOut(_PORT) # D10

    @property
    def header(self):
        return ';'.join(self._fields)

    def __init__(self, debug=False):
        uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=3000)
        super(Gps, self).__init__(uart, debug=debug)
        self._fields = list()
        self._fields.extend(Gps._KEYS[0:3])
        Gps._DIS_PIN.direction = digitalio.Direction.OUTPUT
        Gps._DIS_PIN.value = False

    def __str__(self):
        content = list()
        for key in self._fields:
            if key == 'datetime':
                content.append(self._timestamp_to_datetime())
            elif key == 'speed':
                content.append(self.knots_to_kmh())
            elif key == 'altitude':
                content.append(self.altitude_m)
            else:
                content.append(getattr(self, key))
        for i in range(len(content)):
            content[i] = str(content[i])
        return ';'.join(content)

    def enable(self, val=True):
        """
        Enables or disables the GPS module to save energy
        :param val: Enables the module if True, disables it otherwise
        """
        Gps._DIS_PIN.value = not val

    def update(self):
        """
        Fetches the latest data coming from the GPS module
        Call this method at least once before reading a GPS position
        """
        try:
            return super(Gps, self).update()
        except UnicodeError:
            return False

    def set_logging(self, field_name, enable):
        """
        Enables or disables the logging output for the given field
        :param field_name:
        :param enable:
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
                raise RuntimeError('unknown field {}'.format(field_name))
            else:
                self._fields.append(field_name)

    def _timestamp_to_datetime(self):
        """
        Format a struct_time into human-readable datetime
        """
        return '{}/{}/{} {}:{}:{}'.format(
            self.timestamp_utc.tm_mday, 
            self.timestamp_utc.tm_mon, 
            self.timestamp_utc.tm_year, 
            self.timestamp_utc.tm_hour, 
            self.timestamp_utc.tm_min, 
            self.timestamp_utc.tm_sec)
        
    def knots_to_kmh(self):
        """
        Converts provided GPS speed (in knots) to standard km/h
        """
        try:
            return self.speed_knots / 1852
        except TypeError:
            return 0
