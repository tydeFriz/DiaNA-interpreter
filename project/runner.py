from typing import List, Tuple
from pool import Strand


class Runner:

    def __init__(self, strand: Strand):
        self.strand: Strand = strand
        self.current: int = -1

    def tick(self) -> Tuple[str, List[str]]:
        self.current += 1
        if self.current >= len(self.strand.acids):
            return 'die', []

        acid = self.strand.acids[self.current]
        return acid.operator, acid.params
