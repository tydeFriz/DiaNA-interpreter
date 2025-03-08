from enum import Enum
from termcolor import cprint


class Severity(Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    PROGRAM_OUT = 9


class Logger:

    def __init__(self):
        self.colors: dict = {
            Severity.ERROR: 'red',
            Severity.WARNING: 'yellow',
            Severity.INFO: 'light_cyan',
            Severity.PROGRAM_OUT: 'white',
        }

    def log(self, severity: Severity, message: str):
        cprint(message, self.colors[severity])
