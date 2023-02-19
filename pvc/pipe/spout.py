import logging
from typing import Optional

from pvc.pipe import pipe

import SpoutGL
import numpy as np
from OpenGL import GL


class SpoutPipe(pipe.PVCPipe):
    """SpoutPipe is the Spout implementation of the PVCPipe generic interface."""

    def __init__(
        self, sender_name: str = "SpoutSender", receiver_name: str = "SpoutReceiver"
    ):
        super().__init__(sender_name, receiver_name)
        self.sender: Optional[SpoutGL.SpoutSender] = None
        self.receiver: Optional[SpoutGL.SpoutReceiver] = None
        self.setup()

    def setup(self) -> None:
        # setup spout senders and receivers
        self.sender = SpoutGL.SpoutSender()
        self.sender.setSenderName(self.sender_name)
        self.receiver = SpoutGL.SpoutReceiver()
        self.receiver.setReceiverName(self.receiver_name)

    def send(self, frame: np.array) -> None:
        h, w = frame.shape[:2]

        success = self.sender.sendImage(frame, w, h, GL.GL_RGBA, False, 0)

        # This fixes the CPU receiver (first frame is discarded)
        # More information: https://github.com/jlai/Python-SpoutGL/issues/15
        self.sender.setCPUshare(True)

        if not success:
            logging.error("Could not send spout image.")
            return

        # Indicate that a frame is ready to read
        self.sender.setFrameSync(self.sender_name)

    def receive(self) -> Optional[np.array]:
        buffer = None

        while True:
            result = self.receiver.receiveImage(buffer, GL.GL_RGBA, False, 0)

            if self.receiver.isUpdated():
                width = self.receiver.getSenderWidth()
                height = self.receiver.getSenderHeight()
                buffer = np.array([[np.repeat(0, width * height * 4)]], dtype=np.uint8)

            if result and buffer.any():
                return buffer

            # Wait until the next frame is ready
            # Wait time is in milliseconds; note that 0 will return immediately
            self.receiver.waitFrameSync(self.receiver_name, 1)

    def teardown(self) -> None:
        self.sender.releaseSender()
        self.receiver.releaseReceiver()
