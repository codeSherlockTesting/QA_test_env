"""Handler module 28: handler_028."""


def handler_028_handle(event):
    """Handle event for handler_028."""
    return {"handler": "handler_028", "event": event, "handled": True}


def handler_028_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_028", "all"]


class Handler028:
    def __init__(self):
        self.name = "handler_028"

    def process(self, event):
        return handler_028_handle(event)
