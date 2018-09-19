"""
import board
import adafruit_dotstar
from nonblocking_timer import *
from micropython import const
"""
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

# class Todoc:
class Todoc:
    """
    Defines basic helpers to manage the internal RGB LED
    """
    
    def blink(self, color=None, period=0.5):
      """
      Blinky thingy
      """
        if color is not None:
            self.color = color
        self._saved_color = color
        
        self.set_interval(period)

        self.start()
