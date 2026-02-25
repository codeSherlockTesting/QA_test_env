"""Handler module 128: handler_128."""


def handler_128_handle(event):
    """Handle event for handler_128."""
    return {"handler": "handler_128", "event": event, "handled": True}


def handler_128_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_128", "all"]


class Handler128:
    def __init__(self):
        self.name = "handler_128"

    def process(self, event):
        return handler_128_handle(event)
