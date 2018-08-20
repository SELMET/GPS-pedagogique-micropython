import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the pin is connected to ground with a wire
# CircuitPython can write to the drive
storage.remount("/", switch.value)

if switch.value:
    print( "Read only mode : module won't be able to write to internal storage" )
else:
    print( "Read & write mode : module will be able to write to internal storage but a computer won't" )