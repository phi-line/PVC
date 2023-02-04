from pvc.op import operator


def validate_op(op_input: dict):
    """
    A simple validator for the operator input data

    {
       "op": {
            "name": "upscale",
            "config": {
                "model": "real-esrgan",
                "factor": 4,
          }
       }
    }
    """
    assert op_input.get("op") is not None, 'Input does not contain "op"'
    assert (
        op_input["op"].get("name") is not None
    ), 'Input operator does not contain "name"'
    assert (
        op_input["op"]["name"] in operator.OPERATORS
    ), f'Input operator "{data["op"]["name"]}" is not valid.'

    assert (
        op_input["op"].get("config") is not None
    ), 'Input operator does not contain a "config"'
