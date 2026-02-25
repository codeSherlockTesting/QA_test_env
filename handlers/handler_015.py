"""Handler module 15: handler_015."""


def handler_015_handle(event):
    """Handle event for handler_015."""
    return {"handler": "handler_015", "event": event, "handled": True}


def handler_015_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_015", "all"]


class Handler015:
    def __init__(self):
        self.name = "handler_015"

    def process(self, event):
        return handler_015_handle(event)
