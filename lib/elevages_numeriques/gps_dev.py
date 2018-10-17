"""
`GPS`
====================================================

GPS utilities module.  Can interact, control and read data from a GPS module,
such as latitude, longitude, and more.

"""

import busio
import digitalio
import board
import adafruit_gps


class Gps(adafruit_gps.GPS):
    """Creates the Gps interface

        :param boolean debug: print errors if they occur , optionnal

        Example usage:

        .. code-block:: python
        
            from elevages_numeriques.gps import *

            gps = Gps() # same as gps = Gps(debug=False)
            gps.update()
            print(gps.header)
            print(gps)

        """

    _KEYS = (
        'datetime', 'latitude', 'longitude', 'altitude', 'speed', 'fix_quality', 'satellites', 'horizontal_dilution')

    _DIS_PIN = None # Sphinx autodoc will throw a NameError when trying to get board.D10
    if hasattr(board, 'D10'): # Do that instead to allow compilation without the correct microcontroler
        _DIS_PIN = digitalio.DigitalInOut(board.D10)
    else:
        _DIS_PIN = 10

    @property
    def header(self):
        """
        Returns the list of currently enabled GPS data fields in CSV format
        :return string: A semicolon-separated list of the enabled fields
        """
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
                content.append(self._knots_to_kmh())
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
        :return boolean: True if update succeeded, False if it failed
        """
        try:
            return super(Gps, self).update()
        except UnicodeError:
            return False

    def set_logging(self, field_name, enable):
        """
        Enables or disables the logging output for the given field

        :param field_name:
        :param enable: Wether to enable or not the given field
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
                if self.debug:
                    print('unknown field {}'.format(field_name))
                    # raise RuntimeError('unknown field {}'.format(field_name))
            else:
                self._fields.append(field_name)

    def _timestamp_to_datetime(self):
        """
        Formats a struct_time into human-readable datetime
        """
        return '{}/{}/{} {}:{}:{}'.format(
            self.timestamp_utc.tm_mday,
            self.timestamp_utc.tm_mon,
            self.timestamp_utc.tm_year,
            self.timestamp_utc.tm_hour,
            self.timestamp_utc.tm_min,
            self.timestamp_utc.tm_sec)

    def _knots_to_kmh(self):
        try:
            return self.speed_knots / 1852
        except TypeError:
            return 0
