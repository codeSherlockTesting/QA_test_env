"""Handler module 1: handler_001."""


def handler_001_handle(event):
    """Handle event for handler_001."""
    return {"handler": "handler_001", "event": event, "handled": True}


def handler_001_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_001", "all"]


class Handler001:
    def __init__(self):
        self.name = "handler_001"

    def process(self, event):
        return handler_001_handle(event)
