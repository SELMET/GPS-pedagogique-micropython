import board
import digitalio
import storage
 


class Logger():
    def __init__(self):
        self._switch = digitalio.DigitalInOut(board.D7)
        self._switch.direction = digitalio.Direction.INPUT
        self._switch.pull = digitalio.Pull.UP
        
    def can_log(self):
        """
        If the switch reads LOW, the module can write to its internal storage and the computer can't
        If the switch reads HIGH, the module can read its internal storage but can't write on it
        """
        return not self._switch.value
        
    def log_line(self, file_name, line, newline=True):
        
        if not self.can_log():
            print('Warning ! Switch is in the wrong position: logging may be disabled !')
        
        try:
            with open('/{}'.format(file_name), "a") as fp:
                fp.write(line)
                if newline and not line.endswith('\n'):
                    fp.write('\n')
                fp.flush()
                
        except OSError as e:
            delay = 0.5
            if e.args[0] == 28:
                raise OSError('storage is probably full ')
            elif e.args[0] == 30:
                raise OSError('storage is probably read-only : check the switch')
        
        