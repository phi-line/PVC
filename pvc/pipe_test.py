import sys

import numpy as np
import pytest

import pipe

CYAN = np.array([[[0, 255, 255, 255]]], dtype=np.uint8)
MAGENTA = np.array([[[255, 0, 255, 255]]], dtype=np.uint8)


def test_pvc():
    # instantiate two PVC pipes, A and B
    left = pipe.PVCPipe.create(sender_name="A", receiver_name="B")
    right = pipe.PVCPipe.create(sender_name="B", receiver_name="A")

    # first send a cyan frame from left to right, through A
    left.send(CYAN)
    frame = right.receive()    
    assert frame is not None
    assert np.array_equal(frame, CYAN)

    # then send a magenta frame from right to left, through B
    right.send(MAGENTA)
    frame = left.receive()
    assert frame is not None
    assert np.array_equal(frame, MAGENTA)

    # clean up
    left.teardown()
    right.teardown()


if __name__ == "__main__":
    pytest.main(sys.argv)
