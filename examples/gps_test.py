from elevages_numeriques.gps import *
import time

gps = Gps() # declare your GPS  object

# Choose which data you want to keep
# By default, only datetime, latitude and longitude are kept
# You can enable a field with gps.set_logging(FIELD_NAME, True)
# and disable a field with gps.set_logging(FIELD_NAME, False)
# where FIELD_NAME can be one of the following :
# 'all' or '*'          : selects all the following fields at once
# 'datetime',           : current date and time (UTC timezone !), formatted as 'YYYY-MM-DD hh:mm:ss'
# 'latitude',           : latitude, in degrees
# 'longitude',          : longitude, in degrees
# 'altitude',           : altitude, in meters
# 'speed',              : current speed, in Km/h
# 'fix_quality',        : positionning quality indicator; 0=invalid, 1=valid, 2 and more: high precision
# 'satellites',         : how many satellites do we see ?
# 'horizontal_dilution' : GPS signal confidence indicator. The lower the better Check Wikipedia if you need more details.
#                         <2:Excellent, 2-5:Good, 5-10:Moderate, 10 and more:Poor

# example 1 : Everything except speed and altitude
# gps.set_logging('all', True)
# gps.set_logging('speed', False)
# gps.set_logging('altitude', False)

# example 2 : only speed, altitude and # of satellites, in that order
# gps.set_logging('all', False)
# gps.set_logging('speed', True)
# gps.set_logging('altitude', True)
# gps.set_logging('satellites', True)

# example 3 (these are the fields by default) : datetime, latitude and longitude, in that order
gps.set_logging('all', False)
gps.set_logging('datetime', True)
gps.set_logging('latitude', True)
gps.set_logging('longitude', True)


last_print = time.monotonic()
logs = 0
while logs < 10:
    # Make sure to call gps.update() every loop iteration
    # This returns a bool that's true if it got new data
    gps.update()
    
    # Every second print out current location details if there's a fix.
    current_time = time.monotonic()
    if current_time - last_print >= 1.0:
        last_print = current_time
        
        if not gps.has_fix: # if the GPS has a fix, it means it knows where it is
            print('Waiting for fix... {} satellite(s) found'.format(int(gps.satellites)))
            continue
        
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print(gps.header)   # this prints the enabled fields names, CSV formatted
        print(gps)          # this prints the enabled fields content, CSV formatted
        logs = logs + 1