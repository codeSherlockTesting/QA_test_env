"""Handler module 165: handler_165."""


def handler_165_handle(event):
    """Handle event for handler_165."""
    return {"handler": "handler_165", "event": event, "handled": True}


def handler_165_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_165", "all"]


class Handler165:
    def __init__(self):
        self.name = "handler_165"

    def process(self, event):
        return handler_165_handle(event)
