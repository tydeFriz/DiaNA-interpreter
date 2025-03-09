from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pool import Acid

import secrets
from typing import List, Dict
from enums import CutPos


class Strand:

    def __init__(self, acids: List[Acid]):
        self.acids: List[Acid] = acids
        self.index: Dict[str, List[int]] = {}
        self._compile_index()

    def _compile_index(self):
        self.index = {}
        acid_index = 0
        for acid in self.acids:
            if acid.label not in self.index.keys():
                self.index[acid.label] = []
            self.index[acid.label].append(acid_index)
            acid_index += 1

    def label(self) -> str:
        return self.acids[0].label

    def append(self, strand: Strand):
        self.acids += strand.acids
        self._compile_index()

    def cut(self, label: str, pos: CutPos) -> List[Strand]:
        new_strands: List[Strand] = []
        acid_index = secrets.choice(self.index[label])
        if acid_index == 0 and pos == CutPos.ABOVE:
            new_strands.append(self)
        elif acid_index == len(self.acids) - 1 and pos == CutPos.BELOW:
            new_strands.append(self)
        elif pos == CutPos.ABOVE:
            new_strands.append(Strand(self.acids[:acid_index]))
            new_strands.append(Strand(self.acids[acid_index:]))
        elif pos == CutPos.BELOW:
            new_strands.append(Strand(self.acids[:acid_index+1]))
            new_strands.append(Strand(self.acids[acid_index+1:]))

        return new_strands
