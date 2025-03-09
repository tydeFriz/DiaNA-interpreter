from typing import List, Tuple

import config
from enums import Operator
from pool import Strand

RUNNER_COUNTER = 0


class Runner:

    def __init__(self, strand: Strand):
        global RUNNER_COUNTER
        RUNNER_COUNTER += 1
        self.strand: Strand = strand
        self.current: int = -1
        self.id: str = str(RUNNER_COUNTER) + ' ' + self.strand.label()

    def tick(self) -> Tuple[Operator, List[str]]:
        self.current += 1
        if self.current >= len(self.strand.acids):
            return Operator.die, []

        acid = self.strand.acids[self.current]
        if config.DEBUG_PEDANTIC:
            print("running: " + acid.get_line())
        return acid.operator, acid.params
