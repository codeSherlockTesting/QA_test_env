"""Handler module 38: handler_038."""


def handler_038_handle(event):
    """Handle event for handler_038."""
    return {"handler": "handler_038", "event": event, "handled": True}


def handler_038_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_038", "all"]


class Handler038:
    def __init__(self):
        self.name = "handler_038"

    def process(self, event):
        return handler_038_handle(event)
