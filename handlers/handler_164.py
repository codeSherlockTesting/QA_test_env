"""Handler module 164: handler_164."""


def handler_164_handle(event):
    """Handle event for handler_164."""
    return {"handler": "handler_164", "event": event, "handled": True}


def handler_164_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_164", "all"]


class Handler164:
    def __init__(self):
        self.name = "handler_164"

    def process(self, event):
        return handler_164_handle(event)
