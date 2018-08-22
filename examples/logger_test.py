from elevages_numeriques.logger import *

logger = Logger() # Declare your logger object

# The module has a switch which changes its internal storage mode :
# Development mode (or USB mode): allows the user to modify, read and write data to the module's internal storage.
#       The module won't be able to write anythong, but can still read from its internal storage
# Logging mode : allows the module to write data on its internal storage, the data is still accessible via USB, but can't be written that way

# logger.can_log() can be used to remind you if the if the storage switch allows the module to log data
if logger.can_log():
    print("Switch mode : Logging")
else:
    print("Switch mode : USB, development only")
    

logger.log_line('logging.txt', "hello, ", newline=False)
logger.log_line('logging.txt', "world ! (in one line only)")

logger.log_line('example.txt', "to another file ...")
logger.log_line('example.txt', "... using distinct lines")

logger.log_line('structured.csv', "this;is;a;structured;line;using;CSV;formatting")
logger.log_line('structured.csv', "and;another;one")

# Write in a subfolder
logger.log_line('GPS/position.csv', "2018-09-01 14:00:30;43.6168692;3.8585908")

# Check is a file already exists
if logger.file_exists('nonsense.test'): # try with logging.txt too !
    print('file exists')
else:
    print('no such a file')
    