import time
from elevages_numeriques.led import *

led = Led() # Declare your LED

# Available colors are :
# RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE, PURPLE, TEAL, WHITE AND OFF

led.color = RED
time.sleep(1)
led.color = GREEN
time.sleep(1)
led.color = BLUE
time.sleep(1)

for t in range(5): # fade the LED several times
    
    for i in range(1, 10): # fade in
        led.brightness = i/10 # brightness can be between 0.1 and 1.0
    
    for i in range(10, 1, -1): # fade out
        led.brightness = i/10
        
# The LED has two base modes : static and blinking
# Static is the default mode : the LED keep a fixed color and brightness
# Blink... makes the LED blink at a given speed, but needs to call led.run() in a main loop

led.blink(color=WHITE, period=0.3)

# Let's keep a timer to change the LED mode later
start_time = time.monotonic()

# Here is our main loop
while True:
    led.run()
    
    current_time = time.monotonic()
    if current_time - start_time > 5: # if 5 seconds have passed since we entered the loop
        led.static() # make the LED static again