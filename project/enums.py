from enum import Enum


class Operator(Enum):
    LABEL = 1
    CUT = 2
    GLUE = 3
    COPY = 4
    KILL = 5
    RUN = 6
    die = -1


class CutPos(Enum):
    ABOVE = -1
    BELOW = 1

