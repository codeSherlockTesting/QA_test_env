"""Handler module 138: handler_138."""


def handler_138_handle(event):
    """Handle event for handler_138."""
    return {"handler": "handler_138", "event": event, "handled": True}


def handler_138_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_138", "all"]


class Handler138:
    def __init__(self):
        self.name = "handler_138"

    def process(self, event):
        return handler_138_handle(event)
