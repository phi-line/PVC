from fastapi import FastAPI, WebSocket

from pvc.op import validator, OPERATORS

pvc = FastAPI()

@pvc.websocket("/pipe")
async def pipe(ws: WebSocket):
    """
    /pipe is a websocket endpoint that allows for the transfer of images between
    a client and a server. The client sends an image over spout/syphon, along
    with some details about what processing to do once it gets to the server.

    1. Client places image in the sender spout/syphon buffer.
    2. Client sends a message over websocket, alerting the server of what to do with
       the next image. The server can read the image into memory, and pass it to the
       appropriate OP callback.
    3. Server executes the OP callback, and finishes the transaction by placing it
       in the reciever spout/syphon buffer.
    4. Server sends a message over websocker, alerting the client that the
       processing is done.
    """
    await ws.accept()
    while True:
        input_data = await ws.receive_json()

        try:
            name, config = validator.validate_op(input_data)
        except AssertionError as e:
            await ws.send_json({"status": "error", "msg": str(e)})
    
        op = OPERATORS[name](config)
