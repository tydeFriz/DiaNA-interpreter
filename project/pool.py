from __future__ import annotations
from enum import Enum
from typing import Dict, List
from const import OPERATOR_PARAMS
from custom_exceptions import InvalidOperatorException
import secrets


class CutPos(Enum):
    ABOVE = -1
    BELOW = 1


class Acid:

    def __init__(self, line: str):
        operator, parameters = line.lstrip().split(maxsplit=1)
        if operator not in OPERATOR_PARAMS.keys():
            raise InvalidOperatorException(operator)

        self.label: str = line
        self.operator: str = operator
        self.params: List[str] = self._parse_parameters(parameters)

    def _parse_parameters(self, parameters: str) -> List[str]:
        parameters = parameters.split(' ')
        return [p.replace('_', ' ') for p in parameters]


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


class Pool:

    def __init__(self):
        self.strands: Dict[str, List[Strand]] = {}

    def add_strand(self, strand: Strand):
        label = strand.acids[0].label
        if label not in self.strands.keys():
            self.strands[label] = []
        self.strands[label].append(strand)

    def find(self, label: str) -> Strand | None:
        if label not in self.strands.keys():
            return None
        return secrets.choice(self.strands[label])

    def clone(self, label: str):
        strand = self.find(label)
        if not strand:
            return
        acids = []
        for acid in strand.acids:
            acids.append(Acid(acid.label))
        new_strand = Strand(acids)
        self.add_strand(new_strand)

    def cut(self, label: str, pos: CutPos):
        strands: List[Strand] = []
        for strand_list in self.strands.values():
            strands += strand_list
        possibilities: List[Strand] = [strand for strand in strands if label in strand.index.keys()]
        if len(possibilities) == 0:
            return

        strand_to_cut: Strand = secrets.choice(possibilities)
        kill_label: str = strand_to_cut.acids[0].label
        new_strands: List[Strand] = strand_to_cut.cut(label, pos)
        self.strands[kill_label].remove(strand_to_cut)
        for strand in new_strands:
            self.add_strand(strand)

    def glue(self, label_top: str, label_bottom: str):
        bottom_strand = self.find(label_bottom)
        if not bottom_strand:
            return
        strands: List[Strand] = []
        for strand_list in self.strands.values():
            strands += strand_list
        possibilities: List[Strand] = [
            strand for strand in strands if strand.acids[-1].label == label_top and strand != bottom_strand
        ]
        if len(possibilities) == 0:
            return
        up_strand: Strand = secrets.choice(possibilities)
        up_strand.append(bottom_strand)
        self.strands[label_bottom].remove(bottom_strand)

    def kill(self, label: str):
        if label not in self.strands.keys():
            return
        strand_index = secrets.choice(range(len(self.strands[label])))
        killed = self.strands[label].pop(strand_index)
        killed.acids = []
