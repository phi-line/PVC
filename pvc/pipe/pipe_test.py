import sys

import numpy as np
import pytest

from . import pipe

CYAN = np.array([[[0, 255, 255, 255]]], dtype=np.uint8)
MAGENTA = np.array([[[255, 0, 255, 255]]], dtype=np.uint8)


def setup():
    """Instantiate two PVC pipes."""
    left = pipe.PVCPipe.create(sender_name="A-pytest", receiver_name="B-pytest")
    right = pipe.PVCPipe.create(sender_name="B-pytest", receiver_name="A-pytest")
    return (left, right)


def cleanup(pipe_con):
    """Clean up two PVC pipes"""
    left, right = pipe_con
    left.teardown()
    right.teardown()


@pytest.fixture
def pipe_connection():
    """Pytest fixture to setup/teardown PVC pipes A and B."""
    pipe_con = setup()
    yield pipe_con
    cleanup(pipe_con)


def test_pipe(pipe_connection):
    """Test PVC pipe communication.

    Creates a bi-directional pipe, and sends messages around the loop.
    """
    left, right = pipe_connection

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


if __name__ == "__main__":
    pytest.main(sys.argv)
