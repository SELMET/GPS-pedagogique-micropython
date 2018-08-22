import board
import adafruit_dotstar
from nonblocking_timer import *

# Simple colors definition
OFF = (0, 0, 0)
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

# class Led:
class Led(nonblocking_timer):
    """
    Defines basic helpers to manage the internal RGB LED
    """

    def __init__(self, brightness=0.2, r=0, g=0, b=0):
        super(Led, self).__init__(0.5)
        self._blink_state = False
        
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
        self._dot[0] = (r, g, b)
    
    def static(self):
        self.stop()
        self.color = self._saved_color
        
    def stop(self):
        super(Led, self).stop()
        pass
        
    def run(self):
        if self._status == nonblocking_timer._RUNNING:
            self.next()
    
    def next(self):
        if (super(Led, self).next()):
            self._blink_state = not self._blink_state
            
            if(self._blink_state):
                self._dot[0] = self._saved_color
            else:                
                self._dot[0] = [0, 0, 0]

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
        
    def blink(self, color=None, period=0.5):
        if color is not None:
            self.color = color
        self._saved_color = color
        
        self.set_interval(period)
        
        self.start()