from interpreter import Interpreter


PROGRAM_FILE = './program/test.dna'


if __name__ == '__main__':
    interpreter = Interpreter(PROGRAM_FILE)
    interpreter.run()
