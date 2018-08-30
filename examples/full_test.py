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

# We broke out of the previous loop : the GPS has a fix !
print('We have a GPS fix !')
led.color = GREEN
file_name = 'GPS.csv' # Where to store the data
gps.set_logging('speed', True)
gps.set_logging('satellites', True)

if not logger.file_exists(file_name):
    header = gps.header # something like 'datetime;latitude;longitude'
    logger.log_line(file_name, header) # If the log file is freshly created, add the header

logs = 0
while logs < 25: 
    gps.update()
    led.brightness = logs / 25 # Slowly increase the brightness as you get more GPS points
    written = logger.log_line(file_name, str(gps))
    if not written:
        print("couldn't write to storage")
    print('Log #{} : {}'.format(logs, str(gps)))
    logs = logs + 1

led.color = WHITE
led.brightness = 0.2
time.sleep(3)

# Finally, shutdown the LED if the switch is in LOG mode
# This helps saving energy, thus increasing the module's battery life
while True:
    if logger.can_log():
        led.brightness = 0 # led.color = OFF would turn it off too
    else:
        led.brightness = 0.2