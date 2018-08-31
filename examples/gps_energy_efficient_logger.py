"""
This script logs a GPS position every 30 seconds
The GPS sensor is kept disabled most of the time to save energy
"""
import time
import gc       # These libraries are quite big for this small module
from elevages_numeriques.led import *
gc.collect()    # Ask the Garbage Collector (gc) to free some memory
from elevages_numeriques.gps import *
gc.collect()
from elevages_numeriques.logger import *
gc.collect()

gps = Gps()
logger = Logger()

gps.enable(False) # disables the GPS sensor to save energy
gps.set_logging('all', True)    # 'all' or '*' targets all the fields
file_name = 'GPS.csv' # Where to store the data
if not logger.file_exists(file_name):
    header = gps.header
    logger.log_line(file_name, header) # If the log file is freshly created, add the header

def log_position():
	"""
	Re-enable the GPS sensor, get a GPS position when available then disable the sensor again
	"""
	global gps, logger, file_name
	logged = False
	
	gps.enable(True)
	while not logged:
		if gps.update() and gps.has_fix:
            logger.log_line(file_name, str(gps))
			logged = True
	gps.enable(False)

	
	
# Main program starts here
while not gps.has_fix:
    print('Waiting for fix... {} satellite(s) found'.format(gps.satellites))
    gps.update()

last_log = time.monotonic()
while True:
    if(time.monotonic() - last_log > 30): # 
        last_log = time.monotonic()
		log_position()