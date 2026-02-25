"""Handler module 4: handler_004."""


def handler_004_handle(event):
    """Handle event for handler_004."""
    return {"handler": "handler_004", "event": event, "handled": True}


def handler_004_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_004", "all"]


class Handler004:
    def __init__(self):
        self.name = "handler_004"

    def process(self, event):
        return handler_004_handle(event)
