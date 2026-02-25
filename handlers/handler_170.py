"""Handler module 170: handler_170."""


def handler_170_handle(event):
    """Handle event for handler_170."""
    return {"handler": "handler_170", "event": event, "handled": True}


def handler_170_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_170", "all"]


class Handler170:
    def __init__(self):
        self.name = "handler_170"

    def process(self, event):
        return handler_170_handle(event)
