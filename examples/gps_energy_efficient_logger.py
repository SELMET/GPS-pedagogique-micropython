import time
import gc       # These libraries are quite big for this small module
from elevages_numeriques.led import *
gc.collect()    # Ask the Garbage Collector (gc) to free some memory
from elevages_numeriques.gps_dev import *
gc.collect()
from elevages_numeriques.logger import *
gc.collect()

def flash_green():
    led.brightness=0.2    # Flasher une fois en vert
    led.color=GREEN
    time.sleep(0.1)
    led.brightness=0    # Ré-éteindre la LED

led = Led()
gps = Gps()
logger = Logger()

file_name = 'DONNEES_GPS/test_reel_GPS.csv' # Where to store the data
gps.set_logging('all', False)    # 'all' or '*' targets all the fields
gps.set_logging('datetime', True)
gps.set_logging('latitude', True)
gps.set_logging('longitude', True)

n = 1
while logger.file_exists(file_name):
    n=n+1
    file_name = 'DONNEES_GPS/test_reel_GPS_'+str(n)+'.csv'
header = gps.header
logger.log_line(file_name, header, newline=False)
logger.log_line(file_name, ';TTFF')

print ('Ecrire sur ' + file_name)

led.color = OFF
led.brightness=0

last_log = time.monotonic() - 9999
last_line = ''
gps_startup = last_log

while True:
    if(time.monotonic() - last_log > 30):

        gps.enable()
        gps_startup = time.monotonic()
        
        while(not gps.update() or not gps.has_fix or last_line == str(gps)): # attendre une màj réussie qui nous donne un fix et une nouvelle valeur
            pass # 
        
        last_line = str(gps)
        last_log = time.monotonic() # Reset le timer

        ttff = time.monotonic() - gps_startup
        line = str(gps) + ';' + str(ttff)
        logger.log_line(file_name, line) # Ecrire la donnée GPS
        
        print('Line : ' + line)

        gps.enable(False)   # Passer le GPS en éco d'énergie
        flash_green()