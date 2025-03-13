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

    def __init__(self, line: str, append: str = ''):
        if append != '':
            append = append + '.'

        operator, parameters = line.lstrip().split(maxsplit=1)
        if operator not in OPERATOR_MAP.keys():
            raise InvalidOperatorException(operator)
        self.operator: Operator = OPERATOR_MAP[operator]

        self.params: List[str] = _parse_parameters(parameters)
        for i in range(len(self.params)):
            self.params[i] = append + self.params[i]

        self.label: str = self.params[0]
        if operator != Operator.LABEL.name:
            self.label = operator + PARAM_SEPARATOR + PARAM_SEPARATOR.join(self.params)

    def get_line(self) -> str:
        return ' '.join([self.operator.name] + self.params)
