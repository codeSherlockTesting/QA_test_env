"""Handler module 100: handler_100."""


def handler_100_handle(event):
    """Handle event for handler_100."""
    return {"handler": "handler_100", "event": event, "handled": True}


def handler_100_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_100", "all"]


class Handler100:
    def __init__(self):
        self.name = "handler_100"

    def process(self, event):
        return handler_100_handle(event)
