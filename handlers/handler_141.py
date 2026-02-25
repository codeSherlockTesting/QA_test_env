"""Handler module 141: handler_141."""


def handler_141_handle(event):
    """Handle event for handler_141."""
    return {"handler": "handler_141", "event": event, "handled": True}


def handler_141_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_141", "all"]


class Handler141:
    def __init__(self):
        self.name = "handler_141"

    def process(self, event):
        return handler_141_handle(event)
