import abc
from typing import Optional

from pvc.pipe import pipe

import numpy as np


OPERATORS = {
    # default operator that simply returns a NoOP
    "_": lambda: NoOP
}


class OP(abc.ABC):
    """A generic interface for performing an operation via callback."""

    def __init__(self, config: dict):
        super().__init__()
        # Add operator config validation
        self.config = config

    def process(self, left: pipe.PVCPipe, right: pipe.PVCPipe) -> None:
        ...

    @staticmethod
    def create(op_name: str):
        # Check to see if the operator exists in the list of possible operators.
        assert op_name in OPERATORS, f'Operator "{style}" is not supported!'

        return OPERATORS[op_name]


class NoOP(OP):
    """A no-op implementation of the OP generic."""

    def __init__(self, config: dict):
        super().__init__(config)

    def process_input(self, data: dict):
        pass
