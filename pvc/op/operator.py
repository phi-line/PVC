import abc

from pvc.pipe import pipe

class OP(abc.ABC):
    """A generic interface for performing an operation via callback."""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
    
    def validate(self) -> bool:
        ...

    def process(self, i: pipe.PVCPipe, o: pipe.PVCPipe) -> None:
        ...


class NoOP(OP):
    """A no-op implementation of the OP generic."""

    def __init__(self, config: dict):
        super().__init__(config)

    def validate(self) -> bool:
        """Always validate; config is not used."""
        return True

    def process(self, i: pipe.PVCPipe, o: pipe.PVCPipe) -> None:
        """Receive the frame and then send it back."""
        frame = i.receive()
        o.send(frame)


class ControlNet(OP):
    """Implementation of the ControlNet operator."""
    
    def __init__(self, config: dict):
        super().__init__(config)

    def validate(self) -> bool:
        """Validate that the input is acceptable by ControlNet"""
        # TODO(kiem) Validate the ControlNet config
        return True

    def process(self, i: pipe.PVCPipe, o: pipe.PVCPipe) -> None:
        """Receive the frame and then send it back."""
        frame = i.receive()

        # TODO(kiem) Process the input + config with the ControlNet

        o.send(frame)