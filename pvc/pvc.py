import abc
from typing import Optional

import numpy as np


class PVCServer(abc.ABC):
    def __init__(self, sender_name: str, receiver_name: str):
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        super().__init__(sender_name, receiver_name)

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
    def create(sender_name: str, receiver_name: str) -> SpoutServer:
        if platform.startswith("win"):
            import spout

            return spout.SpoutServer(sender_name, receiver_name)
        if platform.startswith("darwin"):
            # Syphon not implemented yet
            raise Exception("OSX is not supported yet!")
        else:
            raise Exception(f"Platform {platform} is not supported!")
