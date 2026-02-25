"""Handler module 190: handler_190."""


def handler_190_handle(event):
    """Handle event for handler_190."""
    return {"handler": "handler_190", "event": event, "handled": True}


def handler_190_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_190", "all"]


class Handler190:
    def __init__(self):
        self.name = "handler_190"

    def process(self, event):
        return handler_190_handle(event)
