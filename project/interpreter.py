from typing import List
import time
import config
from enums import CutPos, Operator
from custom_exceptions import InvalidOperatorException
from logger.logger import Logger, Severity
from pool import Pool, Strand, Acid
from runner import Runner
from const import OPERATOR_PARAMS


START_POINT = 'Start'


def use_hash(filename: str, append: str):
    return filename + '_AS_' + append


class Interpreter:
    def __init__(self, program_file: str):
        self.used_files: List[str] = []

        self.log: Logger = Logger()
        self.runners: List[Runner] = []
        self.pool: Pool = self._make_pool(program_file)
        if config.PREPRINT:
            self.print_state()

    def _make_pool(self, program_file: str, append: str = '') -> Pool:
        import_name = use_hash(program_file, append)
        if import_name in self.used_files:
            self.log.log(Severity.WARNING, 'USE name ambiguity triggered by: ' + import_name)
        self.used_files.append(import_name)

        pool: Pool = Pool()

        with open(program_file, 'r') as file:

            current_acids: List[Acid] = []
            for line in file:
                if line[0] == '#':  # marks a comment
                    continue

                line = line.strip()
                if line:  # line is not empty

                    if line.startswith('USE'):
                        line_split = line.split(' ')
                        if len(line_split) != 4:  # USE line should be in the form USE ./path/to/file.dna AS local_name
                            self.log.log(Severity.ERROR, 'invalid USE: ' + line)
                            quit()
                        sub_append = line_split[3]
                        if append != '':
                            sub_append = append + '.' + sub_append
                        sub_pool = self._make_pool(line_split[1], sub_append)
                        for sub_strands in sub_pool.strands.values():
                            for sub_strand in sub_strands:
                                pool.add_strand(sub_strand)
                        continue

                    try:
                        current_acids.append(Acid(line, append))
                    except InvalidOperatorException as e:
                        self.log.log(Severity.ERROR, 'unknown operator: ' + e.operator)
                        quit()

                elif len(current_acids) > 0:  # line is empty and the previous strand was not comments only
                    new_strand = Strand(current_acids)
                    pool.add_strand(new_strand)
                    current_acids = []

            if len(current_acids) > 0:
                new_strand = Strand(current_acids)
                pool.add_strand(new_strand)

        start_strand = pool.find(START_POINT)
        if append == '' and start_strand is not None:  # main file should always have a LABEL Start
            self.runners.append(Runner(start_strand))
        else:
            self.log.log(
                Severity.WARNING,
                'No starting point was found for file "'
                + program_file
                + '". Start point instructions is: '
                + START_POINT
            )

        return pool

    def run(self):
        while len(self.runners) > 0:
            if config.TICK_INTERVAL > 0:
                time.sleep(config.TICK_INTERVAL)

            runners_to_kill: List[int] = []

            for i in range(len(self.runners)):
                runner = self.runners[i]

                if config.DEBUG_PEDANTIC:
                    print("runner " + runner.id)

                try:
                    runner_should_die = self.runner_tick(runner)
                except Exception as e:
                    self.log.log(
                        Severity.ERROR,
                        "error while executing: "
                        + runner.strand.label()
                        + " -> "
                        + runner.strand.acids[runner.current].label)
                    raise e
                if runner_should_die:
                    runners_to_kill.append(i)

            for i in runners_to_kill[::-1]:
                self.runners.pop(i)

            if config.DEBUG_LOGS:
                self.print_state()

    def runner_tick(self, runner: Runner) -> bool:
        operator, params = runner.tick()
        if len(params) > OPERATOR_PARAMS[operator]:
            self.log.log(
                Severity.ERROR,
                'wrong amount of operators for line: ' + operator.name + ' ' + ' '.join(params)
            )
            quit()

        match operator:
            case Operator.RUN:
                strand = self.pool.find(params[0])
                if strand:
                    self.runners.append(Runner(strand))
            case Operator.CUT:
                if params[1] not in ['UP', 'DOWN']:
                    self.log.log(
                        Severity.ERROR,
                        'bad parameter for CUT: ' + params[1]
                    )
                    quit()
                pos = CutPos.ABOVE if params[1] == 'UP' else CutPos.BELOW
                self.pool.cut(params[0], pos)
            case Operator.GLUE:
                self.pool.glue(params[0], params[1])
            case Operator.COPY:
                self.pool.clone(params[0])
            case Operator.KILL:
                self.pool.kill(params[0])
            case Operator.die:
                if len(self.runners) == 1:
                    self.print_state()
                return True
        return False

    #   --------------------
    #       schifo vario
    #   --------------------

    def print_state(self):
        for key in self.pool.strands:
            for strand in self.pool.strands[key]:
                self.log.log(
                    Severity.PROGRAM_OUT,
                    ''
                )
                self.log.log(
                    Severity.PROGRAM_OUT,
                    'strand ' + key
                )
                for acid in strand.acids:
                    self.log.log(
                        Severity.PROGRAM_OUT,
                        '   ' + acid.get_line() + (' [' + acid.label + ']' if config.PRINT_ACID_LABELS else '')
                    )
        self.log.log(
            Severity.PROGRAM_OUT,
            '_____________________________________________________________________\n'
        )
