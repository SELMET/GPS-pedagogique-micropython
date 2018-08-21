import board
import busio
import adafruit_gps

class Gps():
    def __init__(self):
        RX = board.RX
        TX = board.TX
        uart = busio.UART(TX, RX, baudrate=9600, timeout=3000)
        self._gps = adafruit_gps.GPS(uart, debug=False)
        # Turn on the basic GGA and RMC info
        self._gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Set update rate to once a second (1hz) which is what you typically want.
        self._gps.send_command(b'PMTK220,1000')
    
    def update(self):
        self._gps.update()
    
    def has_fix(self):
        return self._gps.has_fix
    
    @property
    def timestamp_utc(self):
        return self._gps.timestamp_utc
    
    @property
    def latitude(self):
        return self._gps.latitude
    
    @property
    def longitude(self):
        return self._gps.longitude
    
    @property
    def fix_quality(self):
        return self._gps.fix_quality
    
    @property
    def satellites(self):
        return self._gps.satellites
    
    @property
    def altitude_m(self):
        return self._gps.altitude_m
    
    @property
    def track_angle_deg(self):
        return self._gps.track_angle_deg
    
    @property
    def speed_knots(self):
        return self._gps.speed_knots
    
    @property
    def horizontal_dilution(self):
        return self._gps.horizontal_dilution
        
    @property
    def dilution_quality(self):
        """
        cf. https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
        """
        if horizontal_dilution <= 1.0:
            return 'Ideal'
        elif horizontal_dilution <= 2.0:
            return 'Excellent'
        elif horizontal_dilution <= 5.0:
            return 'Good'
        elif horizontal_dilution <= 10.0:
            return 'Moderate'
        elif horizontal_dilution <= 20.0:
            return 'Fair'
        else:
            return 'Poor'
    
    @property
    def height_geoid(self):
        return self._gps.height_geoid