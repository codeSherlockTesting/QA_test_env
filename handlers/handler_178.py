"""Handler module 178: handler_178."""


def handler_178_handle(event):
    """Handle event for handler_178."""
    return {"handler": "handler_178", "event": event, "handled": True}


def handler_178_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_178", "all"]


class Handler178:
    def __init__(self):
        self.name = "handler_178"

    def process(self, event):
        return handler_178_handle(event)
