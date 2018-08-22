import board
import digitalio
import storage

print("===  booting  ===")  
switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

storage.mount("/", switch.value)

if switch.value:
    print("Storage mode : development (USB); read-only to internal storage")
else:
    print("Storage mode : logging (LOG); read and write to internal storage is possible")