"""Handler module 2: handler_002."""


def handler_002_handle(event):
    """Handle event for handler_002."""
    return {"handler": "handler_002", "event": event, "handled": True}


def handler_002_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_002", "all"]


class Handler002:
    def __init__(self):
        self.name = "handler_002"

    def process(self, event):
        return handler_002_handle(event)
