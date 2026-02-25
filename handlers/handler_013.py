"""Handler module 13: handler_013."""


def handler_013_handle(event):
    """Handle event for handler_013."""
    return {"handler": "handler_013", "event": event, "handled": True}


def handler_013_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_013", "all"]


class Handler013:
    def __init__(self):
        self.name = "handler_013"

    def process(self, event):
        return handler_013_handle(event)
