"""Handler module 140: handler_140."""


def handler_140_handle(event):
    """Handle event for handler_140."""
    return {"handler": "handler_140", "event": event, "handled": True}


def handler_140_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_140", "all"]


class Handler140:
    def __init__(self):
        self.name = "handler_140"

    def process(self, event):
        return handler_140_handle(event)
