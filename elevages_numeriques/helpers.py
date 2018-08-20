
 
# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536