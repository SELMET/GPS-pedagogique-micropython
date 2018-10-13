import board
import digitalio


class Logger:
    def __init__(self, debug=False):
        """
        Initialises the Logger object
        :param debug:  Will print storage errors when enabled
        """
        self._switch = digitalio.DigitalInOut(board.D7)
        self._switch.direction = digitalio.Direction.INPUT
        self._switch.pull = digitalio.Pull.UP
        self.debug = False
        
    def can_log(self):
        """
        Checks if the switch is in the LOG position

        If it returns True, the module can write to its internal storage and the computer can't
        If it returns False, the module can read its internal storage but can't write on it
        """
        return not self._switch.value
        
    def file_exists(self, file_name):
        """
        Checks if a file exists

        :param file_name: the file name to check
        :return: True if the file exists, False otherwise
        """
        exists = False
        try:
            with open('/{}'.format(file_name), "r") as fp:
                exists = True
        except OSError as e:
            pass
        return exists

    def log_line(self, file_name, line, newline=True):
        """
        Writes a line to the internal storage
        :param file_name:
        :param line: the string to write
        :param newline: set to False to stay remove the trailing carriage return
        :return:
        """
        try:
            with open('/{}'.format(file_name), "a") as fp:
                fp.write(line)
                if newline and not line.endswith('\n'):
                    fp.write('\n')
                fp.flush()
                return True
                
        except OSError as e:
            if self.debug:                
                if e.args[0] == 28:
                    print('Error : storage is probably full')
                elif e.args[0] == 30:
                    print('Error : storage is probably read-only : check the switch')
            return False