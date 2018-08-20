import board
import adafruit_dotstar
import digitalio

class Led:

    def __init__(self, brightness=0.2, r=0, g=0, b=0):
        try:
            self._dot = adafruit_dotstar.DotStar(
                board.APA102_SCK, 
                board.APA102_MOSI, 
                1,  # num pixels
                brightness=brightness
            )
        except ValueError:
            print("Error initializing RGB LED.")
            print(" The LED may have already been created elsewhere")
            return None
        pass
        
        self._dot[0] = [r, g, b]
        self.mode = 'STATIC'
        
    # end __init__ Led
    
    def __deinit__(self):
        self._dot.deinit()
    
    def __repr__(self):
        return self._dot[0]
    
    @property
    def color(self):
        return self._dot[0]
        
    @color.setter
    def color(self, color):
        self._dot[0] = color
        
    @property
    def brightness(self):
        return self._dot.brightness
    
    @brightness.setter
    def brightness(self, brightness):
        self._dot.brightness = brightness
        self._dot.show()

# end class Led

# Simple colors definition
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)


_mode_switch = digitalio.DigitalInOut(board.D7)
_mode_switch.direction = digitalio.Direction.INPUT
_mode_switch.pull = digitalio.Pull.UP

_internal = digitalio.DigitalInOut(board.D13)
_internal.direction = digitalio.Direction.OUTPUT
_internal.value = _mode_switch.value