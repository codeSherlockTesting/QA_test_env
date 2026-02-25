"""Handler module 103: handler_103."""


def handler_103_handle(event):
    """Handle event for handler_103."""
    return {"handler": "handler_103", "event": event, "handled": True}


def handler_103_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_103", "all"]


class Handler103:
    def __init__(self):
        self.name = "handler_103"

    def process(self, event):
        return handler_103_handle(event)
