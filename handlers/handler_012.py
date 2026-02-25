"""Handler module 12: handler_012."""


def handler_012_handle(event):
    """Handle event for handler_012."""
    return {"handler": "handler_012", "event": event, "handled": True}


def handler_012_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_012", "all"]


class Handler012:
    def __init__(self):
        self.name = "handler_012"

    def process(self, event):
        return handler_012_handle(event)
