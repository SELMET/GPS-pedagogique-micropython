"""
import board
import adafruit_dotstar
from nonblocking_timer import *
from micropython import const
"""

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
