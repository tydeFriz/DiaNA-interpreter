from __future__ import annotations
from typing import Dict, List
import secrets
from enums import CutPos
from pool.strand import Strand
from pool.acid import Acid


class Pool:

    def __init__(self):
        self.strands: Dict[str, List[Strand]] = {}

    def add_strand(self, strand: Strand):
        label = strand.label()
        if label not in self.strands.keys():
            self.strands[label] = []
        self.strands[label].append(strand)

    def find(self, label: str) -> Strand | None:
        if label not in self.strands.keys():
            return None
        options = self.strands[label]
        if len(options) == 0:
            return None
        if len(options) == 1:
            return options[0]
        return secrets.choice(self.strands[label])

    def clone(self, label: str):
        strand = self.find(label)
        if not strand:
            return
        acids = []
        for acid in strand.acids:
            acids.append(Acid(acid.get_line()))
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
        kill_label: str = strand_to_cut.label()
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
        choices = len(self.strands[label])
        if choices < 1:
            return
        strand_index = 0 if choices == 1 else secrets.choice(range(choices))
        killed = self.strands[label].pop(strand_index)
        killed.acids = []
