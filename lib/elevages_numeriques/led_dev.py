"""
`Led`
====================================================

Internal Red-Green-Blue utilities module.  Can control the built-in RGB LED in color and brightness
"""

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


class Led(nonblocking_timer):
    """Creates the RBG Led interface

        :param float brightness: the Led brightness, (ranges from 0.00 to 1.00), optionnal
        :param int r: the red   component value of the color, (ranges from 0 to 255), optionnal
        :param int g: the green component value of the color, (ranges from 0 to 255), optionnal
        :param int b: the blue  component value of the color, (ranges from 0 to 255), optionnal


        Example usage:

        .. code-block:: python
            from elevages_numeriques.led import *

            led = Led() # The Led object can be created without arguments
            # The available colors are :
            # RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE, PURPLE, TEAL, WHITE AND OFF
            led.color = RED # Chosen color is red
            led.brightness = 0.5 # Set brightness to 50%
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
            print('Error initializing RGB LED')
            print(' The LED may have already been created elsewhere')
            return
        self._dot[0] = (r, g, b)
    
    def static(self):
        """
        Sets the Led mode to 'static', to stop blinking
        """
	
        self.stop()
        self.color = self._saved_color
        
    def stop(self):
        super(Led, self).stop()
        pass
        
    def run(self):
    """
    Runs the Led mode update, making it actually blink if Led mode is currently 'blinking' and not 'static'
    """
        if self._status == nonblocking_timer._RUNNING:
            self.next()
    
    def next(self):
        if super(Led, self).next():
            self._blink_state = not self._blink_state
            
            if self._blink_state:
                self._dot[0] = self._saved_color
            else:                
                self._dot[0] = [0, 0, 0]

    def __deinit__(self):
        self._dot.deinit()
    
    def __repr__(self):
        return self._dot[0]
    
    @property
    def color(self):
    """
    Returns the current color of the Led 
    """

        return self._dot[0]
        
    @color.setter
    def color(self, color):
        """Defines the color of the Led to the given value
        
        :param color: A predifined color constant such as RED, CYAN, PURPLE, etc.  
        """
        self._dot[0] = color
        
    @property
    def brightness(self):
    """ Returns the current Led brightness (ranges from 0.00 to 1.00) """
        return self._dot.brightness
    
    @brightness.setter
    def brightness(self, brightness):
        """
        Sets the Led brightness
        :param float brightness: The new brightness (ranges from 0.00 to 1.00)²
        """

        self._dot.brightness = brightness
        self._dot.show()
        
    def blink(self, color=None, period=0.5):
        """
        Sets the internal LED mode to 'blinking mode'

        In blinking mode, you'll need to call run() regularly
        You can set the brightness beforehand to blink with a specific brightness
        :param color: the color to use when blinking
        :param period: The period during the Led is either On or OFF

        Example usage:

        .. code-block:: python
            from elevages_numeriques.led import *

            # Makes the Led blink in Blue
            # The Led will turn on for 1.5 second, turn off for 1.5 second (and so on...) until led.static() is called
            led = Led()
            led.blink(BLUE, 1.5)
            while(True):
                led.run()
        """

        if color is not None:
            self.color = color
        self._saved_color = color
        
        self.set_interval(period)

        self.start()
