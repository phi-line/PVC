import abc
import platform
from typing import Optional

import numpy as np


class PVCPipe(abc.ABC):
    """A generic interface for bi-directional communication over syphon/spout.

    Depending on the detected system platform, PVCPipe will create the appropriate
    sender and receiver, and exposes genereric functions for reading and writing.
    """

    def __init__(self, sender_name: str, receiver_name: str):
        super().__init__()
        self.sender_name = sender_name
        self.receiver_name = receiver_name

    @abc.abstractmethod
    def setup(self) -> None:
        ...

    @abc.abstractmethod
    def send(self, frame: np.array) -> None:
        ...

    @abc.abstractmethod
    def receive(self) -> Optional[np.array]:
        ...

    @abc.abstractmethod
    def teardown(self) -> None:
        ...

    @staticmethod
    def create(sender_name: str, receiver_name: str):
        match platform.system():
            case "Windows":
                from pipe import spout

                return spout.SpoutPipe(sender_name, receiver_name)
            case "Darwin":
                # Syphon not implemented yet
                raise Exception("OSX is not supported yet!")
            case _:
                raise Exception(f'Platform "{platform}" is not supported!')
