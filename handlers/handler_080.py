"""Handler module 80: handler_080."""


def handler_080_handle(event):
    """Handle event for handler_080."""
    return {"handler": "handler_080", "event": event, "handled": True}


def handler_080_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_080", "all"]


class Handler080:
    def __init__(self):
        self.name = "handler_080"

    def process(self, event):
        return handler_080_handle(event)
