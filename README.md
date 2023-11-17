# PVC

```
⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀
⠀⠠⢴⣶⣿⣯⣉⣉⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⣉⣉⣽⣿⣶⡦⠄
⠀⢰⣤⡄⠈⢉⡉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⢉⣉⣁⣠⣤⡆
⠀⢸⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⢸⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠸⢿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇
⠀⠀⠀⣤⣀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⣉⣉⣁⣤
⠀⠀⠀⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠛⠛⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛
```

PVC is a two-way router for Spout and Syphon. You can pass images through the PVC receiver, do whatever post-processing you want with it, and then send it back through the PVC sender.

## Setup

### Activate virtual environment

```
conda activate ./.venv
```

### Generate / update virtual environment

```
conda env update --prefix ./.venv --file environment.yml  --prune
```

## Testing

```
python pvc/pipe/pipe_test.py
```

## API

```
uvicorn pvc.api:pvc --reload
```

### Spout/Syphon API design

1. Client places image in the sender spout/syphon buffer
2. Client sends a message over websocket, alerting the server of what to do with the next image. The server can read the image into memory, and pass it to the appropriate OP callback
3. Server executes the OP callback, and finishes the transaction by placing it in the reciever spout/syphon buffer
4. Server sends a message over websocker, alerting the client that the processing is done.

### API Schema

#### Input

```
{
    "op": {
        "name": "ControlNet",
        "config": {
            ...
        }
    }
}
```

#### Result

```
{
    "status": "done"
    "msg": ""
}
```

```
{
    "status": "error"
    "msg": "reason"
}
```
