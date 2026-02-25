"""Handler module 96: handler_096."""


def handler_096_handle(event):
    """Handle event for handler_096."""
    return {"handler": "handler_096", "event": event, "handled": True}


def handler_096_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_096", "all"]


class Handler096:
    def __init__(self):
        self.name = "handler_096"

    def process(self, event):
        return handler_096_handle(event)
