"""Handler module 187: handler_187."""


def handler_187_handle(event):
    """Handle event for handler_187."""
    return {"handler": "handler_187", "event": event, "handled": True}


def handler_187_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_187", "all"]


class Handler187:
    def __init__(self):
        self.name = "handler_187"

    def process(self, event):
        return handler_187_handle(event)
