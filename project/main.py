import config
from interpreter import Interpreter

if __name__ == '__main__':
    interpreter = Interpreter(config.PROGRAM_FILE)
    interpreter.run()
