import asyncio

from pvc import pvc

CYAN = np.array([[[0, 255, 255, 255]]], dtype=np.uint8)
MAGENTA = np.array([[[255, 0, 255, 255]]], dtype=np.uint8)


def test_pvc():
    # instantiate two PVC frame buffers, A and B
    left = pvc.PVCServer.create(sender_name="A", receiver_name="B")
    right = pvc.PVCServer.create(sender_name="B", receiver_name="A")

    # first send a cyan frame from left to right, through A
    left.send(CYAN, dtype=np.uint8)

    frame = right.receive()
    assert frame == CYAN

    # then send a magenta frame from right to left, through B
    right.send(MAGENTA, dtype=np.uint8)

    frame = left.receive()
    assert frame == MAGENTA


if __name__ == "__main__":
    pytest.main(sys.argv)
