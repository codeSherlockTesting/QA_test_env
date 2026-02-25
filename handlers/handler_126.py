"""Handler module 126: handler_126."""


def handler_126_handle(event):
    """Handle event for handler_126."""
    return {"handler": "handler_126", "event": event, "handled": True}


def handler_126_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_126", "all"]


class Handler126:
    def __init__(self):
        self.name = "handler_126"

    def process(self, event):
        return handler_126_handle(event)
