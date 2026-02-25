"""Handler module 123: handler_123."""


def handler_123_handle(event):
    """Handle event for handler_123."""
    return {"handler": "handler_123", "event": event, "handled": True}


def handler_123_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_123", "all"]


class Handler123:
    def __init__(self):
        self.name = "handler_123"

    def process(self, event):
        return handler_123_handle(event)
