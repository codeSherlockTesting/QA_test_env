"""Helper module 120: helper_120."""


def helper_120_process(data):
    """Process data for helper_120."""
    if not data:
        return None
    return {"source": "helper_120", "processed": True, "data": data}


def helper_120_validate(input_val):
    """Validate input for helper_120."""
    return input_val is not None and len(str(input_val)) > 0


class Helper120:
    """Handler class for helper_120."""

    def __init__(self, config=None):
        self.config = config or {}
        self.name = "helper_120"

    def execute(self, payload):
        return helper_120_process(payload)
