from typing import List
from custom_exceptions import InvalidOperatorException
from logger.logger import Logger, Severity
from pool import Pool, Strand, Acid, CutPos
from runner import Runner
from const import OPERATOR_PARAMS


START_POINT = 'LABEL Start'


class Interpreter:
    def __init__(self, program_file: str):
        self.used_files: List[str] = []

        self.log: Logger = Logger()
        self.runners: List[Runner] = []
        self.pool: Pool = self._make_pool(program_file)

    def _make_pool(self, program_file: str) -> Pool:
        if program_file in self.used_files:
            self.log.log(Severity.ERROR, 'circular file use triggered by a second use of: ' + program_file)
            quit()

        pool: Pool = Pool()

        with open(program_file, 'r') as file:

            current_acids: List[Acid] = []
            for line in file:
                if line[0] == '#':  # marks a comment
                    continue

                line = line.strip()
                if line:  # line is not empty
                    if line.startswith('USE'):
                        sub_pool = self._make_pool(line.split(' ', maxsplit=1)[1])
                        for sub_strands in sub_pool.strands.values():
                            for sub_strand in sub_strands:
                                pool.add_strand(sub_strand)
                        continue
                    try:
                        current_acids.append(Acid(line))
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
        if start_strand is not None:
            self.runners.append(Runner(start_strand))
        else:
            self.log.log(Severity.WARNING, 'No starting point was found. Start point instructions is: ' + START_POINT)

        return pool

    def run(self):
        while len(self.runners) > 0:
            runners_to_kill: List[int] = []

            for i in range(len(self.runners)):
                runner = self.runners[i]
                runner_should_die = self.runner_tick(runner)
                if runner_should_die:
                    runners_to_kill.append(i)

            for i in runners_to_kill[::-1]:
                self.runners.pop(i)

            self.print_state()

    def runner_tick(self, runner: Runner) -> bool:
        operator, params = runner.tick()
        if len(params) > OPERATOR_PARAMS[operator]:
            self.log.log(
                Severity.ERROR,
                'wrong amount of operators for line: ' + operator + ' ' + ' '.join(params)
            )
            quit()

        match operator:
            case 'RUN':
                strand = self.pool.find(params[0])
                if strand:
                    self.runners.append(Runner(strand))
            case 'CUT':
                if params[1] not in ['up', 'down']:
                    self.log.log(
                        Severity.ERROR,
                        'bad parameter for CUT: ' + params[1]
                    )
                pos = CutPos.ABOVE if params[1] == 'up' else CutPos.BELOW
                self.pool.cut(params[0], pos)
            case 'GLUE':
                self.pool.glue(params[0], params[1])
            case 'COPY':
                self.pool.clone(params[0])
            case 'KILL':
                self.pool.kill(params[0])
            case 'die':
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
                    'strand ' + key
                )
                for acid in strand.acids:
                    self.log.log(
                        Severity.PROGRAM_OUT,
                        '   ' + acid.label
                    )
        self.log.log(
            Severity.PROGRAM_OUT,
            '___________________________\n'
        )
