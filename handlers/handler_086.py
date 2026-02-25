"""Handler module 86: handler_086."""


def handler_086_handle(event):
    """Handle event for handler_086."""
    return {"handler": "handler_086", "event": event, "handled": True}


def handler_086_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_086", "all"]


class Handler086:
    def __init__(self):
        self.name = "handler_086"

    def process(self, event):
        return handler_086_handle(event)
