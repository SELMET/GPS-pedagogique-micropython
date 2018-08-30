import time
import gc       # These libraries are quite big for this small module
from elevages_numeriques.led import *
gc.collect()    # Ask the Garbage Collector (gc) to free some memory
from elevages_numeriques.gps import *
gc.collect()
from elevages_numeriques.logger import *
gc.collect()
print("Free RAM : ", gc.mem_free(), 'bytes')

led = Led()
gps = Gps()
logger = Logger()

led.blink(RED, 0.2)
while not gps.has_fix:
    led.run() # Keep the LED blinking
    print('Waiting for fix... {} satellite(s) found'.format(gps.satellites))
    gps.update()
    
led.static()
led.color = OFF

file_name = 'GPS.csv' # Where to store the data
gps.set_logging('all', True)    # 'all' or '*' targets all the fields
if not logger.file_exists(file_name):
    header = gps.header
    logger.log_line(file_name, header) # If the log file is freshly created, add the header

last_log = time.monotonic()
while True:
    gps.update()
    if(time.monotonic() - last_log > 30):
        last_log = time.monotonic()
        if gps.has_fix:
            led.color = GREEN
            logger.log_line(file_name, str(gps))
        else:
            led.color = RED
        
    time.sleep(1)
    led.color = OFF