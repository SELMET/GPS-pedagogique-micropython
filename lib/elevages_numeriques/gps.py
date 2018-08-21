import board
import busio
import adafruit_gps

class Gps(adafruit_gps.GPS):
    
    _header = 'datetime;latitude;longitude;altitude;fix_quality;# satellites;horizontal dilution'
    
    _KEYS = ('datetime', 'latitude', 'longitude', 'fix_quality', 'satellites', 'horizontal_dilution')
    
    _FIELDS = (_KEYS[0:3]) # display first 3 fields by default
    
    @property
    def header(self):
        return ';'.join(Gps._FIELDS)
    
    def __init__(self):
        RX = board.RX
        TX = board.TX
        uart = busio.UART(TX, RX, baudrate=9600, timeout=3000)
        super(Gps, self).__init__(uart, debug=False)
        
    def timestamp_to_datetime(self):
        """
        Format a struct_time into human-readable datetime
        YYYY-MM-DD hh:mm:ss
        """
        time = self.timestamp_utc
        return '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec)
        
    def __str__(self):
        return '{};{};{};{};{};{};{}'.format(
            self.timestamp_to_datetime(), 
            self.latitude, 
            self.longitude, 
            self.altitude_m, 
            self.fix_quality,
            self.satellites, 
            self.horizontal_dilution)
    
    
    
    