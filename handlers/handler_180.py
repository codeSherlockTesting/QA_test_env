"""Handler module 180: handler_180."""


def handler_180_handle(event):
    """Handle event for handler_180."""
    return {"handler": "handler_180", "event": event, "handled": True}


def handler_180_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_180", "all"]


class Handler180:
    def __init__(self):
        self.name = "handler_180"

    def process(self, event):
        return handler_180_handle(event)
