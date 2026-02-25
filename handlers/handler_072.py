"""Handler module 72: handler_072."""


def handler_072_handle(event):
    """Handle event for handler_072."""
    return {"handler": "handler_072", "event": event, "handled": True}


def handler_072_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_072", "all"]


class Handler072:
    def __init__(self):
        self.name = "handler_072"

    def process(self, event):
        return handler_072_handle(event)
