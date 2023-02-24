from pvc.op import operator

OPERATORS = {
    # default operator that simply returns a NoOP
    "_": lambda: operator.NoOP,
    "ControlNet": lambda: operator.ControlNet,
}

def validate_op(op_input: dict) -> operator.OP:
    """
    A simple validator for the operator input data.

    Example:
    {
       "op": {
            "name": "ControlNet",
            "config": {
                ...
            }
        }
    }
    """
    assert op_input.get("op") is not None, 'Input does not contain "op"'
    assert (
        op_input["op"].get("name") is not None
    ), 'Input operator does not contain "name"'
    assert (
        op_input["op"]["name"] in OPERATORS
    ), f'Input operator "{op_input["op"]["name"]}" is not valid.'

    assert (
        op_input["op"].get("config") is not None
    ), 'Input operator does not contain a "config"'

    name = op_input["op"]["name"]
    config = op_input["op"]["config"]
    return name, config