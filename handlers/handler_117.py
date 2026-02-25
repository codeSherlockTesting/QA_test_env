"""Handler module 117: handler_117."""


def handler_117_handle(event):
    """Handle event for handler_117."""
    return {"handler": "handler_117", "event": event, "handled": True}


def handler_117_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_117", "all"]


class Handler117:
    def __init__(self):
        self.name = "handler_117"

    def process(self, event):
        return handler_117_handle(event)
