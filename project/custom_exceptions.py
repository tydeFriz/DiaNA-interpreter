class InvalidOperatorException(Exception):

    def __init__(self, operator: str):
        super().__init__()
        self.operator: str = operator
