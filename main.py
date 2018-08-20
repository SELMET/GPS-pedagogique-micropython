# import board
import gc
import busio
import time
from digitalio import DigitalInOut, Direction, Pull

# import supagro.led
from elevages_numeriques.led import *

"""
import adafruit_gps
RX = board.RX
TX = board.TX
uart = busio.UART(TX, RX, baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart)
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command('PMTK220,1000')
"""

gc.collect()   # make some rooooom

myLed  = Led(r=255, brightness=0.2)
myLed.brightness = 0.1



time.sleep(20)

last_print = time.monotonic()
while True:
    break
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        if gps.has_fix:
            print('Latitude: {} degrees'.format(gps.latitude))
            print('Longitude: {} degrees'.format(gps.longitude))
            print('Fix quality: {}'.format(gps.fix_quality))
            
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))    
            
            
print("===  done  ===")
  
  