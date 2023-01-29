import logging
from typing import Optional

from pvc import pvc_server

import SpoutGL
import numpy as np
from OpenGL import GL


class SpoutServer(pvc_server.PVCServer):
    def __init__(
        self, sender_name: str = "SpoutSender", receiver_name: str = "SpoutReciever"
    ):
        super().__init__(sender_name, receiver_name)
        self.sender: Optional[SpoutGL.SpoutSender] = None
        self.reciever: Optional[SpoutGL.SpoutReciever] = None

    def setup(self) -> None:
        # setup spout senders and receivers
        self.sender = SpoutGL.SpoutSender()
        self.sender.setSenderName(self.sender_name)
        self.reciever = SpoutGL.SpoutReciever()
        self.reciever.set(self.sender_name)

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
        w, h = self.reciever.getSenderSize()
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        success = self.reciever.receiveImage(frame, w, h, GL.GL_RGBA, False, 0)

        if not success:
            logging.error("Could not receive spout image.")
            return

        return frame

    def teardown(self) -> None:
        self.sender.releaseSender()
        self.reciever.releaseReceiver()
