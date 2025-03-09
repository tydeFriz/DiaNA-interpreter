from typing import List
from custom_exceptions import InvalidOperatorException
from enums import Operator


OPERATOR_MAP = {
    Operator.LABEL.name: Operator.LABEL,
    Operator.CUT.name: Operator.CUT,
    Operator.GLUE.name: Operator.GLUE,
    Operator.COPY.name: Operator.COPY,
    Operator.KILL.name: Operator.KILL,
    Operator.RUN.name: Operator.RUN
}

PARAM_SEPARATOR = '|-|'


def _parse_parameters(parameters: str) -> List[str]:
    return parameters.split(' ')


class Acid:

    def __init__(self, line: str):
        operator, parameters = line.lstrip().split(maxsplit=1)
        if operator not in OPERATOR_MAP.keys():
            raise InvalidOperatorException(operator)
        self.operator: Operator = OPERATOR_MAP[operator]
        self.params: List[str] = _parse_parameters(parameters)
        self.label: str = self.params[0] if operator == Operator.LABEL.name else line.replace(' ', PARAM_SEPARATOR)

    def get_line(self) -> str:
        return ' '.join([self.operator.name] + self.params)
