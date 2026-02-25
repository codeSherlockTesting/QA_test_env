"""Handler module 101: handler_101."""


def handler_101_handle(event):
    """Handle event for handler_101."""
    return {"handler": "handler_101", "event": event, "handled": True}


def handler_101_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_101", "all"]


class Handler101:
    def __init__(self):
        self.name = "handler_101"

    def process(self, event):
        return handler_101_handle(event)
